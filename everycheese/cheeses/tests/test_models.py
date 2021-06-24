import pytest
from ..models import Cheese


# Connects tests with our database
pytestmark = pytest.mark.django_db

def test___str__():
    cheese = Cheese.objects.create(name='Stracchio', description='Semi-sweet cheese that stretches good', firmness=Cheese.Firmness.SOFT)
    assert cheese.__str__() == 'Stracchio'
    assert str(cheese) == 'Stracchio'