from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chrapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^santa/', include('secretsanta.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
