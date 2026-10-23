import math
from collections.abc import Iterable
from functools import lru_cache

from pydantic import BaseModel, Field

from common_types import EulerAngle, PositiveFloat, PositiveInt

Matrix3 = tuple[tuple[float, float, float], ...]

MIN_DEPTH = 10.0
MIN_ZOOM = 0.03
MAX_ZOOM = 4.0
DEFAULT_YAW = 35.0
DEFAULT_PITCH = 55.0
DEFAULT_ROLL = 0.0


def _mat_mul(a: Matrix3, b: Matrix3) -> Matrix3:
    def cell(i: int, j: int) -> float:
        return sum(a[i][k] * b[k][j] for k in range(3))

    return (
        (cell(0, 0), cell(0, 1), cell(0, 2)),
        (cell(1, 0), cell(1, 1), cell(1, 2)),
        (cell(2, 0), cell(2, 1), cell(2, 2)),
    )


@lru_cache(maxsize=256)
def euler_matrix(yaw: float, pitch: float, roll: float) -> Matrix3:
    """
    World -> camera rotation matrix, R = R_roll . R_pitch . R_yaw.

    Camera frame (right-handed): x = right, y = up, z = towards viewer.
      - YAW   : turntable rotation around the world Z axis.
      - PITCH : elevation. 0 deg = top-down view, 90 deg = horizon view.
      - ROLL  : rotation around the viewing axis (screen rotation).
    """
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))

    r_yaw: Matrix3 = ((cy, -sy, 0.0), (sy, cy, 0.0), (0.0, 0.0, 1.0))
    r_pitch: Matrix3 = ((1.0, 0.0, 0.0), (0.0, cp, sp), (0.0, -sp, cp))
    r_roll: Matrix3 = ((cr, -sr, 0.0), (sr, cr, 0.0), (0.0, 0.0, 1.0))
    return _mat_mul(r_roll, _mat_mul(r_pitch, r_yaw))


class Camera3D(BaseModel):
    """
    3D camera driven by Euler angles (yaw, pitch, roll) with perspective
    projection. Validated by Pydantic V2; supports (x, y, z) points.
    """

    model_config = {"validate_assignment": True}

    screen_w: PositiveInt = Field(default=800)
    screen_h: PositiveInt = Field(default=600)

    yaw: EulerAngle = Field(default=DEFAULT_YAW)
    pitch: EulerAngle = Field(default=DEFAULT_PITCH)
    roll: EulerAngle = Field(default=DEFAULT_ROLL)

    focal: PositiveFloat = Field(default=650.0)
    zoom: PositiveFloat = Field(default=1.0)

    pan_x: float = 0.0
    pan_y: float = 0.0
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0

    @property
    def center_x(self) -> int:
        return self.screen_w // 2

    @property
    def center_y(self) -> int:
        return self.screen_h // 2

    @property
    def is_upside_down(self) -> bool:
        """True when the world 'up' axis points down on the screen."""
        return euler_matrix(self.yaw, self.pitch, self.roll)[1][2] < 0

    def update_screen_size(self, width: int, height: int) -> None:
        """Updates screen dimensions on window resize."""
        self.screen_w = width
        self.screen_h = height

    def reset_angles(self) -> None:
        self.yaw = DEFAULT_YAW
        self.pitch = DEFAULT_PITCH
        self.roll = DEFAULT_ROLL

    def rotate(
        self, x: float, y: float, z: float = 0.0
    ) -> tuple[float, float, float]:
        """Rotates a world vector into the camera frame (no zoom/pan)."""
        m = euler_matrix(self.yaw, self.pitch, self.roll)
        return (
            m[0][0] * x + m[0][1] * y + m[0][2] * z,
            m[1][0] * x + m[1][1] * y + m[1][2] * z,
            m[2][0] * x + m[2][1] * y + m[2][2] * z,
        )

    def project(
        self, x: float, y: float, z: float = 0.0
    ) -> tuple[int, int, float, bool]:
        """
        Projects a 3D point to (screen_x, screen_y, scale, is_visible).
        A bigger scale means the point is closer to the viewer.
        """
        x_c, y_c, z_c = self.rotate(
            (x - self.position_x) * self.zoom,
            (y - self.position_y) * self.zoom,
            (z - self.position_z) * self.zoom,
        )

        depth = self.focal - z_c
        is_visible = depth > MIN_DEPTH
        depth = max(MIN_DEPTH, depth)

        scale = self.focal / depth
        screen_x = round(self.center_x + x_c * scale + self.pan_x)
        screen_y = round(self.center_y - y_c * scale + self.pan_y)
        return screen_x, screen_y, scale, is_visible

    def _screen_bounds(
        self, points: list[tuple[float, float, float]]
    ) -> tuple[int, int, int, int]:
        pts = [self.project(*p)[:2] for p in points]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return min(xs), max(xs), min(ys), max(ys)

    def fit_to_points(
        self,
        points: Iterable[tuple[float, float, float]],
        padding: int = 110,
    ) -> None:
        """Frames the points (and the origin) inside the window."""
        pts = list(points)
        if not pts:
            return
        pts.append((0.0, 0.0, 0.0))
        self.position_x = self.position_y = self.position_z = 0.0
        avail_w = max(100.0, self.screen_w - 2 * padding)
        avail_h = max(100.0, self.screen_h - 2 * padding)

        # Perspective slightly depends on zoom: two passes are enough.
        self.zoom = 1.0
        for _ in range(2):
            self.pan_x = self.pan_y = 0.0
            min_x, max_x, min_y, max_y = self._screen_bounds(pts)
            factor = min(
                avail_w / max(max_x - min_x, 1),
                avail_h / max(max_y - min_y, 1),
            )
            self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom * factor))

        self.pan_x = self.pan_y = 0.0
        min_x, max_x, min_y, max_y = self._screen_bounds(pts)
        self.pan_x = self.screen_w / 2 - (min_x + max_x) / 2
        self.pan_y = self.screen_h / 2 - (min_y + max_y) / 2

    def zoom_by(self, factor: float) -> None:
        self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom * factor))

    def pan(self, dx: float, dy: float) -> None:
        self.pan_x += dx
        self.pan_y += dy

    def move_local(
        self,
        forward: float = 0.0,
        right: float = 0.0,
        up: float = 0.0,
        speed: float = 1.0,
    ) -> None:
        """Moves the camera relative to the view direction (yaw only)."""
        yaw_rad = math.radians(self.yaw)
        # World directions that appear "up" / "right" on screen.
        fwd_x, fwd_y = math.sin(yaw_rad), math.cos(yaw_rad)
        right_x, right_y = math.cos(yaw_rad), -math.sin(yaw_rad)
        self.position_x += (fwd_x * forward + right_x * right) * speed
        self.position_y += (fwd_y * forward + right_y * right) * speed
        self.position_z += up * speed
