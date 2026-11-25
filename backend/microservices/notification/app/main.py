"""Notification microservice - entry point."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client.eureka_client import EurekaClient

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
BASE_URL = f"http://localhost:{PORT}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = EurekaClient(
        eureka_server="http://localhost:8761/eureka/",
        app_name="NOTIFICATION",
        instance_id=f"localhost:notification:{PORT}",
        instance_host="localhost",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        health_check_url=f"{BASE_URL}/health",
        status_page_url=f"{BASE_URL}/info",
        should_discover=False,
    )
    await client.start()
    try:
        yield
    finally:
        await client.stop()


app = FastAPI(
    lifespan=lifespan,
    title="Notification Microservice API",
    version="1.0.0",
    description="Notification microservice (Python / FastAPI, no database).",
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": BASE_URL, "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
)

app.include_router(notification.router)


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/info")
def info():
    return {"name": "notification", "version": app.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)