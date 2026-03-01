import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from database import init_indexes
from routes.admin_routes import router as admin_router
from routes.ads_routes import router as ads_router
from routes.auth_routes import router as auth_router
from routes.news_routes import router as news_router
from scheduler import start_scheduler
from utils.logger import configure_logging

configure_logging()
logger = logging.getLogger("main")

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(title=settings.app_name)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
def on_startup() -> None:
    init_indexes()
    if settings.scheduler_enabled:
        start_scheduler()


@app.get("/")
@limiter.limit("10/minute")
async def health(request: Request):
    return {"status": "ok", "service": settings.app_name}


app.include_router(auth_router)
app.include_router(news_router)
app.include_router(ads_router)
app.include_router(admin_router)
