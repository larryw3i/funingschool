import os
import re
import sys
from urllib.parse import parse_qs, unquote

from django.http import QueryDict


def get_search_params_from_cookie(request, name):
    params = QueryDict()
    if name in request.COOKIES:
        params = unquote(request.COOKIES[name])
        if params.startswith("?"):
            params = consumptions_sort_params[1:]
        params = QueryDict(params)
        return params
    return None


def get_object_orders_from_cookie(request, name):
    cookie_name = name
    orders = []
    params = get_search_params_from_cookie(request, cookie_name)
    if params:
        for key, value in params.items():
            if key.startswith("sort_"):
                key = key[5:]
                orders.append(f"-{key}" if value == "-" else key)
    return orders.reverse()


# The end.
