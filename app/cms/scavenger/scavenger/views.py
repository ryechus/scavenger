import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse


def health_check(request):
    return HttpResponse()


@staff_member_required
def source_code_version(request):
    return HttpResponse(os.environ.get("SOURCE_CODE_VERSION", "not set").encode())
