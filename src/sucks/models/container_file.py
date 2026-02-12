import pydantic

from typing import List

class ContainerDefinition(pydantic.BaseModel):
    name: str = pydantic.Field(help="A human readable name for the container", default=None)
    image: str = pydantic.Field(help="The container to be used for this, needs to have a systemd entrypoint")
    initSteps: List[str] = pydantic.Field(help="List of initialization steps to be ran at startup", default=[])
    filename: str = pydantic.Field(help="The name of the file these details were sourced from, if this is not set something went _very_ wrong")
