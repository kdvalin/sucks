import pydantic

from typing import List

class ContainerDefinition(pydantic.BaseModel):
    name: str = pydantic.Field(description="A human readable name for the container", default=None)
    image: str = pydantic.Field(description="The container to be used for this, needs to have a systemd entrypoint")
    initSteps: List[str] = pydantic.Field(description="List of initialization steps to be ran at startup", default=[])
    filename: str = pydantic.Field(description="The name of the file these details were sourced from, if this is not set something went _very_ wrong")
    ciSteps: List[str]  = pydantic.Field(description="List of initialization steps to be ran when the ci command is invoked", default=[])
    workdir: str = pydantic.Field(description="Sets the default working directory of setup, run, shell, and ci can be overriden with -w/--workdir", default=None)

    @property
    def container_name(self):
        return f"sucks-{self.filename}"
    
    @property
    def image_name(self) -> str:
        return self.image.split(':')[0]
    
    @property
    def image_tag(self) -> str:
        image_split = self.image.split(':')

        if len(image_split) > 1:
            return image_split[1]
        return "latest"
