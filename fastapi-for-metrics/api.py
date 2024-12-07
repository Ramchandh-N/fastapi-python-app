from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from prometheus_client import Counter, Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
import time
import random
import os

app = FastAPI()

request_count = Counter('http_req_total', 'HTTP Requests Total', ['method', 'endpoint', 'http_status'])
response_time_histogram = Histogram('http_response_time_seconds', 'HTTP Response Time', ['method', 'endpoint', 'http_status'])
memory_usage = Gauge('memory_usage_in_bytes', 'System Memory Usage')

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()  # Start timer
    response = await call_next(request)
    process_time = time.time() - start_time  # Calculate response time

    # Update Prometheus metrics
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()
    response_time_histogram.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).observe(process_time)

    return response

Instrumentator().instrument(app).expose(app)

# Directory for the file download
FILE_PATH = "employees.txt"

# Generate a dummy file for testing
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        f.write("This is an example file for download.")

@app.get("/health", summary="Health Check API")
async def health_check():
    """Returns the health status of the application with a random delay."""
    delay = random.uniform(0.1, 10.0)  # Random delay between 0.1 and 2 seconds
    time.sleep(delay)
    return {"status": "healthy", "response_time": f"{delay:.2f} seconds"}

@app.get("/download", summary="File Download API")
async def download_file():
    """Allows the user to download a file with a random delay."""
    delay = random.uniform(0.1, 10.0)  # Random delay between 0.1 and 2 seconds
    time.sleep(delay)
    return FileResponse(FILE_PATH, media_type="application/octet-stream", filename="employees.csv")

@app.get("/", summary="API Info")
def api_info():
    """Returns information about the available endpoints."""
    return JSONResponse({
        "endpoints": {
            "/health": "Check the health of the application.",
            "/download": "Download the example file."
        }
    })