# Shop-API (Django + DRF + Docker + CI/CD)

Трекер привычек на Django REST Framework, контейнеризированный через Docker Compose, с тестами, покрытием и настроенным CI/CD.

## Локальный запуск

Проект запускается **одной командой** (все сервисы: Django, PostgreSQL, Redis, Celery, Nginx):

```bash
docker compose up --build
