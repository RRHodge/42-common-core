import pygame

from camera_3d import Camera3D

AXES = (
    ("X", (1.0, 0.0, 0.0), (255, 60, 60)),
    ("Y", (0.0, 1.0, 0.0), (60, 255, 60)),
    ("Z", (0.0, 0.0, 1.0), (60, 160, 255)),
)


def draw_3d_gizmo(
    screen: pygame.Surface,
    camera: Camera3D,
    pos_x: int = 930,
    pos_y: int = 100,
    axis_len: int = 35,
) -> None:
    """Draws the X (red) / Y (green) / Z (blue) axes seen by the camera."""
    pygame.draw.circle(screen, (20, 25, 45), (pos_x, pos_y), axis_len + 15)
    pygame.draw.circle(
        screen, (0, 200, 255), (pos_x, pos_y), axis_len + 15, 1
    )
    font = pygame.font.SysFont("Consolas", 11, bold=True)
    # Far axes first so the closest one is drawn on top.
    projected = []
    for label, (ax, ay, az), color in AXES:
        x_c, y_c, z_c = camera.rotate(ax * axis_len, ay * axis_len,
                                      az * axis_len)
        projected.append((z_c, label, color, x_c, y_c))
    for _, label, color, x_c, y_c in sorted(projected):
        end = (round(pos_x + x_c), round(pos_y - y_c))
        pygame.draw.line(screen, color, (pos_x, pos_y), end, 3)
        text = font.render(label, True, color)
        screen.blit(text, (end[0] + 3, end[1] - 6))
