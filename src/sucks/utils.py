import podman

def container_exists(name: str) -> bool:
    with podman.PodmanClient() as client:
        for container in client.containers.list():
            if container.name == name:
                return True
    return False