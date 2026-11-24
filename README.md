# Cooking Recipes Site

The existing recipe pages now run as a Django application with MySQL-backed user accounts. Django's built-in authentication model hashes passwords before storing them; the raw password is never saved. Anonymous visitors can also enter as guests, with access tracked by a server-side session.

## Run with Docker

Install Docker Desktop, start it, then from the project directory run:

```powershell
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080). The root page redirects to login. Use **Continue as Guest** or register an account. Django applies its database migrations automatically when the app container starts.

Stop the containers with `Ctrl+C`, or run:

```powershell
docker compose down
```

MySQL data is kept in the `db_data` Docker volume. To remove the database and all registered accounts as well, run `docker compose down --volumes`.

## Configuration

Compose has local-development defaults, so it starts without extra files. For custom credentials, copy `.env.example` to `.env`, replace the placeholder values, and run Compose. Keep `.env` private and do not use the development defaults on a public server.

## Contact email

Set these values in `.env`:

```dotenv
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_USE_SSL=0
EMAIL_HOST_USER=your-sending-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-sending-email@gmail.com
CONTACT_RECIPIENT_EMAIL=your-destination-email@example.com
```

For Gmail, enable two-step verification and create an App Password. Do not use the normal Gmail account password. `CONTACT_RECIPIENT_EMAIL` is the address that receives contact submissions and can be changed whenever needed.

Restart the containers after changing `.env`:

```powershell
docker compose down
docker compose up --build
```

## Project layout

- `backend/config/`: Django settings, URL routing, and WSGI entry point
- `backend/recipes/`: Django views and registration form
- `frontend/`: Django-rendered templates and CSS
- `images/`: recipe images served as static assets
- `compose.yml`: Django and MySQL services

The app uses Django's built-in `User` model as its data model, Django views as controllers, and the existing HTML pages as templates (Django's MVT pattern, analogous to MVC).
