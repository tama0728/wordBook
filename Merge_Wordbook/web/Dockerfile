# Dockerfile

# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 인증서 파일 복사
COPY ./certs/cert.pem /etc/ssl/certs/
COPY ./certs/privkey.pem /etc/ssl/private/
COPY ./certs/chain.pem /etc/ssl/certs/

# Copy current directory contents into the container at /app
COPY ../.. .

# 환경변수 설정 (Flask 실행을 위한 환경변수)
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port
EXPOSE 5005

# Command to run the application
CMD ["python", "app.py"]
