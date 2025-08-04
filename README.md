# Blog_post_-API
RUN APPLICATION : python manage.py runserver
API END POINT = http://127.0.0.1:8000/api/



Architecture & Tools Used:

Backend Framework: Django 

API :Django REST Framework 

Authentication: Token Authentication for API protection

Database: SQLite


Components:

1. Admin Interface (Part 1)

Used Django Admin to provide full CRUD functionality for blog posts.

2. REST API (Part 2)

Built with Django REST Framework:

GET /api/blogs/ – Lists all published blogs

GET /api/blogs/<id>/ – Fetches a single blog post by ID

Applied @api_view, TokenAuthentication, and IsAuthenticated for secure access

Validated request/response with DRF serializers

3. API Consumer Interface (Part 3)

Created a Django view  Python requests to call /api/blogs/ and /api/blogs/<id>/.


This strictly avoids using Django ORM directly for blog display.
