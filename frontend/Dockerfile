# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

ENV SERVICE_BUS_CONNECTION_STR="Endpoint=sb://studentattend.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Yoa1WTBpGLx4tQWqHSdU7ALErw5Vc+GUz+ASbK75TLE="
ENV SERVICE_BUS_QUEUE_NAME="students"
# Copy the files needed for the app to the container
COPY app.py .
COPY requirements.txt .
COPY templates templates

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for the app to listen on
EXPOSE 5000

# Set the entrypoint for the container
ENTRYPOINT ["python", "app.py"]
