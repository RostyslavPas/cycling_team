# Creative States Cycling Team — MVP Landing

Production-ready MVP landing for the Creative States Cycling Team built with Django.

**Stack:** Django, SQLite for dev, PostgreSQL-ready for production (Render), vanilla HTML/CSS/JS, Django Admin for content management.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_initial_data
python3 manage.py createsuperuser
python3 manage.py runserver
```

Optional: copy `.env.example` to `.env` and edit values.

## Deploy to Render

This project is prepared for Render with:
- `render.yaml`
- `build.sh`
- `gunicorn` + `whitenoise`
- optional `DATABASE_URL` support (PostgreSQL)

### Option A: Blueprint deploy (recommended)

1. Push this repository to GitHub.
2. In Render, choose **New +** -> **Blueprint**.
3. Select this repository (Render will read `render.yaml` automatically).
4. After deploy, open the Render shell and run:

```bash
python manage.py createsuperuser
python manage.py seed_initial_data
```

### Option B: Manual web service

1. In Render, create a new **Web Service** from your repo.
2. Use:

```text
Build Command: ./build.sh
Start Command: gunicorn creative_states.wsgi:application --log-file -
```

3. Add environment variables:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<generate strong secret>
DJANGO_ALLOWED_HOSTS=.onrender.com
DJANGO_SERVE_MEDIA=True
DJANGO_CSRF_TRUSTED_ORIGINS=https://*.onrender.com
DJANGO_SECURE_PROXY_SSL_HEADER=True
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
DJANGO_SECURE_HSTS_PRELOAD=True
```

4. Attach a Render PostgreSQL database and set `DATABASE_URL` in the web service.

5. After first deploy, run in Render shell:

```bash
python manage.py createsuperuser
python manage.py seed_initial_data
```

## Features

- Single landing page with hero, about, trainings, members, sponsors ticker, and signup.
- Training & member carousels with swipe (mobile) and arrows (desktop).
- AJAX signup form with validation and success message.
- Admin-managed trainings, team members, sponsors, and signups.
- Privacy Policy and Terms of Use pages.

## Admin

- Admin panel: `http://127.0.0.1:8000/admin/`
- Models: Trainings, Team Members, Sponsors, Training Signups.
- CSV export for signups from admin actions.

## Training Day Pages (staff-only)

Dynamic page per training weekday and date:

```
/trainings/<weekday>/<YYYY-MM-DD>/
```

Example:
```
/trainings/tuesday/2026-02-11/
```

Access is restricted to staff users. Log in via `/admin/` and then open the training day URL in the same session.

## Strava Embed

In the Training record, set `strava_embed_url` to the iframe `src` from Strava. Example:

```text
https://www.strava.com/routes/12345678/embed
```

If empty, a placeholder will be displayed.

## Media

Team member photos and sponsor logos are uploaded via the admin UI and served from `/media/` in development.
On Render, local media storage is ephemeral. For persistent uploads in production, use object storage (e.g. S3/Cloudinary).
For this MVP (seed images from repository), keep `DJANGO_SERVE_MEDIA=True` in Render so `/media/...` URLs are served.

## Notes

- The project uses a single HTML template (`templates/site.html`), one CSS file, and one JS file.
- Default trainings and sponsors are seeded by `python3 manage.py seed_initial_data`.
