import podman
from sucks.models import ContainerDefinition

class ContainerManger:
    _defintion: ContainerDefinition
    _client: podman.PodmanClient

    def __init__(self, container_def: ContainerDefinition, client: podman.PodmanClient):
        self._defintion = container_def
        self._client = client

    def exists(self) -> bool:
        return self._client.containers.exists(self._defintion.container_name)
