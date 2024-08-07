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
        if 'date_of_birth' in data and data['date_of_birth'] > datetime.date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        if self.instance is None:
            if Author.objects.filter(first_name=data['first_name'], last_name=data['last_name'], date_of_birth=data['date_of_birth']).exists():
                 raise serializers.ValidationError("An author with this first name, last name and DOB already exists.")
        if self.instance is not None and 'date_of_birth' in data:  # This check is for update scenario
            books = self.instance.books.all()
            for book in books:
                if book.publish_date < data['date_of_birth']:
                    raise serializers.ValidationError(f"Book '{book.title}' was published before the author was born.")
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
        if not data.get('authors'):
            raise serializers.ValidationError({'author': 'This field is required.'})
        if 'publish_date' in data and data['publish_date'] > datetime.date.today():
            raise serializers.ValidationError("Publish date cannot be in the future.")
        authors = data.get('authors', [])
        if authors:
            for author in authors:
                print( author.date_of_birth)
                if data['publish_date'] < author.date_of_birth:
                    raise serializers.ValidationError(f"Publication date cannot be earlier than the birth date of author {author.first_name} {author.last_name}.")
        if self.instance is None:
            if Book.objects.filter(title=data['title'],publish_date=data['publish_date']).exists():
                raise serializers.ValidationError("This book exists")
            if Book.objects.filter( isbn=data['isbn']).exists():
                raise serializers.ValidationError("This ISNB exists")
        else:
            same =  Book.objects.filter( isbn=data['isbn'])
            print(f'{same} {same.contains(self.instance)}')
            if (len(same) > 1 or (len(same) == 1 and not same.contains(self.instance))):
                raise serializers.ValidationError("This ISNB exists")
        return data
