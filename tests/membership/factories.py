import factory

from skillcobra.payments.models import MemberShip
from skillcobra.payments.models import Plan
from skillcobra.payments.models import PlanFeature


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan
    name = factory.Faker("en_US")
