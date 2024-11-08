# ITStep Student Work Storage

## Project Description
This project is a website designed for storing student works at ITStep. It allows convenient organization, storage, and management of student submissions, providing centralized access for instructors and students.

## Technologies
- **Backend**: Django (Python)
- **Database**: PostgreSQL

## Requirements
- Python 3.8+
- Django 4.0+
- PostgreSQL

## Installation

1. Clone the repository:
    ```bash
    git clone <https://github.com/Itstepberdichev/student_work.git>
    cd <project_folder_name>
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # for Linux/Mac
    venv\Scripts\activate  # for Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    - Create a PostgreSQL database, e.g., named `student_work_db`.
    - Update the `settings.py` configuration with your database connection details.

5. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser for access to the admin site:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the local server:
    ```bash
    python manage.py runserver
    ```

Open a browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the site.

## Key Features
- Upload and store student work
- Manage access to student submissions
- Interface for instructors and students

## Project Structure
- `student_work/` - main configuration of the Django project
- `student_work/` - application for storing student work
- `templates/` - HTML templates
- `static/` - static files (CSS, JavaScript)

## Authors
This project was created by the ITStep team.

## License
This project is licensed under the MIT License.
