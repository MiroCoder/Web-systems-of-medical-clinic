# Web Systems of Medical Clinic

**Web Systems of Medical Clinic** is a Django web application for the medical clinic **Constellation**. It helps patients register, keep their medical information in one place, view doctors' schedules, and manage clinic appointments through a clean web interface.

The project is prepared as a portfolio-ready full-stack Django application with demo patient data, an admin panel, and real interface screenshots displayed directly in this README.

## Preview

### Main Page

![Main Page](screenshots/home.png)

### Patient Profile

![Patient Profile](screenshots/profile.png)

### Appointments

![Appointments](screenshots/appointments.png)

### Schedule

![Schedule](screenshots/schedule.png)

### Django Admin

![Django Admin](screenshots/admin.png)

## What The App Does

### For Patients

- Register and sign in to a personal clinic account.
- View personal profile data and medical record details.
- Check available doctors and clinic schedule.
- Book visits with doctors by date and time.
- Review planned appointments in a personal table.
- Cancel appointments when needed.

### For Administrators

- Manage patients, doctors, appointments, schedules, and medical cards.
- Edit doctor names and specializations.
- Filter visits by patient, doctor, and date.
- Work with all clinic data through the built-in Django Admin panel.

## Demo User

Use this account to explore the prepared patient flow:

```text
Username: Mike
Password: MikeDemo123!
```

The demo profile includes filled patient data, a birth date after 2000, a medical record, and several scheduled appointments.

## Tech Stack

- Python
- Django
- SQLite
- Django Templates
- HTML
- CSS
- Django Admin

## Project Structure

```text
Web-systems-of-medical-clinic/
+-- hospital/
|   +-- hospital/          # Django project settings
|   +-- mainapp/           # Clinic app, models, views, templates, static files
|   +-- db.sqlite3         # Demo database
|   +-- manage.py
+-- screenshots/           # Images rendered in this README
+-- README.md
```

## Getting Started

Clone the repository and enter the Django project folder:

```bash
git clone https://github.com/MiroCoder/Web-systems-of-medical-clinic.git
cd Web-systems-of-medical-clinic/hospital
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install Django:

```bash
pip install django
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/mainapp/
```

## Admin Panel

The Django Admin panel is available here:

```text
http://127.0.0.1:8000/admin/
```

Create a new administrator if needed:

```bash
python manage.py createsuperuser
```

The included demo database also gives **Mike** admin access for quick review.

## Roadmap

- Add stronger appointment validation based on doctor availability.
- Add profile editing for patients.
- Improve doctor cards with photos and working hours.
- Add email notifications for upcoming appointments.
- Cover appointment booking and profile pages with tests.

## Author

Made by [MiroCoder](https://github.com/MiroCoder).
