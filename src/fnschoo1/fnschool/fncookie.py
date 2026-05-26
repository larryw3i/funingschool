import os
import re
import sys
from urllib.parse import parse_qs, unquote

from django.http import QueryDict


def get_search_params_from_cookie(request, name=None):
    params = QueryDict()
    name = name or request.path
    if name.endswith("/"):
        name = name.rstrip("/")
    if name.startswith("/"):
        name = name.lstrip("/")
    if name in request.COOKIES:
        params = unquote(request.COOKIES[name])
        if params.startswith("?"):
            params = consumptions_sort_params[1:]
        params = QueryDict(params)
        return params
    return QueryDict()


def get_object_orders_from_cookie(request, name=None):
    name = name or request.path
    orders = []
    params = get_search_params_from_cookie(request, name)
    if params:
        for key, value in params.items():
            if key.startswith("sort_"):
                key = key[5:]
                orders.append(f"-{key}" if value == "-" else key)
    orders.reverse()
    return orders or []


# The end.
