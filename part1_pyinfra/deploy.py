""" Deploy flask app + systemd service """

from pyinfra.operations import apt, server, systemd, files

# flask app deploy
apt.packages(
    name="Ensure the python3 package is installed",
    packages=["python3", "curl"],
)

server.shell(
    name="install uv", commands="curl -LsSf https://astral.sh/uv/install.sh | sh"
)

files.directory(path="/app", name="create app directory", user="root")
files.put(
    src="part1_pyinfra/metrics_collector.py",
    dest="/app/metrics_collector.py",
    user="root",
)
server.shell(
    name="Create virtualenv",
    commands="~/.local/bin/uv venv --clear",
)
server.shell(
    name="Install dependencies",
    commands="~/.local/bin/uv pip install flask",
)


# systemd service deploy
files.put(
    src="part1_pyinfra/metrics-collector.service",
    dest="/etc/systemd/system/metrics-collector.service",
    user="root",
)

systemd.daemon_reload(name="reload daemon")

systemd.service(
    name="Restart and enable metrics_collector service",
    service="metrics-collector.service",
    running=True,
    restarted=True,
    enabled=True,
)
