import datetime
from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'date_of_birth']

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must only contain alphabetic characters.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must only contain alphabetic characters.")
        return value

    def validate(self, data):
        if 'first_name' in data and 'last_name' in data:
            if data['first_name'] == data['last_name']:
                raise serializers.ValidationError("First name and last name cannot be the same.")
        if self.instance is None:
            if Author.objects.filter(first_name=data['first_name'], last_name=data['last_name'], date_of_birth=data['date_of_birth']).exists():
                 raise serializers.ValidationError("An author with this first name, last name and DOB already exists.")
        return data

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'publish_date', 'authors']

    def validate_isbn(self, value):
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long.")
        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only numeric characters.")
        return value

    def validate(self, data):
        if 'publish_date' in data and data['publish_date'] > datetime.date.today():
            raise serializers.ValidationError("Publish date cannot be in the future.")
        if self.instance is None:
            if Book.objects.filter(title=data['title'], isbn=data['isbn'], publish_date=data['publish_date']).exists():
                raise serializers.ValidationError("This book exists")
        return data
