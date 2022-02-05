from random import choice
from django import forms

from .choises import SCHEDULE_CHOISE
from .models import EventPerson


class EventPersonForm(forms.ModelForm):
    class Meta:
        model = EventPerson
        fields = ["name", "comment"]

def generate_chousei_form_class(event_date_ids: list[int]):
    new_fieldnames = [
        f"eventdate_{event_date_id}" for event_date_id in event_date_ids
    ]
    new_fields = {
        field_name: forms.ChoiceField(
            choices=SCHEDULE_CHOISE,
            widget=forms.widgets.RadioSelect
        )
        for field_name in new_fieldnames
    }
    ChouseiForm = type('ChouseiForm', (EventPersonForm,), new_fields)
    def eventdate_fields(self):
        return [
            self[field_name] for field_name in new_fieldnames
        ]
    ChouseiForm.eventdate_fields = eventdate_fields
    return ChouseiForm
    

