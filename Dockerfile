FROM python:3.11.9-slim-bullseye

WORKDIR /app

# Install all dependencies 
RUN apt-get update

# Copy requirements.txt file
COPY requirements.txt /app/requirements.txt

# Copy all needed files to docker image app folder
COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# RUN alembic upgrade head

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

# Run build command
# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
# Run build command
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]