from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import cases, workflow

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def internal_auth(request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)
    key = request.headers.get("x-internal-key")
    if settings.internal_api_key and key != settings.internal_api_key:
        raise HTTPException(401, "Unauthorized")
    return await call_next(request)


@app.get("/health")
def health():
    return {"ok": True, "app": settings.app_name, "mock_mode": settings.mock_mode}


app.include_router(cases.router, prefix="/api")
app.include_router(workflow.router, prefix="/api")
