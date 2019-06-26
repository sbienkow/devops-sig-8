FROM python:latest
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY app.py /
CMD gunicorn -b 0.0.0.0 --log-level debug app:api
