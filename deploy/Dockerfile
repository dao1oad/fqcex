FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip \
    && python -m pip install .

CMD ["python", "-m", "perp_platform.control_plane", "--host", "0.0.0.0", "--port", "8080"]
