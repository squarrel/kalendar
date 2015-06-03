from django.shortcuts import render, render_to_response, \
	get_object_or_404, get_list_or_404
from django.contrib import auth
from django.core.context_processors import csrf

from reservations.models import Reservation

TITLE = 'Home'


def index(request):
	if Reservation.objects.all().exists():
		reservations = Reservations.objects.all()\
									.order_by('-date_created')[:5]
	else:
		reservations = None
	args = {}
	args['title'] = TITLE
	args['reservations'] = reservations
	return render(request, 'index.html', args)
