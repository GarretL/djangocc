import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse
from django.contrib.sessions.middleware \
    import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView,
    CheeseUpdateView
)
from .factories import CheeseFactory, cheese

pytestmark = pytest.mark.django_db

def test_good_cheese_list_view_expanded(rf):
    #Determine the URL, rf is shorthand for request Factory
    url = reverse("cheeses:list")
    #Generate a request as if from a user accessing the 
    #Cheese list view
    request = rf.get(url)
    #Call as_view() to make a callable bect
    #callable_obj is analagous to a function based view
    callable_obj = CheeseListView.as_view()
    #Pass in the request into the callable_obj to get an
    #HTTP response by Django
    response = callable_obj(request)
    #Test that the HTTP response has 'Cheese List'
    #in the HTML and has a 200 response code
    #AssertContains explicitly checks respose_code=200
    assertContains(response, 'Cheese List')

def test_good_cheese_list_view(rf):
    #'Get the request'
    request = rf.get(reverse("cheeses:list"))
    #Use the reques to get the response
    response = CheeseListView.as_view()(request)
    #Tet that the response is valid
    assertContains(response, 'Cheese List')

def test_good_cheese_details_view(rf):
    #Create some cheese
    cheese = CheeseFactory()
    # Make a request for our new cheese
    url = reverse("cheeses:detail",
    kwargs={'slug': cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)

def test_good_cheese_create_view(rf, admin_user):
    cheese = CheeseFactory()
    request = rf.get(reverse("cheeses:add"))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assert response.status_code == 200

def test_cheese_list_contains_2_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)

def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()
    url = reverse("cheeses:detail",
    kwargs={'slug': cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)

def test_cheese_create_form_valid(rf, admin_user):
    form_data = {
        "name": "Paski Sir",
        "description": "A Salty hard cheese",
        "firmness": Cheese.Firmness.HARD
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    cheese = Cheese.objects.get(name="Paski Sir")

    assert cheese.description == "A Salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user

def test_cheese_create_correct_title(rf, admin_user):
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')
    
def test_good_cheese_update_view(rf, admin_user, cheese):
    url = reverse("cheeses:update",
    kwargs={'slug': cheese.slug})
    request = rf.get(url)
    request.user = admin_user
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response,"Update Cheese")

def test_cheese_update(rf, admin_user, cheese):
    form_data = {
        'name': cheese.name,
        'description': 'Something new',
        'firmness': cheese.firmness
    }
    url = reverse("cheeses:update",
    kwargs={'slug': cheese.slug})
    request = rf.post(url, form_data)
    request.user = admin_user
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)

    cheese.refresh_from_db()
    assert cheese.description == 'Something new'


