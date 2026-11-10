"""The FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import auth, tasks
from app.config import get_settings

UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def create_app() -> FastAPI:
    docs = get_settings().api_docs
    app = FastAPI(
        title="Tasks API",
        docs_url="/api/docs" if docs else None,
        redoc_url=None,
        openapi_url="/api/openapi.json" if docs else None,
    )

    @app.middleware("http")
    async def require_json_for_changes(request: Request, call_next):
        # A page on another site can send a form or a plain-text body with the user's
        # cookies, but it cannot send Content-Type: application/json without a CORS
        # preflight, which this API never allows. Requiring it blocks cross-site requests
        # even where SameSite does not reach, such as from a sibling subdomain.
        content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
        if request.method in UNSAFE_METHODS and content_type != "application/json":
            return JSONResponse(
                {"detail": "Send requests that change data as application/json."},
                status_code=415,
            )
        return await call_next(request)

    app.include_router(auth.router)
    app.include_router(tasks.router)

    @app.get("/api/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
