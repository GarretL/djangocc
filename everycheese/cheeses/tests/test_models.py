from ..models import Cheese
from .factories import CheeseFactory
import pytest
#Connects
pytestmark = pytest.mark.django_db

def test___str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name
    
