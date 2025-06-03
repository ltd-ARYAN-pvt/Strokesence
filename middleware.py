from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
from db.collections import get_collection
import psutil

#--> logging
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = datetime.now(timezone.utc)
        response = await call_next(request)
        duration = (datetime.now(timezone.utc) - start).total_seconds()

        logs_collection = get_collection("logs")
        await logs_collection.insert_one({
            "path": request.url.path,
            "method": request.method,
            "timestamp": start.isoformat(),
            "duration": duration,
            "status_code": response.status_code
        })
        return response
    
#--> Profiling
class ProfilingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now(timezone.utc)
        process = psutil.Process()
        cpu_start = psutil.cpu_percent(interval=None)
        mem_start = process.memory_info().rss / (1024 * 1024)

        response = await call_next(request)

        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds() * 1000  # in milliseconds
        cpu_end = psutil.cpu_percent(interval=None)
        mem_end = process.memory_info().rss / (1024 * 1024)

        profiling_data = {
            "time_stamp":start_time.isoformat(),
            "cpu_usage":(cpu_start + cpu_end) / 2,
            "memory_usage":(mem_start + mem_end) / 2,
            "latency_ms":duration,
            "endpoint":request.url.path
        }

        profiling_collection = get_collection("profiling")
        await profiling_collection.insert_one(profiling_data)

        return response
