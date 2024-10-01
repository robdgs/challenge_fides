FROM python:3

RUN apt-get update && apt-get install postgresql-client -y

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY login/ /app/login/
COPY wait_for_db.sh /app/login/

WORKDIR /app/login/

RUN chmod +x wait_for_db.sh

EXPOSE 8000

ENTRYPOINT ["./wait_for_db.sh", "login_db", "python3", "manage.py", "runserver", "0.0.0.0:8000"]