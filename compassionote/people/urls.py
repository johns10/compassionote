from django.conf.urls import url
from django.forms import ModelForm

from . import views

app_name = 'people'
urlpatterns = [
	url(r'^$', views.index, name='home'),
    url(r'^contacts/', views.ContactsListView.as_view(), name='contacts'),
    url(r'contact/add/$', views.ContactCreate.as_view(), name='contact-add'),
    url(r'contact/(?P<pk>[0-9]+)/$', views.ContactDetailView.as_view(), name='contact-view'),
    url(r'contact/(?P<pk>[0-9]+)/edit/$', views.ContactUpdate.as_view(), name='contact-update'),
    url(r'contact/(?P<pk>[0-9]+)/delete/$', views.ContactDelete.as_view(), name='contact-delete'),
    url(r'^import/$', views.CsvImportCreate.as_view(), name='csvimporter'),
    url(r'^list/$', views.PersonListView.as_view(), name='people'),
    url(r'^(?P<pk>[0-9]+)/$', views.PersonDetailView.as_view(), name='person'),
    url(r'add/$', views.PersonCreateView.as_view(), name='person-add'),
    url(r'(?P<pk>[0-9]+)/edit/$', views.PersonUpdate.as_view(), name='person-edit'),
    url(r'(?P<pk>[0-9]+)/match/$', views.PersonMatch.as_view(), name='person-match'),
]