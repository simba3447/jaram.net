from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime, date
from django.views.generic import TemplateView
from main.util import create_response
import calendar

from schedule.models import Event


class ScheduleView(TemplateView):
    template_name = 'schedule/calendar.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        today = date.today()
        year = today.year
        month = today.month
        calendar.setfirstweekday(calendar.SUNDAY)
        response['new_calendar'] = calendar.monthcalendar(year, month)
        response['events'] = Event.objects.filter(
            start_date__range=(
                datetime(year, month, 1), datetime(year, month, calendar.monthrange(year, month)[1]))).order_by(
            '-start_date')
        return render(request, self.template_name, response)


class ScheduleDetailView(TemplateView):
    template_name = 'schedule/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        try:
            event = Event.objects.get(eng_name=kwargs.get('name'))
        except ObjectDoesNotExist:
            return redirect('/main/?warning=잘못된 접근입니다.')
        return render(request, self.template_name, response)
