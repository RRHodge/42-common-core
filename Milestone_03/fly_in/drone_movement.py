from pydantic import BaseModel

from common_types import NonEmptyStr


class DroneMovement(BaseModel):
    """A drone movement during one simulation turn."""

    drone_id: NonEmptyStr
    destination: NonEmptyStr

    def to_stdout_format(self) -> str:
        """Official output format: D<ID>-<dest>"""
        return f"{self.drone_id}-{self.destination}"
