FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache gcc musl-dev libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["python", "/app/app/main.py"]