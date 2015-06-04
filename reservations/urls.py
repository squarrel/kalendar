from django.conf.urls import url
from reservations import views

urlpatterns = [
	url(r'^$', views.reservations, name='reservations'),
	url(r'^(?P<reservation_id>\d+)/$', views.reservation, name='reservation'),
	url(r'^make-reservation/$', views.make_reservation,	name='make-reservation'),
	url(r'^edit-reservation/(?P<reservation_id>\d+)/$', views.edit_reservation, name='edit-reservation'),
	url(r'^delete-reservation/(?P<reservation_id>\d+)/$', views.delete_reservation, name='delete-reservation'),
	url(r'^calendar/$', views.this_month, name='this_month'),
	url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/$', views.calendar, name='calendar'),
]
