# The Dockerfile defines the image's environment
# Import Python runtime and set up working directory
FROM python:3.7-alpine
WORKDIR /app
COPY . /app

# Install any necessary dependencies
RUN pip install pipenv
RUN pipenv install

# Run app.py when the container launches
CMD ['python', 'app.py']
