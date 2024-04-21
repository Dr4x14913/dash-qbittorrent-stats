FROM python:latest

# Install dependencies
RUN pip install mysql-connector-python qbittorrent-api apscheduler pandas

# Copy local code to the container image.
COPY ./schedule /schedule

# Define working directory in the container
WORKDIR /schedule

CMD ["python", "schedule.py"]
