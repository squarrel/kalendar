from django import forms
from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
	
	
	class Meta:
		model = Reservation
		fields = ['date_reserved', 'title', 'confirmed']
