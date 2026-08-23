"""Public comparison pages, sitemap/robots, and the reference bench (Move 2).

Guards the profit lens: comparison content is the CAC cutter (loaded
~$1,000/close toward the ~$150 cash floor), so these pages must stay public,
rank-ready, and honest — every price cites its source, estimates are flagged
third-party, and nothing is invented.
"""

import pytest
from django.test import Client

from core.marketing_data import CANONICAL_PATHS, COMPETITORS
from core.marketing_models import CaseStudy
from core.models import Organization

pytestmark = pytest.mark.django_db

PAGE_NEEDLES = (
    ("/compare/tank-track/", ("$180", "$150", "$480", "$630", "August 2026")),
    ("/compare/servicecore/", ("Quote-only", "annual contract", "6-12 week", "August 2026")),
    ("/compare/pumpdocket/", ("$99", "$139", "75", "August 2026")),
)


@pytest.fixture
def anon_client(db: None) -> Client:
    """Crawlers and prospects reach these pages without an account."""
    return Client()


class TestComparisonPages:
    @pytest.mark.parametrize(("url", "needles"), PAGE_NEEDLES)
    def test_page_is_public_with_verified_pricing(
        self, anon_client: Client, url: str, needles: tuple[str, ...]
    ) -> None:
        response = anon_client.get(url)

        assert response.status_code == 200
        body = response.content.decode()
        for needle in needles:
            assert needle in body

    @pytest.mark.parametrize("url", [url for url, _ in PAGE_NEEDLES])
    def test_page_flags_estimates_and_carries_seo_meta(self, anon_client: Client, url: str) -> None:
        body = anon_client.get(url).content.decode()

        assert "third-party reported" in body.lower()
        assert "confirm current terms" in body  # freshness disclaimer
        assert '<meta name="description"' in body

    def test_titles_target_buyer_research_terms(self, anon_client: Client) -> None:
        expected = {
            "tank-track": "Tank Track",
            "servicecore": "ServiceCore",
            "pumpdocket": "PumpDocket",
        }

        for slug, name in expected.items():
            body = anon_client.get(f"/compare/{slug}/").content.decode()

            assert name in body.split("</title>")[0]

    def test_cta_points_at_import(self, anon_client: Client) -> None:
        for url, _ in PAGE_NEEDLES:
            body = anon_client.get(url).content.decode()

            assert 'href="/import/"' in body


class TestPricingHonesty:
    def test_every_competitor_fact_cites_its_source(self) -> None:
        for entry in COMPETITORS:
            assert entry["source_domain"] in entry["price_note"]

    def test_servicecore_shows_no_invented_price(self, anon_client: Client) -> None:
        body = anon_client.get("/compare/servicecore/").content.decode()

        assert "no dollar figures" in body.lower()
        assert "third-party reported" in body.lower()

    def test_pumpdocket_quotes_their_own_disclaimer(self, anon_client: Client) -> None:
        body = anon_client.get("/compare/pumpdocket/").content.decode()

        assert "We don't guarantee compliance" in body


class TestDiscovery:
    def test_index_links_all_comparisons(self, anon_client: Client) -> None:
        body = anon_client.get("/compare/").content.decode()

        for entry in COMPETITORS:
            assert f"/compare/{entry['slug']}/" in body

    def test_sitemap_lists_public_pages_only(self, anon_client: Client) -> None:
        response = anon_client.get("/sitemap.xml")

        assert response.status_code == 200
        assert response["Content-Type"] == "application/xml"
        body = response.content.decode()
        for path in CANONICAL_PATHS:
            assert path in body
        assert "/admin/" not in body

    def test_robots_points_at_sitemap(self, anon_client: Client) -> None:
        response = anon_client.get("/robots.txt")

        assert response.status_code == 200
        assert "Sitemap:" in response.content.decode()


class TestWallOfLove:
    def test_dashboard_counts_only_callable_references(
        self, client: Client, org: Organization
    ) -> None:
        CaseStudy.objects.create(
            organization=org, title="Callable Co", quote="q", outcome="o", is_callable=True
        )
        CaseStudy.objects.create(
            organization=org, title="Quiet Co", quote="q", outcome="o", is_callable=False
        )

        body = client.get("/").content.decode()

        assert "Wall of Love" in body
        assert "Callable Co" in body
        assert "Quiet Co" not in body

    def test_seeded_bench_is_sample_and_never_callable(self) -> None:
        assert CaseStudy.objects.count() == 3
        assert CaseStudy.objects.filter(is_callable=False, sample=True).count() == 3
