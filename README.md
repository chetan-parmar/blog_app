# Django Blog Application

## Project Overview

This is a Django-based blog application that includes user authentication, post creation, post categorization, commenting, and a responsive user interface styled with TailwindCSS. The application supports user registration and login, profile management, and dynamic home page views with filtering and search functionality.

## Features

- User Authentication: Registration, login, and profile management.
- Blog Post Management: Create, edit, and view blog posts.
- Categorization: Blog posts can be categorized.
- Comments: Basic commenting system for blog posts.
- Pagination: Dynamic home page with pagination, filtering, and search.
- Responsive Design: Styled with TailwindCSS.
- Docker Support: Docker and Docker Compose setup for easy deployment.
- Unit Tests: Test cases for critical functionalities.

## Setup Instructions

### Prerequisites

- Python 3.9 or later
- Node.js and npm (for TailwindCSS)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/nishantdevlpr92/blogger
    ```

2. Navigate to the project directory:
    ```sh
    cd blogger
    ```

3. Set up your Python environment and install dependencies:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

4.  Make .env file in your repository
    ```sh
    cp .env .env.example
    ```

5. Apply database migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Start the development server:
    ```sh
    python manage.py runserver
    ```

7. Run tests to ensure everything is working:
    ```sh
    python manage.py test blog.tests
    ```
