FROM python:3.9.7-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt
RUN cd /
EXPOSE 8000
RUN pip install -U pip && pip install -U -r requirements.txt
WORKDIR /app
COPY . .
CMD ["python3", "app.py"]
