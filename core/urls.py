"""URL routes for the PumpRun owner app."""

from django.urls import path

from core import views, views_export, views_public

urlpatterns = [
    path("", views_public.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("import/", views.import_customers, name="import"),
    path("import/template.csv", views.import_template, name="import_template"),
    path("route/<str:route_day>/", views.route_day, name="route_day"),
    path("jobs/<int:pk>/complete/", views.job_complete, name="job_complete"),
    path("jobs/<int:pk>/report.pdf", views.job_report_pdf, name="job_report"),
    path("jobs/<int:pk>/invoice/pay/", views.invoice_mark_paid, name="invoice_pay"),
    path("i/<str:token>/", views_public.invoice_public, name="invoice_public"),
    path("i/<str:token>/pay/", views_public.invoice_pay_stripe, name="invoice_pay_stripe"),
    path(
        "billing/<int:org_pk>/subscribe/<str:plan>/",
        views_public.billing_subscribe,
        name="billing_subscribe",
    ),
    path("billing/<int:org_pk>/done/", views_public.billing_callback, name="billing_callback"),
    path(
        "export/route-sale/<str:route_day>/",
        views_export.route_sale_export,
        name="route_sale_export",
    ),
    path(
        "export/invoices/<int:year>/<int:month>/",
        views_export.invoice_export,
        name="invoice_export",
    ),
    # Public marketing pages (Move 2): deliberately login-free so crawlers reach them.
    path("compare/", views_public.compare_index, name="compare_index"),
    path("compare/tank-track/", views_public.compare_tank_track, name="compare_tank_track"),
    path("compare/servicecore/", views_public.compare_servicecore, name="compare_servicecore"),
    path("compare/pumpdocket/", views_public.compare_pumpdocket, name="compare_pumpdocket"),
    path("pricing/", views_public.pricing, name="pricing"),
    path("title5-kit/", views_public.title5_kit, name="title5_kit"),
    path("title5-kit.pdf", views_public.title5_kit_pdf, name="title5_kit_pdf"),
    path("title5-kit/done/", views_public.title5_kit_done, name="title5_kit_done"),
    path("signup/", views_public.signup, name="signup"),
    path("healthz/", views_public.health, name="health"),
    path("sw.js", views_public.service_worker, name="sw"),
    path("robots.txt", views_public.robots_txt, name="robots"),
    path("sitemap.xml", views_public.sitemap_xml, name="sitemap"),
]
