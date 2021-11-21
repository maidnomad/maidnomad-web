import factory
import factory.fuzzy
from apps.maidlist import models as maidlist_models


class MaidProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = maidlist_models.MaidProfile

    code = factory.Sequence(lambda n: f"maid_{n}")
    name = factory.Sequence(lambda n: f"メイドさん {n}号")
    content = factory.fuzzy.FuzzyText()
    main_image = factory.django.ImageField()
    thumbnail_image = factory.django.ImageField()
