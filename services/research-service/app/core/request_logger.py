import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """
    Log every incoming HTTP request.
    """

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s | %s | %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response