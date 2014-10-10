from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    """
    index
    """
    return render_to_response('index.html', {},
                              context_instance=RequestContext(request))
