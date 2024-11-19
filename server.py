# - *- coding: utf-8 - *-

import optparse
from http.server import HTTPServer

from router import Router
from config import HOSTNAME, PORT


if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option(
		"--hostname",
		help="Hostname for the app " + "[default %s]" % HOSTNAME,
		default=HOSTNAME
	)
	parser.add_option(
		"--port",
		help="Port for the app " + "[default %s]" % PORT,
		default=PORT
	)
	args, _ = parser.parse_args()

	web_server = HTTPServer((args.hostname, int(args.port)), Router)
	print("Server started http://%s:%s" % (args.hostname, args.port))

	try:
		web_server.serve_forever()
	except KeyboardInterrupt:
		pass

	web_server.server_close()
	print("Server stopped.")
