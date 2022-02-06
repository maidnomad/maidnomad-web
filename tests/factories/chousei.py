import factory
import factory.fuzzy
from apps.chousei import choises, models


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    key = factory.fuzzy.FuzzyText(length=32)
    event_name = factory.Sequence(lambda n: f"ダミーイベント #{n}")
    memo = ""


class EventDateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventDate


class EventPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventPerson

    comment = ""


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Schedule

    answer = factory.fuzzy.FuzzyChoice(
        choices=[k for k, _ in choises.SCHEDULE_ANSWER_CHOISE]
    )
