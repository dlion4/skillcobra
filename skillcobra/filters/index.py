import django_filters as filters
from django.db import models
from django_filters import FilterSet

from skillcobra.school.models import Course


class CourseFilter(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Course
        fields = ["title"]
        # filter_overrides = {
        #     models.CharField : {
        #         "filter_class": filters.CharFilter,
        #         "extra": lambda f: {
        #             "lookup_expr": "icontains",
        #         },
        #     },
        # }
    # @property
    # def qs(self):
    #     parent = super().qs
    #     print("parent: ", parent)
    #     print("student: ", self.request)
    #     return parent.filter(title=self.title)


