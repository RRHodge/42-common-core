from pydantic import BaseModel, ConfigDict, Field

from common_types import CleanZoneName, PositiveInt
from zone_type import ZoneType


class Zone(BaseModel):
    """A hub of the drone network (2D or 3D)."""

    model_config = ConfigDict(populate_by_name=True)

    name: CleanZoneName
    x: int
    y: int
    z: int = 0
    zone_type: ZoneType = Field(default=ZoneType.NORMAL, alias="zone")
    color: str = "none"
    max_drones: PositiveInt = 1

    @property
    def is_blocked(self) -> bool:
        return self.zone_type == ZoneType.BLOCKED

    @property
    def travel_turns(self) -> int:
        """Turns needed to enter this zone (single source of truth)."""
        return 2 if self.zone_type == ZoneType.RESTRICTED else 1
