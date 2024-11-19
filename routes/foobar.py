from http import HTTPStatus
from typing import Tuple


__all__ = ["foobar"]

def foobar(method, *args, **kwargs) -> Tuple[HTTPStatus, str | None]:
	params, body = args

	if method == "GET":
		return HTTPStatus.OK, ','.join(params)

	return HTTPStatus.METHOD_NOT_ALLOWED, None
