from django.db import models


class Reservation(models.Model):
	date_reserved = models.DateTimeField(default='2015-01-01', null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=55, blank=True, null=True)
	description = models.TextField(max_length=450, blank=True, null=True)
	confirmed = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Reservations'
