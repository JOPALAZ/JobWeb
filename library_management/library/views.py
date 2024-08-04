from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as django_filters
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class BookFilter(django_filters.FilterSet):
    printed__lte = django_filters.DateFilter(field_name='publish_date', lookup_expr='lte')
    title__contains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['printed__lte', 'title__contains']

class AuthorFilter(django_filters.FilterSet):
    name__contains = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    surname__contains = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    birth__lte = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lte')
    class Meta:
        model = Author
        fields = ['name__contains', 'surname__contains', 'birth__lte']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = AuthorFilter
    search_fields=['first_name', 'last_name']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        if author.books.exists():
            return Response({'error': 'Cannot delete an author with books.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = BookFilter
    search_fields = ['title']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response