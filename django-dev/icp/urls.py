from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^icp/', include('icp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
#    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'icp_main.views.index'),
    (r'^research/', 'icp_main.views.research'),
    (r'^showcase/$', 'icp_main.views.showcase'),
    (r'^showcase/project/(?P<project_name>[a-zA-Z][a-zA-Z0-9]+)$', 'icp_main.views.showcase_project'),
    (r'^showcase/event/(?P<event_name>[a-zA-Z][a-zA-Z0-9]+)$', 'icp_main.views.showcase_event'),
	(r'^gallery/$', 'icp_main.views.gallery'),
    (r'^gallery/project/(?P<project_name>[a-zA-Z][a-zA-Z0-9]+)$', 'icp_main.views.gallery_project'),
    (r'^gallery/event/(?P<event_name>[a-zA-Z][a-zA-Z0-9]+)$', 'icp_main.views.gallery_event'),
    (r'^resource/', 'icp_main.views.resource'),
    (r'^partner/', 'icp_main.views.partner'),
    (r'^contact/', 'icp_main.views.contact'),
    (r'^login/', 'icp_main.views.loginpage'),
    (r'^logout/', 'icp_main.views.logoutpage'),
    (r'^memberfiles/(?P<filename>[a-zA-Z0-9 -_.]+)$', 'icp_main.views.memberdownload'),
    (r'^newpass/', 'icp_main.views.newpass'),
    (r'^register/', 'icp_main.views.register'),


)
