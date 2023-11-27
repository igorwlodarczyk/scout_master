from functools import wraps
from django.shortcuts import redirect


def group_required(required_group):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if (
                request.user.is_authenticated
                and request.user.groups.filter(name=required_group).exists()
            ):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("/login/")

        return wrapper

    return decorator
