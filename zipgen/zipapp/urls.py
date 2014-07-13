from django.conf.urls import patterns, url

from zipapp import views

urlpatterns = patterns('',
    url(r'^test$', views.test, name='test'),

)

