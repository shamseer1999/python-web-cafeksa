import factory
from faker import Faker
from django.contrib.auth.models import User
from .models import Product

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.Faker("name")
    description = factory.Faker("sentence",nb_words = 2)
    created_by = User.objects.get_or_create(username = "admin")[0]