import uvicorn

import app  # noqa
from config.settings import Settings

if __name__ == "__main__":
    settings = Settings()

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        use_colors=settings.COLOR_LOGS,
        proxy_headers=True,
        reload_dirs=["core", "config"],
    )
