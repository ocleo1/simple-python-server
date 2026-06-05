# Simple Python Server

## How to use

### systemd

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

### MacOS Launch Agent

Copy the project to an install location:

```sh
sudo cp -r . /usr/local/opt/simple-python-server
```

#### uv

The plist uses `uv run` by default, which automatically manages dependencies. Adjust the `uv` path if needed:

```sh
# Confirm your uv path
which uv

# Edit PORT/HOSTNAME and uv path in the plist if needed, then install
cp com.simple-python-server.plist ~/Library/LaunchAgents/

# macOS 13+
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.simple-python-server.plist
# macOS 12 and earlier
launchctl load ~/Library/LaunchAgents/com.simple-python-server.plist
```

#### pip

If you prefer pip, replace `ProgramArguments` in the plist with the venv Python after running `pip install`:

```xml
<key>ProgramArguments</key>
<array>
    <string>/usr/local/opt/simple-python-server/.venv/bin/python3</string>
    <string>server.py</string>
</array>
```

```sh
cd /usr/local/opt/simple-python-server
python3 -m venv --prompt simple-python-server .venv
.venv/bin/pip install -r requirements.txt
```

#### Manage the service:

**macOS 13+ (Ventura and later) — use `bootstrap`/`bootout`:**

```sh
# Install (load and enable at login)
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.simple-python-server.plist

# Uninstall
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.simple-python-server.plist

# Start / stop without unloading
launchctl kickstart gui/$(id -u)/com.simple-python-server
launchctl kill SIGTERM gui/$(id -u)/com.simple-python-server

# Reload after editing the plist
launchctl bootout   gui/$(id -u) ~/Library/LaunchAgents/com.simple-python-server.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.simple-python-server.plist

# Status
launchctl print gui/$(id -u)/com.simple-python-server
```

**macOS 12 and earlier — use `load`/`unload`:**

```sh
# Install
launchctl load ~/Library/LaunchAgents/com.simple-python-server.plist

# Uninstall
launchctl unload ~/Library/LaunchAgents/com.simple-python-server.plist

# Start / stop
launchctl start com.simple-python-server
launchctl stop  com.simple-python-server

# Status
launchctl list | grep simple-python-server
```

**Logs (both):**

```sh
tail -f /usr/local/opt/simple-python-server/logs/stdout.log
tail -f /usr/local/opt/simple-python-server/logs/stderr.log
```

## Development

### uv

```sh
uv sync
uv run server.py
```

### pip

```sh
python3 -m venv --prompt simple-python-server .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```
