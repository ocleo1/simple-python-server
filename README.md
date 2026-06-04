# Simple Python Server

## systemd

Copy the project and install the service:

```sh
python3 -m venv --prompt simple-python-server .venv
.venv/bin/pip install -r requirements.txt
# Edit .env and set API_PORT
sudo cp simple-python-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now simple-python-server
```

Manage the service:

```sh
sudo systemctl status simple-python-server
sudo journalctl -u simple-python-server -f
sudo systemctl restart simple-python-server
```

## Development

### uv

```sh
uv sync
uv run python3 server.py
```

### pip

```sh
python3 -m venv --prompt simple-python-server .venv
source .venv/bin/active
pip install -r requirements.txt
python server.py
```
