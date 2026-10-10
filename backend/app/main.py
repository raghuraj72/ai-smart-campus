import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1 import analytics, auth, complaints, organizations, websockets
from app.core.limiter import limiter
from app.services.websocket_manager import ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_task = asyncio.create_task(ws_manager.listen_to_redis())
    yield
    redis_task.cancel()
    try:
        await redis_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="AI Smart Campus Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# SlowAPI Configuration
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Prometheus Telemetry Instrumentation (/metrics)
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(complaints.router, prefix="/api/v1", tags=["Complaints"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(organizations.router, prefix="/api/v1", tags=["Organizations"])
app.include_router(websockets.router)


@app.get("/health", tags=["Health"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {"status": "online", "system": "AI Smart Campus Core"}
