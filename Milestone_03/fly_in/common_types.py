from typing import Annotated
from pydantic import Field, AfterValidator


def normalize_angle(angle: float) -> float:
    """Keeps Euler angles bounded within [0.0, 360.0)."""
    return angle % 360.0


def validate_clean_zone_name(value: str) -> str:
    """Ensures a zone name is non-empty and contains no spaces or hyphens."""
    if not value or not value.strip():
        raise ValueError("Zone name cannot be empty.")
    if any(char in value for char in {"-", " "}):
        raise ValueError(
            "Zone name cannot contain spaces or dashes."
        )
    return value.strip()


# --- Reusable Pydantic V2 Type Aliases ---
PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0.0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]
CleanZoneName = Annotated[str, AfterValidator(validate_clean_zone_name)]
EulerAngle = Annotated[float, AfterValidator(normalize_angle)]
