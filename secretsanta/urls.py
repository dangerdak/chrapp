from django.conf.urls import patterns, url

from secretsanta import views

urlpatterns = patterns('',
        # Registration view
        url(r'^register/$',
            views.register,
            name='register'),
)
