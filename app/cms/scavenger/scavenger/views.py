import os

from django.http import HttpResponse


def health_check(request):
    return HttpResponse()


def source_code_version(request):
    return HttpResponse(os.environ.get("SOURCE_CODE_VERSION", "not set").encode())
