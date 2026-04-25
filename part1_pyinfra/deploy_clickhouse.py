""" Deploy clickhouse yaml config to server"""

from pyinfra.operations import files

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
