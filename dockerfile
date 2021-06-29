FROM python:latest

WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5555
COPY . .

CMD python src/main.py