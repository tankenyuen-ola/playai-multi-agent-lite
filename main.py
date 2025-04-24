import uvicorn
import argparse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from core.routers.approuter import router, openai_router
from core.config.allowed_hosts import app_allowed_hosts

# Create FastAPI app instance
app = FastAPI(
    title="Player Multi-Agent API",
    description="API for the Player Multi-Agent system",
    version="0.1.0"
)

# Configure size limits
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_REQUEST_SIZE = 20 * 1024 * 1024  # 20MB

class SizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check content length for all requests
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > MAX_REQUEST_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request too large"}
            )
        
        # For multipart requests, check individual file sizes
        if request.headers.get('content-type', '').startswith('multipart/form-data'):
            try:
                form = await request.form()
                for field in form:
                    if hasattr(field, 'file'):
                        file_size = 0
                        async for chunk in field.file.stream():
                            file_size += len(chunk)
                            if file_size > MAX_UPLOAD_SIZE:
                                return JSONResponse(
                                    status_code=413,
                                    content={"detail": "File too large"}
                                )
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"detail": f"Invalid multipart request: {str(e)}"}
                )
        
        response = await call_next(request)
        return response

# Add middleware
app.add_middleware(SizeLimitMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=app_allowed_hosts)

# Include routers
app.include_router(router)
app.include_router(openai_router)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns basic API information
    """
    return {
        "message": "Welcome to the Player Multi-Agent API",
        "version": "0.1.0",
        "status": "operational"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status
    """
    return {
        "status": "healthy",
        "service": "multi-agent-api"
    } 
