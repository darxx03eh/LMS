# 🎓 Online Learning Management System (LMS) API
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) 
[![Django REST](https://img.shields.io/badge/Django%20REST-FF1709?style=for-the-badge&logo=django&logoColor=white/)](https://www.djangorest.com/)
[![LMS](https://img.shields.io/badge/LMS-FF6600?style=for-the-badge&logo=LMS&logoColor=white)](https://LMS.org/)

---

## ✨ Overview

This project is a RESTful API for an Online Learning Management System (LMS) built with Django REST Framework.
It provides a structured platform where instructors can create and manage courses, while students can enroll, learn, and track their progress. 
The system also includes reviews, ratings, and search features to enhance the learning experience.

---

## 🔑 Key Features

- User Roles: Admin, Instructor, Student with JWT authentication.
- Courses: Instructors create/manage; students browse and view.
- Lessons & Materials: Video/PDF uploads, accessible only to enrolled students.
- Enrollment & Progress: Track lessons completed and course completion %.
- Reviews & Ratings: Students leave 1–5 star reviews with comments.
- Search & Filters: Search courses, filter by category/instructor/rating, with pagination.
- Permissions: Instructors manage their own content; admins have full control.

---

## 🧱 Tech Stack

| Layer          | Technology                                            |
|----------------|-------------------------------------------------------|
| Backend        | Django & Django REST                                  |
| ORM            | Django ORM                                            |
| Database       | PostgreSQL                                            |
| Auth           | JWT Bearer Authentication                             |
| Object Mapping | Serializers                                           |
| Validation     | Serializers perform validation ```validate_<field>``` |
| Logging        | Python Logging / Django Logging Configuration         |
| Filtering      | Django-filter                                         |
| Storage        | Cloudinary & Local                                    |
| Testing        | Django Test Framework / DRF APITestCase               |

---

## 🚀 Running the App
1.	**Clone the repository**:
	```bash
	git clone https://github.com/darxx03eh/LMS.git
	cd LMS
	```
	
2.	**install virtualenv in you'r device**:
	```bash
	pip install virtualenv
	```

3.	**Create virtualenv into project**:
	```bash
	virtualenv venv
	```
	
4.	**Run the virtualenv**:
	```bash
	.\venv\Scripts\activate
	```
	
5.	**install packages from requirements.txt**:
	```bash
	pip install -r requirements.txt
	```
   
6.	**Create .env file**:
7.	**Add you'r own env**:
	```
	# DATABASE SETTINGS
	DB_NAME=DB_NAME
	DB_USER=DB_USER
	DB_PASSWORD=DB_PASSWORD
	DB_HOST=DB_HOST
	DB_PORT=DB_PORT

	# JWT SETTINGS
	JWT_SIGNING_KEY=JWT_SIGNING_KEY
	JWT_AUDIENCE=lms-JWT_AUDIENCE
	JWT_ISSUER=lms-JWT_ISSUER

	# Cloudinary Settings
	CLOUD_NAME=CLOUD_NAME
	CLOUD_API_KEY=CLOUD_API_KEY
	CLOUD_API_SECRET=CLOUD_API_SECRET
	
	# Loggin settings
	LOG_LEVEL=LOG_LEVEL
	LOG_FILE=FILE.log
	LOG_FILE_CONTROLLERS=FILE_CONTROLLERS.log
	```

8.	**Apply Migrations**:
	```bash
	py .\manage.py makemigrations
	```
	then 
	```bash 
	py .\manage.py migrate
	```
	
9.	**Run the project**:
	```bash
	py .\manage.py runserver <port>
	```
	
10.	**Browse to Swagger UI**:
	```
	http://localhost:<port>/api/schema/swagger-ui
	```
	
---

## 🧪 Running Tests

To run tests
```bash
py .\manage.py test
```
---

## 📚 API Documentation

after running the project, navigate to
```
http://localhost:<port>/api/schema/swagger-ui
```
to enable Swagger UI

---

**Auth**

| HTTP Method | Endpoint               | Description                                                   |
|-------------|------------------------|---------------------------------------------------------------|
| POST        | /api/v1/login          | enter to you'r account                                        |
| POST        | /api/v1/signup         | register a new user such as instructor or student             |
| POST        | /api/v1/logout         | exit from you'r account                                       |

**Users**

| HTTP Method | Endpoint               | Description                                                   |
|-------------|------------------------|---------------------------------------------------------------|
| GET         | /api/v1/users          | show you'r account details                                    |
| PATCH       | /api/v1/users          | update you'r account information such as email, phone_number  |

**Courses**

| HTTP Method | Endpoint                             | Description                                                                                                                 |
|-------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| GET         | /api/v1/courses                      | show you'r courses if you'r an instructor, you'r enrolled courses if you'r a student and all courses if you'r an admin      | 
| POST        | /api/v1/courses                      | add courses if you'r instructor or admin                                                                                    |
| GET         | /api/v1/courses/{id}                 | show a specific course if you'r an instructor, you'r specific enrolled course if you'r a student, admin can show any course |
| PUT         | /api/v1/courses/{id}                 | update you'r own course, admin can update any course                                                                        |
| DELETE      | /api/v1/courses/{id}                 | delete you'r own course, admin can delete any course                                                                        |
| POST        | /api/v1/courses/{id}/enroll          | for students only to enroll any course they want                                                                            |
| GET         | /api/v1/courses/{id}/feedbacks       | to view all feedbacks linked to specific course, instructor can view feedbacks for his course, admin can any course         |                    
| GET         | /api/v1/courses/{id}/progress        | to show you'r progress in any course                                                                                        |
| GET         | /api/v1/courses?search=              | to search for courses using eaither title or description                                                                    |
| GET         | /api/v1/courses?instructor=          | to filter courses by specific instructor                                                                                    |
| GET         | /api/v1/courses?category__icontains= | to filter courses by category contains written ignoring case                                                                |
| GET         | /api/v1/courses?category__iexact=    | to filter courses by category but exact name ignoring case                                                                  |
| GET         | /api/v1/courses?page=                | enter the page number to view more courses (pagination)                                                                     |
| GET         | /api/v1/courses?rate__gte            | to filter courses by rating greater than or equal                                                                           |
| GET         | /api/v1/courses?rate__lte            | to filter courses by rating less than or equal                                                                              |

**Lessons**

| HTTP Method | Endpoint                            | Description                                                                                                                                        |
|-------------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| GET         | /api/v1/lessons                     | show you'r course's lessons if you'r an instructor, you'r enrolled course's lessons if you'r a student and all courses's lessons if you'r an admin | 
| GET         | /api/v1/course/{id}/lessons         | view a specific own course's lessons for an instructor, a specific enrolled course's lessons for a student, any lessons for admin                  |
| POST        | /api/v1/lessons/                    | create a new lesson for own course if you'r an instructor, admin can create lessons for any course                                                 |
| GET         | /api/v1/lessons/{id}                | view specific lesson                                                                                                                               |
| PUT         | /api/v1/courses/{id}                | update an exis lesson for own specific lesson for an instructor, admin can update any lesson                                                       |
| DELETE      | /api/v1/courses/{id}                | delete you'r own lesson if you'r an instructor, admin can delete any lessons                                                                       |
| POST        | /api/v1/lessons/{id}/mark_completed | students can mark lesson as completed only for enrolled courses                                                                                    |

**Feedbacks**

| HTTP Method | Endpoint                   | Description                                                                        |
|-------------|----------------------------|------------------------------------------------------------------------------------|
| POST        | /api/v1/courses/feedbacks  | student can add only one feedback cotains rate and comment for any enrolled course | 
| GET         | /api/v1/feedbacks          | view you'r own feedbacks, admin can view all feedbacks from any student            |
| GET         | /api/v1/feedbacks/{id}     | view specific feedback                                                             |
| PUT         | /api/v1/feedbacks/{id}     | update you'r own feedback                                                          |
| DELETE      | /api/v1/courses/{id}       | delete you'r own feedback                                                          |

---

## 🗂 Folder Structure

```
LMS/
├── api/									# Main API app
│	├── migrations 
│	├── models								# Database models (ORM)
│	│	├── __init__.py
│	│	├── completed_lesson.py
│	│	├── course.py
│	│	├── enrollment.py
│	│	├── feedback.py
│	│	├── lesson.py
│	│	├── time_stamped_mix_in.py
│	│	├── user.py
│	├── serializers							# Handle JSON conversion & validation
│	│	├──__init__.py
│	│	├── auth_serializers.py
│	│	├── course_serializers.py
│	│	├── feedback_serializers.py
│	│	├── lessons_serializers.py
│	│	├── user_serializers.py
│	├── services							# Business logic layer
│	│	├── __init__.py
│	│	├── course_servicees
│	├── tests								# Test directory
│	│	├── helpers/		
│	│	│	├── __init__.py
│	│	│	├── helpers.py
│	│	├── __init__.py
│	│	├── auth_tests.py
│	│	├── course_tests.py
│	│	├── feedback_tests.py
│	│	├── lesson_tests.py
│	│	├── user_tests.py
│	├── views								# "Controllers" in Django terms
│	│	├── __init__.py
│	│	├── auth_views.py					# Auth-related endpoints
│	│	├── course_views.py					# Course-related endpoints
│	│	├── feedback_views.py				# Feedback-related endpoints
│	│	├── lessons_views.py				# Lesson-related endpoints
│	│	├── user_views.py					# User-related endpoints
│	├── __init__.py
│	├── admin.py							# Register the models and others into admin dashboard
│	├── apps.py
│	├── urls.py								# API-specific URL routing
├── LMS/
│	├── __init__.py
│	├── asgi.py								# ASGI config for deployment
│	├── settings.py							# Project settings
│	├── urls.py								# Project-level URL routing
│	├── wsgi.py								# WSGI config for deployment
├── media/
│	├── lessons/
│	│	├── docs/							# Docs like pdf
│	│	├── videos/							# Videos
├── utails/									# Shared utilities and helpers
│	├── __init__.py
│	├── custom_permissions.py				# Custom permissions
│	├── exception_handler.py				# Exception handler
│	├── filters.py							# Filters
│	├── response_middleware.py				# Response middleware
├── venv/									# Virtual Environment
├── .env									# Environment variables (not in version control)
├── .gitignore
├── controllers.log							# logging controllers actions
├── docker-compose-yml						# Docker compose
├── Dockerfile								# Docker file
├── general.log								# logging general actions
├── manage.py								# Django's command-line utility
├── README.md
├── requirements.txt						# Project dependencies
```

---

## 🔒 Authentication & Authorization
- Uses **JWT Tokens**
- Supports roles: `Admin`, `Instructor`, `Student`
- Role-based access via `permission_class`

---

## Database Schema
Below is the Entity-Relationship Diagram (ERD) illustrating the structure of the database, including tables, relationships, and keys used in the application.

![ERD Diagram](ERD/LMS.png)


## 👨🏻‍💻 Author

Built by ```Mahmoud Darawsheh - darxx03eh```  
Backend training by ASAL Technologies

---

## 📜 License

This project is licensed under the MIT License.

