import pytest
from pydantic import ValidationError

from sucks.models.container_file import ContainerDefinition


def make_definition(**kwargs) -> ContainerDefinition:
    defaults = {
        "image": "registry.access.redhat.com/ubi9-init",
        "filename": "test",
    }
    defaults.update(kwargs)
    return ContainerDefinition(**defaults)


class TestContainerDefinition:
    def test_minimal_valid(self):
        defn = make_definition()
        assert defn.image == "registry.access.redhat.com/ubi9-init"
        assert defn.filename == "test"

    def test_image_required(self):
        with pytest.raises(ValidationError):
            ContainerDefinition(filename="test")

    def test_filename_required(self):
        with pytest.raises(ValidationError):
            ContainerDefinition(image="registry.access.redhat.com/ubi9-init")

    def test_init_steps_default_empty(self):
        defn = make_definition()
        assert defn.initSteps == []

    def test_ci_steps_default_empty(self):
        defn = make_definition()
        assert defn.ciSteps == []

    def test_workdir_default_none(self):
        defn = make_definition()
        assert defn.workdir is None

    def test_name_default_none(self):
        defn = make_definition()
        assert defn.name is None

    def test_container_name(self):
        defn = make_definition(filename="myenv")
        assert defn.container_name == "sucks-myenv"

    def test_image_name_no_tag(self):
        defn = make_definition(image="registry.access.redhat.com/ubi9-init")
        assert defn.image_name == "registry.access.redhat.com/ubi9-init"

    def test_image_name_with_tag(self):
        defn = make_definition(image="ubuntu:24.04")
        assert defn.image_name == "ubuntu"

    def test_image_tag_explicit(self):
        defn = make_definition(image="ubuntu:24.04")
        assert defn.image_tag == "24.04"

    def test_image_tag_defaults_to_latest(self):
        defn = make_definition(image="registry.access.redhat.com/ubi9-init")
        assert defn.image_tag == "latest"

    def test_init_steps_populated(self):
        defn = make_definition(initSteps=["dnf install -y git", "dnf install -y jq"])
        assert defn.initSteps == ["dnf install -y git", "dnf install -y jq"]

    def test_ci_steps_populated(self):
        defn = make_definition(ciSteps=["echo hello", "exit 0"])
        assert defn.ciSteps == ["echo hello", "exit 0"]
