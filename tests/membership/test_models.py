import pytest

pytestmark = pytest.mark.django_db

class TestPlanModel:
    def test_plan_output_string(self, plan_factory):
        plan = plan_factory()
        assert isinstance(plan.__str__(), str)

# class TestMembershipModel:
#     def test_membership_output_string(self): ...

# class PlanFeatureMode:
#     def test_plan_feature_mode_output_string(self): ...
