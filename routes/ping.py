from http import HTTPStatus
from typing import Tuple


__all__ = ["ping"]

def ping(method, *args, **kwargs) -> Tuple[HTTPStatus, str | None]:
	if method == "GET":
		return HTTPStatus.OK, "pong"

	return HTTPStatus.METHOD_NOT_ALLOWED, None
