FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /code
COPY requirements.txt requirements.txt
COPY . . 
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "core.main:app", "--reload", "--host", "0.0.0.0"]