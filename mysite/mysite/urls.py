from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from wsn.views import *

urlpatterns = [

    # url(r'^admin/', include(admin.site.urls)),
	url(r'^sensors/$', sensors),
	url(r'^udp/$',udp),
	url(r'^tcp/$',tcp),
	url(r'^html/$',html),
	url(r'^get_data/(.+)/$', get_data),
	url(r'^post_data/$', post_data),
	url(r'^get_ping/(.+)/$', get_ping),
	url(r'^post_ping/$', post_ping),
	url(r'^get_serial/(.+)/$', get_serial),
	url(r'^post_serial/$', post_serial),
    url(r'^demo/$', demo),
] 

#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

