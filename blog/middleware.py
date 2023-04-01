from .models import Visitor


def my_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        visitor,isCreated=Visitor.objects.get_or_create(csrf=request.META['CSRF_COOKIE'],agent=request.META['HTTP_USER_AGENT'])
        if isCreated:
            visitor.visits=visitor.visits+1
        else:
            visitor.requests=visitor.requests+1
        visitor.host = request.META['COMPUTERNAME']
        visitor.ip = request.META['HTTP_HOST']
        visitor.os = request.META['HTTP_SEC_CH_UA_PLATFORM']
        visitor.save()
        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
    return middleware





