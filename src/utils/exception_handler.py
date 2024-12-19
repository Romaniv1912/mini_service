import httpx

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.utils.trace_id import get_request_trace_id


def register_exception(app: FastAPI):
    @app.exception_handler(httpx.HTTPError)
    def httpx_error_handler(request: Request, exc: httpx.HTTPError):
        """
        HTTP exception handler

        :param request:
        :param exc:
        :return:
        """

        host = exc.request.url.host
        path = exc.request.url.path
        method = exc.request.method
        return JSONResponse(
            dict(
                trace_id=get_request_trace_id(request),
                detail=f"Can't get access to resource {host=}, {path=}, {method=}",
            ),
            status_code=500,
        )

    @app.exception_handler(Exception)
    def all_unknown_exception_handler(request: Request, exc: Exception):
        """
        Global unknown exception handling

        :param request:
        :param exc:
        :return:
        """

        return JSONResponse(
            dict(
                trace_id=get_request_trace_id(request),
                detail=str(exc),
            ),
            status_code=500,
        )
