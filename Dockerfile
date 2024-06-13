FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements.txt /backend/

RUN pip install -r requirements.txt

COPY . /backend/

EXPOSE 8000
ADD start.sh /start.sh
RUN chmod a+x /start.sh
ENTRYPOINT ["/start.sh" ]
