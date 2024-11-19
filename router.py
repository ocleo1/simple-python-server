import unittest

from io import BytesIO
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from unittest.mock import MagicMock
from urllib.parse import urlparse, unquote, ParseResult
from functools import reduce
from inspect import isfunction
from typing import Dict, Callable

from routes import routes


__all__ = ["Router"]

class Router(BaseHTTPRequestHandler):
	def __get_charset(self):
		charset = "utf-8"
		content_type: str | None = self.headers.get("content-type")
		if content_type is not None:
			parts = content_type.split("=")
			if len(parts) == 2:
				charset = parts[-1]
		return charset

	def __write_response(self, http_status: HTTPStatus, result: str | None):
		self.protocol_version = "HTTP/1.1"
		self.send_response(http_status)
		charset = self.__get_charset()
		if http_status < HTTPStatus.BAD_REQUEST:
			mime = self.headers.get("accept")
			if mime is not None:
				self.send_header("Content-type", f"{mime};charset={charset}")
			else:
				self.send_header("Content-type", f"text/plain;charset={charset}")
		self.end_headers()
		if result is not None:
			data = bytes(result, charset)
			self.wfile.write(data)

	def __router(self, parsed_url: ParseResult) -> Callable | None:
		self.__params = list()
		path_chunks = parsed_url.path.split('/')
		def reducer(acc: Dict | Callable, curr: str):
			if isfunction(acc):
				return acc
			handler = acc.get(curr)
			if handler is not None:
				return handler
			handler = acc.get("[]")
			if handler is not None:
				self.__params.append(curr)
				return handler
			handler = acc.get("/")
			if handler is not None:
				return handler
			return acc
		func = reduce(reducer, path_chunks[1:], routes)
		if isinstance(func, Dict):
			func = func.get('/')
		if isfunction(func):
			return func
		return None
	
	def __handle(self, method: str, body = None):
		parsed_url = urlparse(self.path)
		route_handler = self.__router(parsed_url)
		if route_handler is None:
			self.__write_response(HTTPStatus.INTERNAL_SERVER_ERROR, None)
		else:
			http_status, result = route_handler(method, self.__params, body, parsed_url=parsed_url)
			self.__write_response(http_status, result)

	def log_request(self, code='-', size='-'):
		if self.path == '/ping':
			return
		super().log_request(code, size)

	def do_GET(self):
		self.__handle("GET")

	def do_POST(self):
		charset = self.__get_charset()
		content_length = self.headers.get("content-length")
		body = None
		if content_length is not None:
			body = self.rfile.read(int(content_length)).decode(charset)
		else:
			body = self.rfile.read().decode(charset)
		body = unquote(body, charset)
		self.__handle("POST", body)

class TestRouter(unittest.TestCase):
	def setUp(self):
		self.__address = ('127.0.0.1', 8080)

	def __create(self, request: bytes) -> Router:
		mock_socket = MagicMock()
		mock_socket.makefile.return_value = BytesIO(request)

		handler = Router(mock_socket, self.__address, None)
		handler.rfile = BytesIO()
		handler.wfile = BytesIO()
		handler.send_response = MagicMock()
		handler.send_header = MagicMock()
		handler.end_headers = MagicMock()

		return handler

	def test_do_GET_root(self):
		request = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

		handler = self.__create(request)
		handler.do_GET()

		self.assertEqual(handler.wfile.getvalue(), b"")
		handler.send_response.assert_called_with(HTTPStatus.OK)
		handler.send_header.assert_any_call("Content-type", "text/plain;charset=utf-8")
		handler.end_headers.assert_called_once()
		self.assertEqual(handler.send_response.call_count, 1)

	def test_do_GET_foo_bar(self):
		request = b"GET /foo/bar HTTP/1.1\r\nHost: localhost\r\n\r\n"

		handler = self.__create(request)
		handler.do_GET()

		self.assertEqual(handler.wfile.getvalue(), b"")
		handler.send_response.assert_called_with(HTTPStatus.OK)
		handler.send_header.assert_any_call("Content-type", "text/plain;charset=utf-8")
		handler.end_headers.assert_called_once()
		self.assertEqual(handler.send_response.call_count, 1)

	def test_do_GET_foo_go(self):
		request = b"GET /foo/go HTTP/1.1\r\nHost: localhost\r\n\r\n"

		handler = self.__create(request)
		handler.do_GET()

		self.assertEqual(handler.wfile.getvalue(), b"go")
		handler.send_response.assert_called_with(HTTPStatus.OK)
		handler.send_header.assert_any_call("Content-type", "text/plain;charset=utf-8")
		handler.end_headers.assert_called_once()
		self.assertEqual(handler.send_response.call_count, 1)

	def test_do_GET_foo_run_hello(self):
		request = b"GET /foo/run/hello HTTP/1.1\r\nHost: localhost\r\n\r\n"

		handler = self.__create(request)
		handler.do_GET()

		self.assertEqual(handler.send_response.call_count, 1)
		handler.send_response.assert_called_with(HTTPStatus.OK)
		handler.send_header.assert_any_call("Content-type", "text/plain;charset=utf-8")
		handler.end_headers.assert_called_once()
		self.assertEqual(handler.wfile.getvalue(), b"run")

	def test_do_POST_foo_run_hello(self):
		request = b"POST /foo/run/hello HTTP/1.1\r\nHost: localhost\r\nContent-Type: text/plain;charset=utf-8\r\n\r\n{hello:world}"

		handler = self.__create(request)
		handler.do_POST()

		self.assertEqual(handler.send_response.call_count, 1)
		handler.send_response.assert_called_with(HTTPStatus.METHOD_NOT_ALLOWED)

	def tearDown(self) -> None:
		del self.__address


if __name__ == '__main__':
	unittest.main()
