from django.forms import Textarea


class TextAreaWithDatepickerWidget(Textarea):
    template_name = 'chousei/forms/widgets/textarea_with_datepicker.html'
