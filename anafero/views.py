from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from anafero.models import Referral


@login_required
@require_POST
def create_referral(request):
    target = None
    referral = Referral.create(
        user=request.user,
        redirect_to=request.POST.get("redirect_to"),
        target=target
    )
    path = reverse("anafero_process_referral", code=referral.code)
    domain = Site.objects.get_current().domain
    url = "http://%s%s" % (domain, path)
    return HttpResponse(json.dumps({"status": "OK", "url": url}))


def process_referral(request, code):
    referral = get_object_or_404(Referral, code=code)
    referral.respond(request, "RESPONDED")
    return redirect(referral.redirect_to)