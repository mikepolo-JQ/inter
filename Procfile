release: make data
web: daphne src.project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: make worker
