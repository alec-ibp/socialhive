
###########
# BUILDER #
###########

FROM python:3.8-slim-buster as builder

# set work directory
WORKDIR /code

# accept build args
ARG DJANGO_SECRET_KEY

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install SO dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    postgresql-client \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip

# Copy project dependencies
COPY requirements.txt /code/requirements.txt

# Build project dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt


###############
# FINAL IMAGE #
###############

# Final stage/image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /code

# create unprivileged user and group
RUN addgroup --gid 1001 --system app \
    && adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

# fetch data from builder stage
COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt /code/requirements.txt

# install project dependencies
RUN pip install --no-cache /wheels/*

# Copy source code
COPY . /code/

# use the unprivileged user
USER app

EXPOSE 8000
