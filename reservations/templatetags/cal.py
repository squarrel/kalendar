from calendar import HTMLCalendar
from django import template
from django.core.urlresolvers import reverse
from datetime import date
from itertools import groupby
from collections import defaultdict
from django.utils.html import conditional_escape as esc

register = template.Library()


def do_reservations_calendar(parser, token):
	try:
		tag_name, year, month, reservation_list = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires three arguments" % token.contents.split()[0])
	return ReservationCalendarNode(year, month, reservation_list)


class ReservationCalendarNode(template.Node):
	def __init__(self, year, month, reservation_list):
		try:
			self.year = template.Variable(year)
			self.month = template.Variable(month)
			self.reservation_list = template.Variable(reservation_list)
		except ValueError:
			raise template.TemplateSyntaxError


	def render(self, context):
		try:
			my_reservation_list = self.reservation_list.resolve(context)
			my_year = self.year.resolve(context)
			my_month = self.month.resolve(context)
			cal = ReservationCalendar(my_reservation_list)
			return cal.formatmonth(int(my_year), int(my_month))
		except ValueError:
			return
		except template.VariableDoesNotExist:
			return


class ReservationCalendar(HTMLCalendar):
	def __init__(self, reservations):
		super(ReservationCalendar, self).__init__()
		self.reservations = self.group_by_day(reservations)


	def format_day(self, day, weekday):
		if day != 0:
			cssclass = self.cssclasses[weekday]
			if date.today() == date(self.year, self.month, day):
				cssclass += ' today'
			if day in self.reservations:
				cssclass += ' filled'
				body = ['<ul>']
				#print(day)
				for reservation in self.reservations[day]:
					print("reservation.date_reserved:", reservation.date_reserved)
					#print("reservation.confirmed:", reservation.confirmed)
					body.append('<li>')
					if reservation.confirmed:
						body.append('<a id="confirmed" href="%s">' % reverse('reservation', args=[reservation.id]))
					else:
						body.append('<a href="%s">' % reverse('reservation', args=[reservation.id]))
					body.append(esc(reservation.date_reserved.strftime("%Y/%m/%d")))
					body.append('</a></li>')
				body.append('</ul>')
				#print(body)
				return self.day_cell(cssclass, '<span class="day-number">%d</span> %s' % (day, ''.join(body)))
			return self.day_cell(cssclass, '<span class="day-number-no-reservation">%d</span>' % (day))
		return self.day_cell('noday', '&nbsp;')


	def formatmonth(self, year, month):
		self.year, self.month = year, month
		return super(ReservationCalendar, self).formatmonth(year, month)


	def group_by_day(self, reservations):
		days = []
		reservation_objects = []
		for r in reservations:
			days.append(r.date_reserved.day)
			reservation_objects.append(r)
		gr = {}
		for i in range(len(days)):
			day = days[i]
			reservation = reservation_objects[i]
			gr.setdefault(day, []).append(reservation)
		return gr


	def day_cell(self, cssclass, body):
		return '<td class="%s">%s</td>' % (cssclass, body)

register.tag("reservations_calendar", do_reservations_calendar)
