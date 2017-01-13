from django.conf.urls import url
from . import views

app_name = 'therm'

urlpatterns = [
    # /therm/
    url(r'^$', views.index, name='index'),
    # /therm/some request
    url(r'^Compute/$', views.computetherm, name='computetherm')
]
