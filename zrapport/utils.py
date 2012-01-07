from datetime import datetime, date
from django import utils
from django.core.exceptions import ObjectDoesNotExist
from zrapport.models import Report, ReportType

def fill_count(source, source_prefix = '', assignee_prefix = '', update = {}):
	x = {}
	tmp = source.cleaned_data if hasattr(source, 'cleaned_data') else vars(source)
	x['%sonethousand' % assignee_prefix] = tmp['%sonethousand' % source_prefix]
	x['%sfivehundred' % assignee_prefix] = tmp['%sfivehundred' % source_prefix]
	x['%stwohundred' % assignee_prefix] = tmp['%stwohundred' % source_prefix]
	x['%sonehundred' % assignee_prefix] = tmp['%sonehundred' % source_prefix]
	x['%sfifty' % assignee_prefix] = tmp['%sfifty' % source_prefix]
	x['%stwenty' % assignee_prefix] = tmp['%stwenty' % source_prefix]
	x['%sten' % assignee_prefix] = tmp['%sten' % source_prefix]
	x['%sfive' % assignee_prefix] = tmp['%sfive' % source_prefix]
	x['%sone' % assignee_prefix] = tmp['%sone' % source_prefix]
	x['%shalf' % assignee_prefix] = tmp['%shalf' % source_prefix]
	x.update(update)
	return x

def fill_settle(source, source_prefix = '', assignee_prefix = ''):
	tmp = source.cleaned_data if hasattr(source, 'cleaned_data') else vars(source)
	return fill_count(source, source_prefix, assignee_prefix, update = {
		'settle_datetime': datetime.today(),
		'sale_high_tax': tmp['sale_high_tax'],
		'sale_mid_tax': tmp['sale_mid_tax'],
		'sale_no_tax': tmp['sale_no_tax'],
		'payment_card': tmp['payment_card'],
		'payment_cash': tmp['payment_cash'],
		'payment_bong': tmp['payment_bong'],
		'other_membership': tmp['other_membership'],
	})

def get_last_report_id():
	in_this_year = "%s-01-01" % date.today().year
	try:
		return Report.objects.filter(start_datetime__gte=in_this_year).latest("report_id").report_id
	except ObjectDoesNotExist:
		return 0

def get_unfinished_report():
	try:
		return Report.objects.get(end_datetime=None)
	except ObjectDoesNotExist:
		return None
