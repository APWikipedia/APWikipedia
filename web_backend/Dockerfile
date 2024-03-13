FROM python:3.11.5

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-m" , "flask",  "--app","app.py", "run", "--host=0.0.0.0","--port=5000"]