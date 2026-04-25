"""Host list"""

# docker_hosts = [
#     ("server1", {"ssh_hostname": "localhost", "ssh_port": 2221, "ssh_user": "root"}),
#     ("server2", {"ssh_hostname": "localhost", "ssh_port": 2222, "ssh_user": "root"}),
# ]

wls_hosts = [
    (
        "server1",
        {"ssh_hostname": "172.18.50.179", "ssh_user": "root", "ssh_port": 2222},
    ),
    (
        "server2",
        {"ssh_hostname": "172.18.50.179", "ssh_user": "root", "ssh_port": 2221},
    ),
]
