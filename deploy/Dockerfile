FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    && python -m pip install .

CMD ["python", "-m", "perp_platform.control_plane", "--host", "0.0.0.0", "--port", "8080"]
