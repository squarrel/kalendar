from django.shortcuts import render, render_to_response, \
	get_object_or_404, get_list_or_404
from django.contrib import auth
from django.core.context_processors import csrf

from reservations.models import Reservation

import time
from datetime import date, datetime
from calendar import monthrange

TITLE = 'Reservations'
MONTHS = "January February March April May June July August September \
	October November December"
MONTHS = MONTHS.split()


def reservations(request):
	if Reservation.objects.all().exists():
		reservations = Reservations.objects.all().\
			order_by('-date_created')
	else:
		reservations = None
	args = {}
	args['title'] = TITLE
	args['reservations'] = reservations
	return render(request, 'reservations/reservations.html', args)


def reservation(request, reservation_id):
	reservation = get_object_or_404(Reservation, pk=reservation_id)
	args = {}
	args['title'] = TITLE
	args['reservation'] = reservation
	return render(request, 'reservations/reservation.html', args)


def make_reservation(request):
	pass


def edit_reservation(request, reservation_id):
	pass


def delete_reservation(request, reservation_id):
	pass


def named_month(month_number):
	# return name of the month, given the number
	return date(1900, month_number, 1).strftime("%B")


def this_month(request, reservation):
	today = timezone.now()
	return calendar(request, reservation, today.year, today.month)


def calendar(request, reservation, year, month):
	my_year = int(year)
	my_month = int(month)
	my_calendar_from_month = datetime(my_year, my_month, 1)
	my_calendar_to_month = datetime(my_year, my_month,
									monthrange(my_year, my_month)[1], 
									23, 59)
	my_reservation_events = Reservation.objects.\
		filter(date_reserved__gte=my_calendar_from_month).\
		filter(date_reserved__lte=my_calendar_to_month).\
		filter(reservation=reservation)
	my_previous_year = my_year
	my_previous_month = my_month - 1
	if my_previous_month == 0:
		my_previous_year = my_year - 1
		my_previous_month = 12
	my_next_year = my_year
	my_next_month = my_month + 1
	if my_next_month == 13:
		my_next_year = my_year + 1
		my_next_month = 1
	my_year_after_this = my_year + 1
	my_year_before_this = my_year - 1
	args = {}
	args['reservation'] = reservation
	args['reservation_list'] = my_reservation_events
	args['month'] = my_month
	args['month_name'] = named_month(my_month)
	args['year'] = my_year
	args['previous_month'] = my_previous_month
	args['previous_month_name'] = named_month(my_previous_month)
	args['previous_year'] = my_previous_year
	args['next_month'] = my_next_month
	args['next_month_name'] = named_month(my_next_month)
	args['next_year'] = my_next_year
	args['year_before_this'] = my_year_before_this
	args['year_after_this'] = my_year_after_this
	return render(request, 'reservations/calendar.html', args)
