"""Rebase already-registered ModelAdmins/inlines onto Unfold base classes.

Third-party apps (notably django-helpdesk) register their admins against
Django's stock ``admin.ModelAdmin``, so Unfold only styles the surrounding
chrome and their add/change forms render unstyled. We rebuild each
registration in place as a subclass that mixes the Unfold base class in front
of the original, preserving every original option (list_display, inlines,
custom methods, ...) while picking up Unfold's form templates and widgets.

Django's ``UserAdmin`` is special-cased: it swaps in a different form and
fieldsets on the *add* page (username + password fields). Putting Unfold first
in the MRO would shadow that logic and render an empty add-user form, so for
UserAdmin we keep the base class first and instead supply Unfold's own themed
auth forms — the pattern Unfold documents.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import StackedInline as UnfoldStackedInline
from unfold.admin import TabularInline as UnfoldTabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


def _rebase_inline(inline):
    """Return an inline class derived from the matching Unfold inline base."""
    if issubclass(inline, admin.StackedInline) and not issubclass(
        inline, UnfoldStackedInline
    ):
        return type(inline.__name__, (UnfoldStackedInline, inline), {})
    if issubclass(inline, admin.TabularInline) and not issubclass(
        inline, UnfoldTabularInline
    ):
        return type(inline.__name__, (UnfoldTabularInline, inline), {})
    return inline


def apply():
    for model, model_admin in list(admin.site._registry.items()):
        admin_cls = type(model_admin)
        if issubclass(admin_cls, UnfoldModelAdmin):
            continue  # already Unfold-based

        if issubclass(admin_cls, UserAdmin):
            # Keep UserAdmin first so its add-form / add_fieldsets logic wins;
            # Unfold supplies themed auth forms and styling via the mixin.
            new_cls = type(
                admin_cls.__name__,
                (admin_cls, UnfoldModelAdmin),
                {
                    "form": UserChangeForm,
                    "add_form": UserCreationForm,
                    "change_password_form": AdminPasswordChangeForm,
                },
            )
        else:
            attrs = {}
            if admin_cls.inlines:
                attrs["inlines"] = [_rebase_inline(i) for i in admin_cls.inlines]
            new_cls = type(admin_cls.__name__, (UnfoldModelAdmin, admin_cls), attrs)

        admin.site.unregister(model)
        admin.site.register(model, new_cls)
