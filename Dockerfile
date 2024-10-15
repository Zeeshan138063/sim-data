# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libffi-dev \
    libssl-dev \
    tcl-dev \
    x11vnc \
    xvfb \
    fluxbox \
    && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variable for virtual display
ENV DISPLAY=:99

# Expose the VNC port (if you want to connect via VNC later)
EXPOSE 5900

# Run the Xvfb server, and execute the Python script
CMD xvfb-run --server-args="-screen 0 1024x768x24" python app_curl_cffi.py
