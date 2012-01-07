from datetime import datetime
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from zrapport.forms import CountingForm, SettlementForm, StartForm
from zrapport.models import Report, ReportType
from zrapport.utils import fill_count, fill_settle, get_last_report_id, get_unfinished_report

def counting(request, report_type_id):
	rt = get_object_or_404(ReportType, pk=report_type_id)
	return render_to_response('zrapport/_counting.html', {
		'form': CountingForm(fill_count(rt, source_prefix = 'start_'))
	}, context_instance = RequestContext(request))

def index(request):
	unfinished_report = get_unfinished_report()
	if unfinished_report:
		return HttpResponseRedirect('/unfinished/')
	return render(request, 'zrapport/index.html')

def new(request):
	unfinished_report = get_unfinished_report()
	if unfinished_report:
		return HttpResponseRedirect('/unfinished/')
	if request.method == 'POST':
		form = StartForm(request.POST)
		if form.is_valid():
			report = Report()
			now = datetime.today()
			report.__dict__.update(fill_count(form, assignee_prefix = 'start_', update = {
				'year': now.year,
				'start_datetime': now,
				'report_id': get_last_report_id() + 1,
				'report_type_id': form.cleaned_data["report_type_id"],
			}))
			report.save()
			return redirect("/%d/" % report.id)
		return render_to_response('zrapport/start.html', {
			'form': form
		}, context_instance = RequestContext(request))
	
	rt = ReportType.objects.all()
	if(len(rt) == 0):
		return HttpResponse('Det finnes ingen rapport-typer, kontakt administrator')
	
	return render_to_response('zrapport/start.html', {
		'form': StartForm(fill_count(rt[0], source_prefix = 'start_', update = {
			'report_type_id': rt[0].id,
		}))
	}, context_instance = RequestContext(request))

def report(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	if report.verified_datetime:
		return HttpResponse('Rapporten er verifisert')
	if report.end_datetime:
		report.update_result_values()
		return render_to_response('zrapport/result.html', {
			'report': report,
			'unfinished_report': get_unfinished_report(),
		}, context_instance = RequestContext(request))
	if report.settle_datetime:
		return HttpResponseRedirect('/%d/result/' % report.id)
	return HttpResponseRedirect('/%d/settle/' % report.id)

def result(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	if request.method == 'POST':
		report.end_datetime = datetime.today()
		report.save()
		return HttpResponseRedirect("/")
	report.update_result_values()
	return render_to_response('zrapport/result.html', {
		'report': report,
		'unfinished_report': get_unfinished_report(),
	}, context_instance = RequestContext(request))

def settle(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	if request.method == 'POST':
		form = SettlementForm(request.POST)
		if form.is_valid():
			report.__dict__.update(fill_settle(form, assignee_prefix = 'end_'))
			report.save()
			return redirect("/%d/" % report.id)
		return render_to_response('zrapport/settle.html', {
			'form': form,
			'unfinished_report': get_unfinished_report(),
			'report': report,
		}, context_instance = RequestContext(request))
	return render_to_response('zrapport/settle.html', {
		'form': SettlementForm(fill_settle(report, source_prefix = 'end_')),
		'unfinished_report': get_unfinished_report(),
		'report': report,
	}, context_instance = RequestContext(request))

def start(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	if request.method == 'POST':
		form = StartForm(request.POST)
		if form.is_valid():
			report.__dict__.update(fill_count(form, assignee_prefix = 'start_', update = {
				'report_type_id': form.cleaned_data['report_type_id']
			}))
			report.save()
			return redirect("/%d/" % report.id)
		return render_to_response('zrapport/start.html', {
			'form': form,
			'unfinished_report': get_unfinished_report(),
			'report': report,
		}, context_instance = RequestContext(request))
	return render_to_response('zrapport/start.html', {
		'form': StartForm(fill_count(report, source_prefix = 'start_', update = {
			'report_type_id': report.report_type_id,
		})),
		'unfinished_report': get_unfinished_report(),
		'report': report,
	}, context_instance = RequestContext(request))

def unfinished(request):
	unfinished_report = get_unfinished_report()
	return render_to_response('zrapport/unfinished.html', {
		'unfinished_report': unfinished_report,
	}, context_instance = RequestContext(request))
