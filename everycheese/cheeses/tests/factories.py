from django.db import models
from django.template.defaultfilters import slugify
from ..models import Cheese
import factory
import factory.fuzzy


class CheeseFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker('paragraph', nb_sentences = 3, variable_nb_sentences=True)
    firmness = factory.fuzzy.FuzzyChoice([x[0] for x in Cheese.Firmness.choices])

    class Meta:
        model = Cheese