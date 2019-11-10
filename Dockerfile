# The Dockerfile defines the image's environment
# Import Python runtime and set up working directory
FROM python:3.7-alpine
WORKDIR /app
COPY . /app

# Install any necessary dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install pipenv
RUN pipenv install

# Run app.py when the container launches
CMD ['python', 'app.py']
