""" handle requests for courseware search http requests """
import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from .api import perform_search


def do_search(request, course_id=None):
    """
    Search view for http requests
    """
    results = {
        "error": _("Nothing to search")
    }
    status_code = 500

    try:
        if request.method == 'POST':
            search_terms = request.POST["search_string"]

            # process pagination requests
            size = 20
            from_ = 0
            if "page_size" in request.POST:
                size = int(request.POST["page_size"])
                if "page_index" in request.POST:
                    from_ = int(request.POST["page_index"]) * size

            results = perform_search(
                search_terms,
                user=request.user,
                size=size,
                from_=from_,
                course_id=course_id,
            )

            status_code = 200
    # Allow for broad exceptions here - this is an entry point from external reference
    except Exception as err:  # pylint: disable=broad-except
        results = {
            "error": str(err)
        }

    return HttpResponse(
        json.dumps(results),
        content_type='application/json',
        status=status_code
    )
