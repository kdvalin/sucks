import pytest
from unittest.mock import MagicMock, patch

from sucks.models.container_file import ContainerDefinition
from sucks.utils.container import ContainerManager


@pytest.fixture
def definition():
    return ContainerDefinition(image="ubuntu:24.04", filename="test")


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture
def manager(definition, client):
    return ContainerManager(definition, client)


class TestParseVolumeStrs:
    def test_none_returns_empty(self, manager):
        assert manager._parse_volume_strs(None) == {}

    def test_empty_list_returns_empty(self, manager):
        assert manager._parse_volume_strs([]) == {}

    def test_simple_volume(self, manager):
        result = manager._parse_volume_strs(["/host/path:/container/path"])
        assert result == {
            "/host/path": {"bind": "/container/path", "extended_mode": []}
        }

    def test_volume_with_options(self, manager):
        result = manager._parse_volume_strs(["/host/path:/container/path:ro,z"])
        assert result == {
            "/host/path": {"bind": "/container/path", "extended_mode": ["ro", "z"]}
        }

    def test_invalid_volume_skipped(self, manager):
        result = manager._parse_volume_strs(["/only/one/part"])
        assert result == {}

    def test_multiple_volumes(self, manager):
        result = manager._parse_volume_strs([
            "/host/a:/container/a",
            "/host/b:/container/b:ro",
        ])
        assert "/host/a" in result
        assert "/host/b" in result


class TestExists:
    def test_delegates_to_client(self, manager, client):
        client.containers.exists.return_value = True
        assert manager.exists() is True
        client.containers.exists.assert_called_once_with("sucks-test")

    def test_returns_false_when_not_exists(self, manager, client):
        client.containers.exists.return_value = False
        assert manager.exists() is False


class TestExec:
    def test_basic_exec(self, manager):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            rc = manager.exec(["echo", "hello"])
            assert rc == 0
            args = mock_run.call_args[0][0]
            assert args == ["podman", "exec", "sucks-test", "echo", "hello"]

    def test_exec_with_tty(self, manager):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            manager.exec(["bash"], tty=True)
            args = mock_run.call_args[0][0]
            assert "-t" in args

    def test_exec_with_interactive(self, manager):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            manager.exec(["bash"], interactive=True)
            args = mock_run.call_args[0][0]
            assert "-i" in args

    def test_exec_with_workdir(self, manager):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            manager.exec(["ls"], workdir="/opt")
            args = mock_run.call_args[0][0]
            assert "-w" in args
            assert "/opt" in args

    def test_exec_returns_nonzero_on_failure(self, manager):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            rc = manager.exec(["false"])
            assert rc == 1
