from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Author, Book
import datetime

class AuthorTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='name', password='pass')
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1970-01-01'
        )
        self.url = '/api/authors/'

    def test_list_authors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_duplicate(self):
        data = {'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '1970-01-01'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author(self):
        data = {'first_name': 'Jane', 'last_name': 'Smith', 'date_of_birth': '1980-05-05'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_update_author(self):
        data = {'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '1981-01-01'}
        response = self.client.put(f'{self.url}{self.author.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.date_of_birth, datetime.date(1981, 1, 1))

    def test_delete_author(self):
        response = self.client.delete(f'{self.url}{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_retrieve_author(self):
        response = self.client.get(f'{self.url}{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_create_author_with_missing_first_name(self):
        data = {'last_name': 'Doe', 'date_of_birth': '1970-01-01'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author_with_invalid_date_of_birth(self):
        data = {'first_name': 'Jane', 'last_name': 'Smith', 'date_of_birth': 'invalid-date'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='name', password='pass')
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1970-01-01'
        )
        self.author1 = Author.objects.create(
            first_name='John1',
            last_name='Doe1',
            date_of_birth='1970-01-01'
        )
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publish_date='2024-01-01'
        )
        self.book.authors.add(self.author)
        self.book.authors.add(self.author1)
        self.url = '/api/books/'

    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'isbn': '9876543210123',
            'publish_date': '2024-05-05',
            'authors': [self.author.id, self.author1.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_duplicate_book(self):
        data = {
            'title': 'Test Book',
            'isbn': '1234567890123',
            'publish_date': '2024-01-01',
            'authors': [self.author.id, self.author1.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)

    def test_update_book(self):
        data = {
            'title': 'Updated Book',
            'isbn': '1234567890123',
            'publish_date': '2024-06-06',
            'authors': [self.author.id]
        }
        response = self.client.put(f'{self.url}{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.authors.count(), 1)

    def test_delete_book(self):
        response = self.client.delete(f'{self.url}{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_retrieve_book(self):
        response = self.client.get(f'{self.url}{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_create_book_with_missing_title(self):
        data = {
            'isbn': '9876543210123',
            'publish_date': '2024-05-05',
            'authors': [self.author.id, self.author1.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_invalid_publish_date(self):
        data = {
            'title': 'Invalid Date Book',
            'isbn': '9876543210123',
            'publish_date': 'invalid-date',
            'authors': [self.author.id, self.author1.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_missing_authors(self):
        data = {
            'title': 'No Authors Book',
            'isbn': '9876543210123',
            'publish_date': '2024-05-05',
            'authors': []
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)