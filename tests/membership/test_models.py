import pytest

# Apply the Django database mark for the entire test class
pytestmark = pytest.mark.django_db


class TestPlanModel:
    def test_plan_output_string(self, plan_factory):
        # Use the factory's create method to instantiate the object
        plan = (
            plan_factory.create()
        )  # or plan_factory.build() if you don't need to save it to the DB

        # Now perform your assertions
        assert isinstance(plan.__str__(), str)


# class TestMembershipModel:
#     def test_membership_output_string(self): ...

# class PlanFeatureMode:
#     def test_plan_feature_mode_output_string(self): ...
