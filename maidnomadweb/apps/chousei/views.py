from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction

from .models import Event, EventDate, EventPerson, Schedule
from .forms import generate_chousei_form_class
from .choises import SCHEDULE_CHOISE


def _get_event_info(key: str):
    event = get_object_or_404(Event, key=key)
    event_dates = event.eventdate_set.all().order_by(
        "start_datetime",
    )
    return event, event_dates


def view(request: HttpRequest, key: str):
    event, event_dates = _get_event_info(key)
    event_people = event.eventperson_set.all()
    schedules = Schedule.objects.filter(
        event_person__event = event,
    )
    answer_dict = {
        (schedule.event_person.pk, schedule.event_date.pk): schedule.answer
        for schedule in schedules
    }
    event_date_answer = [
        {
            "start_datetime": event_date.start_datetime,
            "answers": [
                dict(SCHEDULE_CHOISE).get(
                    answer_dict.get((event_person.pk, event_date.pk)),
                    ""
                )
                for event_person in event_people
            ]
        }
        for event_date in event_dates
    ]
    return render(
        request,
        "chousei/view.html",
        {
            "event": event,
            "event_date_answer": event_date_answer,
            "event_people": event_people,
        },
    )


def add(request: HttpRequest, key: str):
    event, event_dates = _get_event_info(key)
    ChouseiForm = generate_chousei_form_class(
        [event_date.pk for event_date in event_dates]
    )
    if request.method == "POST":
        form = ChouseiForm(data=request.POST)
        if form.is_valid():
            form.instance.event = event
            with transaction.atomic():
                form.save()
                for event_dates_field in form.eventdate_fields():
                    eventdate_id = int(event_dates_field.name.split("_")[1])
                    value = form.cleaned_data[event_dates_field.name]
                    schedule = Schedule(event_person=form.instance, event_date_id=eventdate_id, answer=value)
                    schedule.save()
                return redirect("chousei:view", key)
    else:
        form = ChouseiForm()
    return render(
        request,
        "chousei/edit.html",
        {
            "event": event,
            "event_dates": event_dates,
            "form": form,
            "is_add": True,
        },
    )


def edit(request: HttpRequest, key: str, person_id: int):
    event, event_dates = _get_event_info(key)
    ChouseiForm = generate_chousei_form_class(
        [event_date.pk for event_date in event_dates]
    )
    person = get_object_or_404(EventPerson, event=event, pk=person_id)
    if request.method == "POST":
        form = ChouseiForm(instance=person, data=request.POST)
        if form.is_valid():
            form.instance.event = event
            form.instance.pk = person_id
            with transaction.atomic():
                form.save()
                for event_dates_field in form.eventdate_fields():
                    eventdate_id = int(event_dates_field.name.split("_")[1])
                    value = form.cleaned_data[event_dates_field.name]
                    try:
                        schedule = Schedule.objects.get(event_person=form.instance, event_date_id=eventdate_id)
                    except Schedule.DoesNotExist:
                        schedule = Schedule(event_person=form.instance, event_date_id=eventdate_id)
                    schedule.answer = value
                    schedule.save()
                return redirect("chousei:view", key)
            return redirect("chousei:view", key)
    else:
        form = ChouseiForm(instance=person)
        schedules = person.schedule_set.all()
        for schedule in schedules:
            field = form.fields.get(f"eventdate_{schedule.event_date_id}")
            field.initial = schedule.answer
    
    return render(
        request,
        "chousei/edit.html",
        {
            "event": event,
            "event_dates": event_dates,
            "form": form,
            "person": person,
            "is_add": False,
        },
    )
