import sys

from urllib.request import Request, urlopen

from config import HOSTNAME, PORT


url = f"http://{HOSTNAME}:{PORT}/ping"
req = Request(url=url, method="GET", headers={ "Accept": "plain/text" })
with urlopen(req) as res:
	body = res.read().decode("utf-8")
	if body == "pong":
		sys.exit(0)
	else:
		sys.exit(1)
