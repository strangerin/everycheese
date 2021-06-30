from .factories import CheeseFactory, cheese
from django.http import request, response
import pytest 
from pytest_django.asserts import ( 
    assertContains, 
    assertRedirects 
    ) 
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory 
from everycheese.users.models import User 
from ..models import Cheese 
from ..views import ( 
    CheeseCreateView, 
    CheeseListView, 
    CheeseDetailView,
    CheeseUpdateView 
    ) 

pytestmark = pytest.mark.django_db

# NOTE do not remove the expnaded version of the first test - it is needed for the future reference
def test_good_cheese_list_view_expanded(rf):
    # Determine the URL
    url = reverse("cheeses:list")
    # rf - pytest shortcut to the request factory
    request = rf.get(url)
    # call as_view() to get an HTTP response served by Django
    callable_obj = CheeseListView.as_view()
    response = callable_obj(request)
    # test that HTTP response has Cheese list in the HTML and has a 200 response code
    assertContains(response, 'Cheese List')


def test_good_cheese_list_view(rf):
    # Get Request
    request = rf.get(reverse("cheeses:list"))
    # Use the request to get the response
    response = CheeseListView.as_view()(request)
    # validate the response
    assertContains(response, "Cheese List")


def test_cheese_list_contains_2_cheeses(rf):
    # couple of objects to work with
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # create request for a list
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    # assert that response contains both cheese names in the template
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)    


def test_good_cheese_detail_view(rf, cheese):
    # make a request for a new cheese
    url = reverse('cheeses:detail', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # use request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug = cheese.slug)
    # validate the response
    assertContains(response,cheese.name)


def  test_contains_cheese_data(rf, cheese):
    # make a request for a new cheese
    url = reverse('cheeses:detail', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # use request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug = cheese.slug)
    # validate the response
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_good_cheese_create_view(rf, admin_user):
    # request for a new cheese
    request = rf.get(reverse("cheeses:add"))
    # add authenticated user
    request.user = admin_user
    # aaaaaand get the response
    response = CheeseCreateView.as_view()(request)
    # validate the response
    assert response.status_code == 200

def test_cheese_create_form_valid(rf, admin_user):
    # Submit the cheese add form
    form_data = {
        'name': "Paski Sir",
        'description': 'A salty hard Cheese',
        'firmness': Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    # Get the cheese based on name
    cheese = Cheese.objects.get(name='Paski Sir')
    # Test that the cheese matches our form
    assert cheese.description == 'A salty hard Cheese'
    assert cheese.firmness ==  Cheese.Firmness.HARD
    assert cheese.creator == admin_user


def test_cheese_create_title(rf, admin_user):
    """Test title for cheese create view"""
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')


def test_cheese_update_view(rf, admin_user, cheese):
    url = reverse("cheeses:update",
        kwargs={'slug':cheese.slug})
    # Make request for a new cheese
    request = rf.get(url)
    # Add on authenticated user
    request.user = admin_user
    # get da response
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # validate the response
    assertContains(response, "Update Cheese")


def test_cheese_update(rf, admin_user, cheese):
    """POST request to CheeseUpdateview updates a cheese and redirect"""
    form_data = {
        'name': cheese.name,
        'description': "Something new",
        'firmness': cheese.firmness
    }

    url = reverse("cheeses:update", kwargs={"slug": cheese.slug})
    request = rf.post(url, form_data)
    request.user = admin_user
    callable_obj = CheeseUpdateView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Check that the cheese has been modified
    cheese.refresh_from_db()
    assert cheese.description == 'Something new'