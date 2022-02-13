import factory
import factory.fuzzy
from apps.organizerlist import models


class OrganizerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrganizerProfile

    code = factory.Sequence(lambda n: f"org_{n}")
    name = factory.Sequence(lambda n: f"オーガナイザー {n}号")
    content = factory.fuzzy.FuzzyText()
    main_image = factory.django.ImageField()
    thumbnail_image = factory.django.ImageField()
    og_image = factory.django.ImageField()
