FROM python:3.10-bullseye

RUN apt update
RUN apt upgrade -y

# If you find that SQLite is not available, you can uncomment the following line to install it:
# RUN apt-get install -y sqlite3

RUN apt-get install -y nano iputils-ping curl borgbackup cron

# Add a new user
RUN useradd -ms /bin/bash pilot
# Switch to the new user
USER pilot

#ENV POETRY_NO_INTERACTION=1

## PYTHON
RUN curl -sSL https://install.python-poetry.org | python3 -
# Update PATH to include Poetry
ENV PATH="/home/pilot/.local/bin:$PATH"

# Copy the project files into the container
COPY ./ /DashboardRaffinerie
# Set the working directory
WORKDIR /DashboardRaffinerie

# initialisation of poetry
RUN poetry install

# # Expose port 8080
EXPOSE 8080

# # Start Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
