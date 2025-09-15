import factory
from faker import Faker

fake = Faker()

class URLFactory(factory.Factory):
    class Meta:
        model = dict

    url = factory.LazyFunction(lambda: fake.url())