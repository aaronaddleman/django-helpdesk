from django.apps import AppConfig


class UnfoldAdminConfig(AppConfig):
    """Local app that re-themes third-party admin registrations with Unfold.

    Listed last in INSTALLED_APPS so its ``ready()`` runs after Django's admin
    autodiscovery has imported every other app's ``admin.py`` (helpdesk, auth,
    etc.). At that point the admin registry is fully populated and we can
    rebase each ModelAdmin onto ``unfold.admin.ModelAdmin``.
    """

    name = "standalone.unfold_admin"
    label = "unfold_admin"

    def ready(self):
        from . import overrides

        overrides.apply()
