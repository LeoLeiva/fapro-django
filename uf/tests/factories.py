import factory
from faker import Factory

from uf.models import ValuesUF

faker = Factory.create()


class ValuesUFFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ValuesUF

    date = factory.LazyAttribute(lambda _: faker.date(pattern="%Y-%m-%d"))
    value = factory.LazyAttribute(lambda _: faker.numerify(text='#####.##'))
