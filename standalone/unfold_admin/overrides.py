"""Rebase already-registered ModelAdmins/inlines onto Unfold base classes.

Third-party apps (notably django-helpdesk) register their admins against
Django's stock ``admin.ModelAdmin``, so Unfold only styles the surrounding
chrome and their add/change forms render unstyled. We rebuild each
registration in place as a subclass that mixes the Unfold base class in front
of the original, preserving every original option (list_display, inlines,
custom methods, ...) while picking up Unfold's form templates and widgets.
"""

from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import StackedInline as UnfoldStackedInline
from unfold.admin import TabularInline as UnfoldTabularInline


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

        attrs = {}
        if admin_cls.inlines:
            attrs["inlines"] = [_rebase_inline(i) for i in admin_cls.inlines]

        new_cls = type(admin_cls.__name__, (UnfoldModelAdmin, admin_cls), attrs)
        admin.site.unregister(model)
        admin.site.register(model, new_cls)
