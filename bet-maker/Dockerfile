FROM python:3.10.14-alpine

WORKDIR /app

COPY . .

RUN apk update && apk add --no-cache ca-certificates && update-ca-certificates

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
