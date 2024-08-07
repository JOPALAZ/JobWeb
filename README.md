# Library Management Application

This project is a simple library management application that allows users to manage books and authors. The application includes the following features:

## Features

### GUI + API showcase:
https://github.com/user-attachments/assets/d8ec7a0b-a82a-40a5-9d4c-61d0b18d0bc8


### Author Management:
- Add a new author (first name, last name, date of birth).
- View a list of all authors.
- Edit an author.
- Delete an author.

### Book Management:
- Add a new book (title, ISBN, publication date, authors (0-N)).
- View a list of all books.
- Edit a book.
- Delete a book.

## Project Structure

### Backend:
- Created a REST API using Django 4.x and Django Rest Framework (DRF) to allow CRUD operations for books and authors.
- Models in Django for authors and books are related.
- Input data validation is implemented.

### Frontend:
- QUASAR simple GUI with authentication (login).

### Tests:
- Basic tests for individual API endpoints are created using the Django testing framework.

### Bonus Features Implemented:
- Filtering and searching for books and authors using Django lookups (e.g., `/api/books?printed__lte=2030-06-24&title__contains=Book`) and pagination for lists.
- Simple GUI in Quasar.
- Authentication and authorization using tokens. Only logged-in users can add and edit books and authors (user management is done using Django Admin).

## Installation and Running

### Requirements:
- Docker
- Docker Compose

### Steps to Run:
1. Clone the repository:
   ```bash
   git clone https://github.com/JOPALAZ/JobWeb.git
   cd JobWeb
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. After the containers are up and running, the backend API will be available at `http://localhost:8000`, and the frontend will be available at `http://localhost:8080`.

## API Endpoints

### Authors:
- **Add Author**: `POST /api/authors/`
- **View All Authors**: `GET /api/authors/`
- **Edit Author**: `PUT /api/authors/{id}/`
- **Delete Author**: `DELETE /api/authors/{id}/`

### Books:
- **Add Book**: `POST /api/books/`
- **View All Books**: `GET /api/books/`
- **Edit Book**: `PUT /api/books/{id}/`
- **Delete Book**: `DELETE /api/books/{id}/`

### Authentication:
- **Login**: Can be done using page `http://localhost:8080/#/login` with username is `name` and password is `pass`. Also Token can be obtained via request with those cridentials to POST /api/api-token-auth

## Filtering and Pagination:
- Example for filtering books by publication date and title:
  ```bash
  GET /api/books?printed__lte=2030-06-24&title__contains=Book
  ```

- Example for pagination:
  ```bash
  GET /api/books?page=2
  ```

---

This project provides a basic library management system with additional features for filtering, searching, and user authentication, making it a comprehensive example of a Django-based REST API.
