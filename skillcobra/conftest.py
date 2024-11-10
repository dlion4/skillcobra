from pytest_factoryboy import register

from tests.membership.factories import PlanFactory  # Adjust the import if necessary

# Register the PlanFactory so it can be used as a fixture
register(PlanFactory)
