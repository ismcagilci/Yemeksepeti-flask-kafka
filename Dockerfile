FROM python:3.9.1
COPY ./requirements.txt /python-flask/requirements.txt
WORKDIR /python-flask
RUN pip install -r requirements.txt
COPY . /python-flask
CMD ["python","./app.py"]