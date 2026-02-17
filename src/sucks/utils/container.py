import podman
from sucks.models import ContainerDefinition

class ContainerManger:
    _defintion: ContainerDefinition
    _client: podman.PodmanClient

    def __init__(self, container_def: ContainerDefinition, client: podman.PodmanClient):
        self._defintion = container_def
        self._client = client

    @property
    def _container(self) -> podman.domain.containers.Container:
        return self._client.containers.get(self._defintion.container_name)

    def exists(self) -> bool:
        return self._client.containers.exists(self._defintion.container_name)

    def kill(self) -> bool:
        try:
            self._container.kill()
        except podman.errors.APIError as e:
            return False
        return True
