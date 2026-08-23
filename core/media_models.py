"""Job media: field photo attachments (proof-of-service evidence).

Photos at the tank are a validated paid-feature gap (rivals force a $79/mo
third-party subscription). Stored as plain ``FileField`` so no Pillow
dependency enters the stack; type/size validation happens at the form layer.
"""

from django.db import models


def _upload_path(instance: "JobAttachment", filename: str) -> str:
    return f"job-media/{instance.job_id}/{filename}"


class JobAttachment(models.Model):
    """One photo captured at the stop, tied to the completed job."""

    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self) -> str:
        return f"JOB-{self.job_id:06d} · {self.file.name.rsplit('/', 1)[-1]}"
