FROM python:3.8
RUN mkdir /web
COPY web/app/ /web/app/
COPY web/flask-bin.py /web/
COPY web/requirements.txt /web/
WORKDIR /web
RUN python -m pip install --upgrade pip
RUN python -m pip --no-cache-dir install -r requirements.txt
CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "flask-bin:app"]