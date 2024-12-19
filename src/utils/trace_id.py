from fastapi import Request

from src.core.conf import settings


def get_request_trace_id(request: Request) -> str:
    return request.headers.get(settings.APP.TRACE_ID_REQUEST_HEADER_KEY) or '-'
