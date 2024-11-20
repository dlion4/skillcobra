from rest_framework import generics  # noqa: I001
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from skillcobra.school.models import Category, SubCategory


from .serializers import CategorySerializer, SubCategorySerializer


class CategoryApiView(
    generics.ListAPIView,
    generics.RetrieveUpdateDestroyAPIView,
):
    """
    API endpoint for retrieving all categories.
    """

    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # Use category_pk here instead of pk
        category_pk = kwargs.get("category_pk")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Use category_pk here instead of pk
        category_pk = kwargs.get("category_pk")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Use category_pk here instead of pk
        category_pk = kwargs.get("category_pk")

        return super().destroy(request, *args, **kwargs)


class SubCategoryModelAPIView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = SubCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SubCategorySerializer

    def create(self, request, *args, **kwargs):
        # Use category_pk and subcategory_pk here
        category_pk = kwargs.get("category_pk")
        subcategory_pk = kwargs.get("subcategory_pk")
        print(f"Category PK: {category_pk}, Subcategory PK: {subcategory_pk}")
        return Response({}, status=status.HTTP_201_CREATED)
