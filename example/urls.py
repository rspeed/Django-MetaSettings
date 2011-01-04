from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
	(r'^.*$', 'direct_to_template', {'template': 'placeholder.html'}),
)
