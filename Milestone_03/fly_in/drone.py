from pydantic import BaseModel, Field

from common_types import NonEmptyStr


class Drone(BaseModel):
    id: NonEmptyStr
    current_position: str = "start"
    transit_remaining_turns: int = Field(default=0, ge=0)
    assigned_path: list[str] = Field(default_factory=list)
    path_index: int = Field(default=0, ge=0)
