from django.conf.urls.defaults import *
from app.views import CustomRegistrationView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'app.views.main'),
                       url(r'^signup$', 'app.account.signup'),
                       url(r'^start$', 'app.views.start', name="start"),
                       url(r'^preferences$', 'app.views.preferences'),
                       url(r'^choose$', 'app.views.choose'),
                       url(r'^results$', 'app.views.results'),
                       url(r'^import$', 'app.import.main', name='import'),
                       url(r'^versions$', 'app.views.versions', name='versions'),
                       url(r'^v(?P<version_id>[0-9]+)$', 'app.views.set_version'),
                       url(r'^my_foodie$', 'app.views.my_foodie'), # reinier
                       url(r'^random_meal$', 'app.views.random_meal'), #reinier
                       url(r'^about$', 'app.views.about'), #reinier
                       url(r'^intro2$', 'app.views.intro2'),
                       url(r'^intro3$', 'app.views.intro3'),
                       url(r'^intro4$', 'app.views.intro4'),
                       url(r'^intro5$', 'app.views.intro5'),
                       url(r'^intro6$', 'app.views.intro6'),
                       url(r'^intro7$', 'app.views.intro7'),
                       url(r'^intro8$', 'app.views.intro8'),
                       url(r'^intro9$', 'app.views.intro9'),
                       url(r'^VIP$', 'app.views.VIP'), #Chums
                       url(r'^accounts/register/$',
                           CustomRegistrationView.as_view(),
                           name='registration_register'),
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
                       # (r'^accounts/', include('registration.backends.simple.urls')),
)
urlpatterns += staticfiles_urlpatterns()

