from django.conf.urls import url

from accounts.views import register, createprofile, changepass, viewprofile
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout

app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^profile/$', viewprofile, name='profile'),
    url(r'^profile/edit/$', createprofile, name='edit_profile'),
    url(r'^profile/changepass/$', changepass, name='changepass'),
    url(r'^profile/(?P<id>\d+)/$', viewprofile, name='view'),

]
