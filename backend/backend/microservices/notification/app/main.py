
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client import eureka_client

from app.routers import notification

PORT = int(os.getenv("PORT", "8091"))


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Enregistrement du microservice dans Eureka
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="127.0.0.1",
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info"
    )

    print("NOTIFICATION registered in Eureka!")

    yield

    # Arrêt du client Eureka
    await eureka_client.stop_async()
    print("NOTIFICATION disconnected from Eureka!")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description="Notification microservice (Python / FastAPI).",
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(notification.router)


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.get("/info")
async def info():
    return {
        "name": "notification",
        "version": app.version
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT
    )
