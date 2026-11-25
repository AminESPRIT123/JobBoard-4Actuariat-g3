"""Notification microservice - entry point.

Run:  python -m app.main                      (port 8084)
      $env:PORT=8094; python -m app.main      (second instance, PowerShell)
The port must come from PORT so the one declared in Eureka matches.
"""
import os
from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka_client
from fastapi import FastAPI

from app.routers import notification

# Port read from the PORT environment variable to allow several instances
PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: register in Eureka as NOTIFICATION
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="NOTIFICATION",
        instance_host="localhost",
        instance_port=PORT,
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info",  # link in the Eureka dashboard
    )
    yield
    # Shutdown: stop the Eureka client (unregisters the instance)
    await eureka_client.stop_async()


app = FastAPI(
    lifespan=lifespan,
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
)

app.include_router(notification.router)


# ---- Health & info (used by Eureka) ----
@app.get("/health", tags=["Monitoring"], summary="Health of the service")
def health() -> dict:
    return {"status": "UP"}


@app.get("/info", tags=["Monitoring"], summary="Service information")
def info() -> dict:
    return {"app": {"name": "notification", "version": app.version}}

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
