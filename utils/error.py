from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

async def mongodb_exception_handler(request: Request, exc: PyMongoError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed", "error": str(exc)},
    )