from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from helpdesk.forms import PublicTicketForm


class DomainRestrictedPublicTicketForm(PublicTicketForm):
    """Public ticket form that only accepts submitter emails on approved domains.

    Enabled by setting HELPDESK_ALLOWED_SUBMITTER_DOMAINS to a list of domains
    (e.g. ["addleman.tech"]). An empty list means no restriction — anyone can
    submit, which is the stock behaviour. Wired in via the upstream-provided
    HELPDESK_PUBLIC_TICKET_FORM_CLASS hook, so helpdesk itself is untouched.
    """

    def clean_submitter_email(self):
        email = self.cleaned_data.get("submitter_email") or ""
        allowed = [
            d.strip().lower()
            for d in getattr(settings, "HELPDESK_ALLOWED_SUBMITTER_DOMAINS", [])
            if d.strip()
        ]
        if allowed and email:
            domain = email.rsplit("@", 1)[-1].lower()
            if domain not in allowed:
                raise forms.ValidationError(
                    _("Tickets can only be submitted from an approved email domain.")
                )
        return email
