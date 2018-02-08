from django.conf.urls import url
from . import views

from django.http import HttpResponse
def test(request):
    return HttpResponse('app level')

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^new$', views.new),
    url(r'^create$', views.create),
    url(r'^review/(?P<id>\d+)$', views.review),
    url(r'^addReview/(?P<id>\d+)$', views.addReview),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^deleteBook/(?P<id>\d+)$', views.deleteBook)
]
