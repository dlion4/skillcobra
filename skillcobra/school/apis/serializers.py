from rest_framework import serializers

from skillcobra.school.models import Category, Course, CourseCurriculum
from skillcobra.school.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]

class CategorySerializer(serializers.ModelSerializer):
    options = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "options",
        ]

class CourseCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculum
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
