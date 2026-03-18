# ⚡ EventHub — Django Event Management System

![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> A clean, full-featured **Event Management Web App** built with Django 4.2 and Python 3.11.  
> Create events, manage registrations, track attendees — all in one place.

---

## 📸 Screenshots

| Home Page | Event Detail | My Events |
|-----------|-------------|-----------|
| Browse & filter events | Register with seat tracker | Organizer dashboard |
<img width="1920" height="1200" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/10e62199-3372-4fa9-bdff-ad7ac9cfdb74" />

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Register, Login, Logout using Django's built-in auth |
| 🎉 **Event CRUD** | Create, Edit, Delete events with image upload |
| 🔍 **Search & Filter** | Filter by keyword, category, and status |
| 🎟️ **Registration** | Register / cancel with live seat tracking |
| 📊 **My Dashboard** | View events you organized and events you're attending |
| 👥 **Attendee List** | Organizers can view full attendee list |
| 🏷️ **Categories** | Color-coded event categories |
| 🛠️ **Admin Panel** | Django admin pre-configured for all models |

---

## 🗂️ Project Structure

```
event_management/
├── event_management/           # Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/                     # Main application
│   ├── migrations/
│   ├── templates/
│   │   └── events/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── event_detail.html
│   │       ├── event_form.html
│   │       ├── event_confirm_delete.html
│   │       ├── attendees.html
│   │       ├── my_events.html
│   │       ├── login.html
│   │       └── register.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/
│   └── event_images/           # Uploaded event images
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11.9
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/event-management.git
cd event-management
```

**2. Create and activate a virtual environment**

```bash
# Linux / Mac
python3.11 -m venv venv
source venv/bin/activate

# Windows
python3.11 -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a superuser**

```bash
python manage.py createsuperuser
```

**6. (Optional) Seed sample categories**

```bash
python manage.py shell
```

```python
from events.models import Category

categories = [
    ('Technology',  '#7c3aed'),
    ('Music',       '#ec4899'),
    ('Sports',      '#10b981'),
    ('Business',    '#3b82f6'),
    ('Art & Culture','#f59e0b'),
    ('Food & Drink','#ef4444'),
]
for name, color in categories:
    Category.objects.create(name=name, color=color)

exit()
```

**7. Run the development server**

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉

---

## 🗄️ Data Models

### `Category`
| Field | Type | Description |
|---|---|---|
| `name` | CharField | Category label (e.g. Technology) |
| `description` | TextField | Optional description |
| `color` | CharField | Hex color code for badges |

### `Event`
| Field | Type | Description |
|---|---|---|
| `title` | CharField | Event name |
| `description` | TextField | Full event details |
| `category` | ForeignKey | → Category (nullable) |
| `organizer` | ForeignKey | → User (creator) |
| `location` | CharField | Venue / address |
| `start_date` / `end_date` | DateTimeField | Event duration |
| `max_attendees` | PositiveIntegerField | Capacity limit |
| `image` | ImageField | Optional event image |
| `status` | CharField | `upcoming` / `ongoing` / `completed` / `cancelled` |
| `is_free` | BooleanField | Free event flag |
| `ticket_price` | DecimalField | Price if paid event |

### `Registration`
| Field | Type | Description |
|---|---|---|
| `event` | ForeignKey | → Event |
| `attendee` | ForeignKey | → User |
| `status` | CharField | `confirmed` / `cancelled` / `waitlisted` |
| `registered_at` | DateTimeField | Auto timestamp |
| `notes` | TextField | Optional attendee notes |

---

## 🌐 URL Reference

| URL | Page | Auth Required |
|---|---|---|
| `/` | Event listing & search | No |
| `/events/create/` | Create new event | ✅ Yes |
| `/events/<id>/` | Event detail | No |
| `/events/<id>/edit/` | Edit event | ✅ Organizer only |
| `/events/<id>/delete/` | Delete event | ✅ Organizer only |
| `/events/<id>/register/` | Register for event | ✅ Yes |
| `/events/<id>/cancel/` | Cancel registration | ✅ Yes |
| `/events/<id>/attendees/` | View attendee list | ✅ Organizer only |
| `/my-events/` | Personal dashboard | ✅ Yes |
| `/login/` | Login page | No |
| `/register/` | Sign up | No |
| `/admin/` | Django admin panel | ✅ Staff only |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11.9 |
| Framework | Django 4.2.7 |
| Database | SQLite (development) |
| Image Handling | Pillow 10.1.0 |
| Frontend | Pure HTML + CSS (no Node.js needed) |
| Auth | Django built-in auth |
| Admin | Django Admin (pre-configured) |

---

## ⚙️ Configuration

Key settings in `event_management/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'events',   # ← Add this
]

TIME_ZONE = 'Asia/Kolkata'   # Change to your timezone

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL           = '/login/'
LOGIN_REDIRECT_URL  = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

---

## 🚨 Production Deployment

Before going live, update `settings.py`:

```python
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']   # Use env variable

ALLOWED_HOSTS = ['yourdomain.com']

# Switch to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ['DB_NAME'],
        'USER':     os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST':     os.environ['DB_HOST'],
        'PORT':     '5432',
    }
}
```

Then run:

```bash
pip install gunicorn psycopg2-binary
python manage.py collectstatic
gunicorn event_management.wsgi:application
```

---

## 📦 requirements.txt

```
Django==4.2.7
Pillow==10.1.0
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch — `git checkout -b feature/your-feature`
3. Commit your changes — `git commit -m 'Add some feature'`
4. Push to the branch — `git push origin feature/your-feature`
5. Open a Pull Request

---


## 👤 Author

**Your Name**
- GitHub: [@gayathribhupathi)

---

<div align="center">
  Built with ❤️ using Django & Python 3.11
</div>
