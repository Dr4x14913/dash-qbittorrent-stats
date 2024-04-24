FROM python:latest

# Install dependencies
RUN pip install mysql-connector-python qbittorrent-api apscheduler pandas

# Copy local code to the container image.
COPY ./scheduler /scheduler

# Define working directory in the container
WORKDIR /scheduler

CMD ["python", "scheduler.py"]
