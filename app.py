from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.settings import Settings
from core.controllers.v1.locations import location_v1_router
from core.controllers.v1.users import user_v1_router
from logger import logger

settings = Settings()

logger.info("Initializing application")

app = FastAPI(
    debug=settings.DEBUG,
    title="Listen Backend API.",
    docs_url="/docs" if settings.IS_DOC_ENABLED else None,
    redoc_url="/redoc" if settings.IS_DOC_ENABLED else None,
)

# Add cors middleware for local development
if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# configure routing

app.include_router(prefix="/v1/users", router=user_v1_router, tags=["users"])
app.include_router(prefix="/v1/locations", router=location_v1_router, tags=["locations"])


logger.info("Application initialization completed")
