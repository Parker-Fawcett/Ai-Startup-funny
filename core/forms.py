"""Forms for CSV upload, job completion, and trial signup."""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

from core.importing import parse_customers_csv


class ImportForm(forms.Form):
    """One uploaded customer-list CSV; validation yields decoded text."""

    csv_file = forms.FileField(label="Customer CSV")

    def clean_csv_file(self) -> str:
        """Decode and validate at the boundary; return the CSV text."""
        upload = self.cleaned_data["csv_file"]
        try:
            text = upload.read().decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise forms.ValidationError("File is not valid UTF-8 text.") from error
        result = parse_customers_csv(text)
        if not result.rows:
            reason = "; ".join(error.reason for error in result.errors) or "no rows found"
            raise forms.ValidationError(f"Nothing imported: {reason}")
        return text


class CompleteForm(forms.Form):
    """The report fields captured at the curb, sized for gloved thumbs."""

    ALLOWED_PHOTO_SUFFIXES: frozenset[str] = frozenset({".jpg", ".jpeg", ".png", ".heic"})
    MAX_PHOTO_BYTES: int = 8 * 1024 * 1024

    gallons = forms.IntegerField(min_value=1)
    disposal_site = forms.CharField(max_length=200)
    system_type = forms.CharField(max_length=50, required=False)
    filter_action = forms.ChoiceField(
        choices=[
            ("none", "No filter / not serviced"),
            ("cleaned", "Filter cleaned"),
            ("replaced", "Filter replaced"),
        ],
        initial="none",
        required=False,
    )
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    photo = forms.FileField(required=False)

    def clean_photo(self) -> object | None:
        """Reject non-photo files and oversized uploads before anything persists."""
        upload = self.cleaned_data.get("photo")
        if not upload:
            return None
        suffix = "." + upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else ""
        if suffix not in self.ALLOWED_PHOTO_SUFFIXES:
            raise forms.ValidationError("Photo must be .jpg, .jpeg, .png, or .heic.")
        if upload.size > self.MAX_PHOTO_BYTES:
            raise forms.ValidationError("Photo must be 8 MB or smaller.")
        return upload


class SignupForm(forms.Form):
    """Self-serve trial form: one submission stands up a shop and its owner."""

    shop_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self) -> str:
        """Honeypot: a filled hidden field means bot."""
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""

    def clean_email(self) -> str:
        """Normalize case and block duplicate shop-owner accounts."""
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self) -> dict[str, object]:
        """Cross-field checks: password match plus Django's strength validators."""
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        if password1:
            user = User(username=cleaned.get("email", ""))
            try:
                password_validation.validate_password(password1, user)
            except forms.ValidationError as errors:
                self.add_error("password1", errors)
        return cleaned
