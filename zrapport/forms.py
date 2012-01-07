from django import forms
from zrapport.models import ReportType

class CountingForm(forms.Form):
	onethousand = forms.IntegerField(min_value = 0)
	fivehundred = forms.IntegerField(min_value = 0)
	twohundred = forms.IntegerField(min_value = 0)
	onehundred = forms.IntegerField(min_value = 0)
	fifty = forms.IntegerField(min_value = 0)
	twenty = forms.IntegerField(min_value = 0)
	ten = forms.IntegerField(min_value = 0)
	five = forms.IntegerField(min_value = 0)
	one = forms.IntegerField(min_value = 0)
	half = forms.IntegerField(min_value = 0)

class SettlementForm(CountingForm):
	sale_high_tax = forms.DecimalField(min_value = 0, decimal_places = 1)
	sale_mid_tax = forms.DecimalField(min_value = 0, decimal_places = 1)
	sale_no_tax = forms.DecimalField(min_value = 0, decimal_places = 1)
	payment_card = forms.DecimalField(min_value = 0, decimal_places = 1)
	payment_cash = forms.DecimalField(min_value = 0, decimal_places = 1)
	payment_bong = forms.DecimalField(min_value = 0, decimal_places = 1)
	other_membership = forms.DecimalField(min_value = 0, decimal_places = 1)

class StartForm(CountingForm):
	report_type_id = forms.ChoiceField(choices = ReportType.objects.values_list('id', 'name'))
