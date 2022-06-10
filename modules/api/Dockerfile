FROM python:3.7-alpine

COPY ./modules/api /api
WORKDIR /api

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 30003

COPY . .
# CMD ["python", "-u", "wsgi.py"]
CMD ["flask", "run", "--host", "0.0.0.0"]