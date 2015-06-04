from django.shortcuts import render, render_to_response, \
	get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils import timezone

from reservations.models import Reservation
from reservations.forms import ReservationForm

import time
from datetime import date, datetime
from calendar import monthrange

TITLE = 'Reservations'
MONTHS = 'January February March April May June July August September \
	October November December'
MONTHS = MONTHS.split()


def reservations(request):
	if Reservation.objects.all().exists():
		reservations = Reservation.objects.all().\
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
	if request.POST:
		form = ReservationForm(request.POST)
		if form.is_valid():# else what?
			form.save()
			return HttpResponseRedirect(reverse('reservations'))
	else:
		form = ReservationForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request, 'reservations/make_reservation.html', args)


def edit_reservation(request, reservation_id):
	if request.POST:
		if Reservation.objects.filter(pk=reservation_id).exists():
			instance = Reservation.objects.get(pk=reservation_id)
			form = ReservationForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('reservation',
												args=(reservation_id,)))
		else:
			return HttpResponseNotFound(
										'<h2>Reservation Not Found</h2>'
										)
	else:
		if Reservation.objects.filter(pk=reservation_id).exists():
			instance = Reservation.objects.get(pk=reservation_id)
			form = ReservationForm(instance=instance)
		else:
			return HttpResponseNotFound(
										'<h2>Reservation Not Found</h2>'
										)
	args = {}
	args['form'] = form
	args['reservation_id'] = reservation_id
	return render(request, 'reservations/edit_reservation.html', args)


def delete_reservation(request, reservation_id):
	if Reservation.objects.filter(pk=reservation_id).exists():
		Reservation.objects.filter(pk=reservation_id).delete()
	else:
		return HttpResponseNotFound(
									'<h2>Reservation Not Found</h2>'
									)
	return HttpResponseRedirect(reverse('reservations'))


def named_month(month_number):
	# return name of the month, given the number
	return date(1900, month_number, 1).strftime("%B")


def this_month(request):
	today = timezone.now()
	return calendar(request, today.year, today.month)


def calendar(request, year, month):
	my_year = int(year)
	my_month = int(month)
	my_calendar_from_month = datetime(my_year, my_month, 1)
	my_calendar_to_month = datetime(my_year, my_month,
									monthrange(my_year, my_month)[1], 
									23, 59)
	my_reservation_events = Reservation.objects.\
		filter(date_reserved__gte=my_calendar_from_month).\
		filter(date_reserved__lte=my_calendar_to_month)
	print("my_reservation_events", my_reservation_events)
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
	args['title'] = TITLE
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
