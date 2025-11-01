import time
from collections import defaultdict
from typing import Dict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from .settings import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter using token bucket algorithm."""
    
    def __init__(self, app, requests_per_minute: int | None = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or settings.rate_limit_per_minute
        self.tokens: Dict[str, float] = defaultdict(lambda: float(self.requests_per_minute))
        self.last_refill: Dict[str, float] = defaultdict(time.time)
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/search"):
            client_ip = request.client.host if request.client else "unknown"
            now = time.time()
            
            # Refill tokens
            time_passed = now - self.last_refill[client_ip]
            tokens_to_add = (time_passed / 60.0) * self.requests_per_minute
            self.tokens[client_ip] = min(
                self.requests_per_minute,
                self.tokens[client_ip] + tokens_to_add
            )
            self.last_refill[client_ip] = now
            
            # Check if enough tokens
            if self.tokens[client_ip] < 1:
                return Response(
                    content='{"detail":"Rate limit exceeded"}',
                    status_code=429,
                    media_type="application/json"
                )
            
            # Consume token
            self.tokens[client_ip] -= 1
        
        response = await call_next(request)
        return response

