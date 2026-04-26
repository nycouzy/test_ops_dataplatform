"""Deploy clickhouse yaml config to server"""

from pyinfra.operations import files, server

CLUSTER_NAME = "clickhouse-cluster"

# deploy clickhouse k8s config
files.directory(path="/clickhouse", name="create clickhouse directory", user="root")
files.put(
    src="part2_k8s_clickhouse/clickhouse-deployment.yaml",
    dest="/clickhouse/clickhouse-deployment.yaml",
    user="root",
)
files.put(
    src="part2_k8s_clickhouse/clickhouse-service.yaml",
    dest="/clickhouse/clickhouse-service.yaml",
    user="root",
)

files.put(
    src="part2_k8s_clickhouse/.env",
    dest="/clickhouse/.env",
    user="root",
)

server.shell(
    name=f"stop cluster: {CLUSTER_NAME} if running",
    commands=f"k3d cluster list | grep {CLUSTER_NAME} | grep running && k3d cluster stop {CLUSTER_NAME} || true",
)

server.shell(
    name="create / replace secret",
    commands="kubectl create secret generic clickhouse-secret --from-env-file=.env --dry-run=client -o yaml | kubectl replace -f -",
)

server.shell(
    name=f"start cluster: {CLUSTER_NAME}", commands=f"k3d cluster start {CLUSTER_NAME}"
)

server.shell(
    name="Apply StatefulSet",
    commands="kubectl apply -f /clickhouse/clickhouse-deployment.yaml",
)
server.shell(
    name="Apply Service",
    commands="kubectl apply -f /clickhouse/clickhouse-service.yaml",
)

server.shell(
    name="Port forwarding with nohup",
    commands="nohup kubectl port-forward svc/clickhouse 8123:8123 > /clickhouse/port-forward.log 2>&1 &",
)
