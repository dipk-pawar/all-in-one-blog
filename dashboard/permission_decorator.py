from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def editor_or_admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser
        or u.groups.filter(name__in=["Blog writer", "Manager"]).exists(),
        login_url="/dashboard/no-permission/",
        redirect_field_name=None,
    )
    return actual_decorator(function) if function else actual_decorator


def manager_or_admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name="Manager").exists(),
        login_url="/dashboard/no-permission/",
        redirect_field_name=None,
    )
    return actual_decorator(function) if function else actual_decorator
