from routes.foobar import foobar


__all__ = ["routes"]

"""
Routes mapping is shown below

{
  'hello': hello,
  'foo': {
	'/': foo,
	'bar': bar,
	'[]': {
	  'apple': apple,
	  '[]': fruit
	  '/': food
	}
  }
}

Explaination
1. /hello invokes `hello` service
2. /foo invokes `foo` service
3. /foo/bar invokes `bar` service
4. /foo/bar2 invokes `food` service, with params [bar2]
5. /foo/bar2/apple invokes `apple` service, with params [bar2]
6. /foo/bar2/pear invokes `fruit` service, with params [bar2, pear]
7. /world return 404
"""
routes = {
	"/": foobar,
	"foo": {
		"/": foobar,
		"bar": foobar,
		"[]": {
			"/": foobar,
			"hello": foobar
		}
	}
}
