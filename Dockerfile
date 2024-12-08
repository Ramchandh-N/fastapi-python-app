FROM python:3.12-slim

WORKDIR /app

# Copy application
COPY fastapi-for-metrics/requirements.txt /app/
COPY fastapi-for-metrics /app/

#checks installation
RUN python3 --version && which python3 && pip3 --version

RUN pip3 install -r requirements.txt

ENTRYPOINT ["uvicorn"]
CMD ["api:app","--reload","--host", "0.0.0.0", "--port", "8000"]