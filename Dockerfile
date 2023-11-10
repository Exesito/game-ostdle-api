FROM python:3.8.10

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]