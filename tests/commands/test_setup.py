from unittest.mock import MagicMock, patch
import types
import pytest

from sucks.models.container_file import ContainerDefinition
from sucks.utils import ContainerManager, SucksException
from sucks.commands.setup import Setup

@pytest.fixture
def container():
    return MagicMock()

@pytest.fixture
def conman():
    return MagicMock()

class TestSetup:
    @pytest.mark.parametrize('privs,vols', [
        (True, ["a","b","c"]),
        (False, ["a","b","c"]),
        (True, []),
        (False, [])
    ])
    def test_bare_setup(self, conman, container, privs, vols):
        conman.exists = MagicMock(return_value=False)
        conman.pull = MagicMock(return_value=True)
        conman.create = MagicMock(return_value=True)

        container.initSteps = []

        setup_args = types.SimpleNamespace(
            conman=conman,
            pull="missing",
            privileged=privs,
            volume=vols,
            container=container
        )
        Setup().run_command(setup_args, None)

        assert conman.exists.called
        conman.pull.assert_called_once_with("missing")
        conman.create.assert_called_once_with(privileged=privs, volumes=vols)

    def test_container_exists(self, conman, container):
        conman.exists = MagicMock(return_value=True)
        container.container_name = "ubuntu"
        setup_args = types.SimpleNamespace(
            conman=conman,
            pull="missing",
            privileged=False,
            volume=[],
            container=container
        )
        with pytest.raises(SucksException):
            Setup().run_command(setup_args, None)

        assert conman.exists.called

    def test_setup_failed_pull(self, conman, container):
        conman.exists = MagicMock(return_value=False)
        conman.pull = MagicMock(return_value=False)

        container.image = "ubuntu:24.04"

        setup_args = types.SimpleNamespace(
            conman=conman,
            pull="missing",
            privileged=False,
            volume=[],
            container=container
        )
        with pytest.raises(SucksException):
            Setup().run_command(setup_args, None)
        assert conman.exists.called
        conman.pull.assert_called_once_with("missing")
