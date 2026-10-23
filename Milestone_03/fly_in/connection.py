from pydantic import BaseModel, Field

from common_types import CleanZoneName


class Connection(BaseModel):
    """Bidirectional link between two zones."""

    from_zone: CleanZoneName
    to_zone: CleanZoneName
    max_link_capacity: int = Field(default=1, gt=0)
