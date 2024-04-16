FROM python:3.10-bullseye

RUN apt update
RUN apt upgrade -y

RUN mkdir -p /usr/share/man/man1
RUN mkdir -p /usr/share/man/man7

RUN apt-get install -y --no-install-recommends postgresql-client
RUN apt-get install -y nano iputils-ping curl borgbackup cron

# Add a new user
RUN useradd -ms /bin/bash laraffinerie
# Switch to the new user
USER laraffinerie

ENV POETRY_NO_INTERACTION=1

## PYTHON
RUN curl -sSL https://install.python-poetry.org | python3 -
# Update PATH to include Poetry
ENV PATH="/home/laraffinerie/.local/bin:$PATH"

# Set the working directory
WORKDIR /DashboardRaffinerie

# Copy the project files into the container
COPY . /DashboardRaffinerie/

# initialisation of poetry
# Regenerate the poetry.lock file to match pyproject.toml
USER root
RUN poetry lock
USER laraffinerie

RUN poetry install

# # Expose port 8080
EXPOSE 8080

# # Start Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
