import podman
import logging

from podman.domain.containers import Container
from sucks.models import ContainerDefinition
from typing import Dict, List

class ContainerManger:
    _defintion: ContainerDefinition
    _client: podman.PodmanClient
    _logger: logging.Logger

    @property
    def _container(self) -> Container:
        return self._client.containers.get(self._defintion.container_name)

    def _parse_volume_strs(self, vols: List[str]) -> Dict[str, object]:
        output = {}

        for vol in vols:
            vol_args = vol.split(':')

            if len(vol_args) < 2 or len(vol_args) > 3:
                self._logger.warning(f"Volume string {vol} does not match expected format, skipping")
                continue
            
            host_dir = vol_args[0]
            container_dir = vol_args[1]
            extended_opts = []
            if len(vol_args) == 3:
                extended_opts = vol_args[2].split(',')

            output[host_dir] = {
                'bind': container_dir,
                'extended_mode': extended_opts,
            }
        return output

    def __init__(self, container_def: ContainerDefinition, client: podman.PodmanClient):
        self._defintion = container_def
        self._client = client
        self._logger = logging.getLogger("sucks")

    def exists(self) -> bool:
        return self._client.containers.exists(self._defintion.container_name)

    def kill(self) -> bool:
        try:
            self._container.kill()
        except podman.errors.APIError as e:
            return False
        return True

    def pull(self) -> bool:
        try:
            self._client.images.pull(self._defintion.image)
        except podman.errors.APIError as e:
            self._logger.info(e)
            return False
        return True

    def create(self, privileged: bool = False, volumes: List[str] = []) -> bool:
        try:
            self._client.containers.create(
                self._defintion.image,
                name=self._defintion.container_name,
                auto_remove=True,
                privileged=privileged,
                volumes=self._parse_volume_strs(volumes)
            ).start()
        except podman.errors.APIError as e:
            self._logger.info(e)
            return False
        return True
