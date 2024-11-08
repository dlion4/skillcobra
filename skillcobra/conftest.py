from pytest_factoryboy import register

from skillcobra.users.models import User
# sourcery skip: dont-import-test-modules
from tests.membership.factories import PlanFactory

register(PlanFactory)
