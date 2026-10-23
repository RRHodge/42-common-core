from pydantic import BaseModel, Field

from common_types import PositiveInt
from drone_movement import DroneMovement


class TurnResult(BaseModel):
    """Complete result of a simulation turn."""

    turn_number: PositiveInt
    movements: list[DroneMovement] = Field(default_factory=list)

    @property
    def stdout_line(self) -> str:
        return " ".join(m.to_stdout_format() for m in self.movements)
