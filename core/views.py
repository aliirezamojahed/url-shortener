from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import URLMapping, VisitedURL

import string
import secrets


def index(request):
    from django.db.models import Count
    benchmark = (VisitedURL.objects
        .values('key')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    for i, b in enumerate(benchmark):
        target_url = URLMapping.objects.get(key=b['key']).target_url
        benchmark[i]['target_url'] = target_url
    context = {
        'benchmark': benchmark,
    }
    return render(request, 'core/index.html', context)


def shortener_post(request):
    return shortener(request, request.POST['url'])


def shortener(request, url):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(6))
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(16))
    obj = URLMapping(key=key, target_url=url, secret_key=secret_key)
    obj.save()
    shortened_url = request.build_absolute_uri(reverse('redirect', args=[key]))
    return HttpResponse(f'Shortened URL: <a href="{shortened_url}">{shortened_url}</a>')


def redirect_url(request, key):

    def get_client_ip():
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    url_instance = URLMapping.objects.get(key=key)
    target_url = url_instance.target_url
    VisitedURL.objects.create(
        key=url_instance,
        is_pc=request.user_agent.is_pc,
        user_ip=get_client_ip(),
    )
    return redirect('http://' + target_url)
