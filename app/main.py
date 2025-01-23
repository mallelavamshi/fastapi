from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import uvicorn

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Image Processing API",
        version="1.0.0",
        description="""
        This API provides endpoints for processing images and generating reports.
        
        Features:
        * Process images from local folder or Google Drive
        * Generate Excel reports with images and analysis
        * Generate PDF reports
        
        For more information, visit the /docs endpoint.
        """,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="Image Processing API",
    description="API for processing images and generating Excel/PDF reports",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api/v1")

# Custom OpenAPI schema
app.openapi = custom_openapi

# Root route
@app.get("/", 
         summary="Root endpoint",
         description="Returns basic information about the API")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to the Image Processing API",
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "available_endpoints": {
                "Process Images": "/api/v1/process-images",
            },
            "version": "1.0.0"
        }
    )

# Health check endpoint
@app.get("/health",
         summary="Health check endpoint",
         description="Returns the current health status of the API")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)