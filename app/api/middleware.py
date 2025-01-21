import time
import traceback

from fastapi import Request, Response, status
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

from app.logger import logger


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """Implement middleware dispatch hook."""

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except:  # pylint: disable=bare-except
            traceback.print_exc()
            response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        process_time = time.perf_counter() - start_time
        logger.info(
            f"Request Logged.",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "process_time": process_time,
            },
        )

        return response
