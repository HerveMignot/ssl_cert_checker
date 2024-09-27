import functions_framework

from check_tools import check_certificates
from check_tools import WARN_IF_DAYS_LESS_THAN

@functions_framework.http
def check_endpoints(request):
    """Check SSL certifcate expiration date for endpoint.
    Args:
        request (flask.Request): The request object.
        <https://cloudfunctionsurl/endpoint=www.site.com[&warn=<days>]>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'endpoint' in request_json:
        endpoint = request_json['endpoint']
        warning = int(request_json.get('warn', WARN_IF_DAYS_LESS_THAN))
    elif request_args and 'endpoint' in request_args:
        endpoint = request_args['endpoint']
        warning = int(request_args.get('warn', WARN_IF_DAYS_LESS_THAN))
    else:
        return 400
    return check_certificates([endpoint], warning)[0]
