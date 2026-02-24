from unittest.mock import MagicMock, patch
import types
import pytest

from sucks.models.container_file import ContainerDefinition
from sucks.utils.container import ContainerManager
from sucks.commands.setup import Setup

@pytest.fixture
def container():
    return MagicMock()

@pytest.fixture
def conman():
    return MagicMock()

class TestSetup:
    def test_bare_setup(self):
        conman.exists = MagicMock(return_value=False)
        conman.pull = MagicMock(return_value=True)
        conman.create = MagicMock(return_value=True)

        container.initSteps = []

        setup_args = types.SimpleNamespace(
            conman=conman,
            pull="missing",
            privileged=False,
            volume=[],
            container=container
        )
        Setup().run_command(setup_args, None)

        assert conman.exists.called
        conman.pull.assert_called_once_with("missing")
        conman.create.assert_called_once_with(privileged=False, volumes=[])
