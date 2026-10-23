"""
FLY-IN : rendu 3D (caméra Euler : yaw / pitch / roll).

Contrôles : clic gauche = yaw + pitch, clic droit = roll, molette = zoom,
clic molette = déplacement, WASD/QE = caméra, G = grille, Espace = reset.
"""
import argparse
import sys
from pathlib import Path

try:
    import pygame
except ImportError:
    print("[ERREUR] Pygame n'est pas installé sur ce système.")
    sys.exit(1)

from animated_drone import AnimatedDrone
from camera_3d import Camera3D
from drone_type import DroneType
from ghost_sprite_manager import GhostSpriteManager
from gizmo import draw_3d_gizmo
from map_parser import MapParser
from router import Router
from zone import Zone

# Map coordinates are small integers: spread them into "world" units.
WORLD_SCALE = 100
HUB_COLORS: dict[str, tuple[int, int, int]] = {
    "green": (0, 255, 100), "red": (255, 70, 70), "blue": (0, 180, 255),
    "yellow": (255, 230, 60), "orange": (255, 150, 40),
    "purple": (160, 90, 230), "violet": (190, 110, 255),
    "cyan": (0, 230, 230), "lime": (170, 255, 60),
    "gold": (255, 200, 40), "magenta": (255, 60, 200),
    "crimson": (220, 30, 70), "darkred": (150, 20, 20),
    "maroon": (130, 40, 60), "brown": (150, 100, 60),
    "black": (60, 60, 70), "rainbow": (255, 120, 220),
}
TURNS_PER_SECOND = 1.5
END_PAUSE_TURNS = 2.0
FPS = 60
MOUSE_SENSITIVITY = 0.5
KEY_ROTATION_STEP = 2.0
DEFAULT_MAP = "maps/challenger/01_the_impossible_dream.txt"

Bounds = tuple[float, float, float, float]


def world_pos(zone: Zone) -> tuple[float, float, float]:
    return (zone.x * WORLD_SCALE, zone.y * WORLD_SCALE,
            zone.z * WORLD_SCALE)


def parse_map_path() -> Path:
    default_map = Path(__file__).resolve().parent / DEFAULT_MAP
    parser = argparse.ArgumentParser(description="Interface graphique Fly-In")
    parser.add_argument("map", nargs="?", default=str(default_map),
                        help="Chemin du fichier carte")
    args, _ = parser.parse_known_args()
    return Path(args.map).resolve()


def map_bounds(hubs: dict[str, Zone]) -> Bounds:
    """(min_x, max_x, min_y, max_y) in world units, origin included."""
    xs = [0.0] + [world_pos(h)[0] for h in hubs.values()]
    ys = [0.0] + [world_pos(h)[1] for h in hubs.values()]
    return min(xs), max(xs), min(ys), max(ys)


def draw_line_3d(
    screen: pygame.Surface,
    camera: Camera3D,
    color: tuple[int, int, int],
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    width: int = 1,
) -> None:
    x1, y1, _, v1 = camera.project(*start)
    x2, y2, _, v2 = camera.project(*end)
    if v1 or v2:
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)


def draw_grid(
    screen: pygame.Surface, camera: Camera3D, bounds: Bounds
) -> None:
    min_x, max_x, min_y, max_y = bounds
    extent = max(max_x - min_x, max_y - min_y, 1)
    step = max(70, int(extent / 12))
    gx0, gx1 = int(min_x) - step, int(max_x) + step
    gy0, gy1 = int(min_y) - step, int(max_y) + step
    color = (20, 40, 70)
    for gx in range(gx0, gx1 + 1, step):
        draw_line_3d(screen, camera, color, (gx, gy0, 0), (gx, gy1, 0))
    for gy in range(gy0, gy1 + 1, step):
        draw_line_3d(screen, camera, color, (gx0, gy, 0), (gx1, gy, 0))


def draw_origin(
    screen: pygame.Surface,
    camera: Camera3D,
    font: pygame.font.Font,
    bounds: Bounds,
) -> None:
    min_x, max_x, min_y, max_y = bounds
    axis_color = (170, 170, 190)
    draw_line_3d(screen, camera, axis_color, (min_x, 0, 0), (max_x, 0, 0), 2)
    draw_line_3d(screen, camera, axis_color, (0, min_y, 0), (0, max_y, 0), 2)
    ox, oy, _, visible = camera.project(0, 0, 0)
    if visible:
        pygame.draw.circle(screen, (255, 255, 255), (ox, oy), 6, 2)
        label = font.render("(0, 0, 0)", True, (255, 255, 255))
        screen.blit(label, (ox + 8, oy - 8))


def draw_connections(
    screen: pygame.Surface,
    camera: Camera3D,
    links: list[tuple[Zone, Zone]],
) -> None:
    for a, b in links:
        tower = "TOWER" in a.name or "TOWER" in b.name
        color = (0, 220, 255) if tower else (0, 150, 220)
        draw_line_3d(screen, camera, color, world_pos(a), world_pos(b), 2)


def draw_entities(
    screen: pygame.Surface,
    camera: Camera3D,
    font: pygame.font.Font,
    sprites: GhostSpriteManager,
    hubs: dict[str, Zone],
    drones: list[AnimatedDrone],
) -> None:
    """Painter's algorithm: farthest (smallest scale) is drawn first."""
    queue: list[tuple[float, int, int, Zone | AnimatedDrone]] = []
    for hub in hubs.values():
        sx, sy, scale, visible = camera.project(*world_pos(hub))
        if visible:
            queue.append((scale, sx, sy, hub))
    for drone in drones:
        sx, sy, scale, visible = camera.project(
            drone.curr_x, drone.curr_y, drone.curr_z)
        if visible:
            queue.append((scale, sx, sy, drone))
    queue.sort(key=lambda item: item[0])

    zoom_factor = min(camera.zoom, 1.5)
    for scale, sx, sy, obj in queue:
        if isinstance(obj, Zone):
            radius = max(4, int(18 * scale * zoom_factor))
            color = HUB_COLORS.get(obj.color, (0, 255, 200))
            pygame.draw.circle(screen, color, (sx, sy), radius)
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy), radius, 2)
            label = font.render(obj.name, True, (255, 255, 255))
            screen.blit(label, (sx - label.get_width() // 2,
                                sy + radius + 2))
        else:
            size = max(8, int(32 * scale * zoom_factor))
            sprite = sprites.get_ghost_sprite(
                obj.color_name, obj.direction_col, size,
                camera.is_upside_down)
            screen.blit(sprite, (sx - sprite.get_width() // 2,
                                 sy - sprite.get_height() // 2))


def draw_hud(
    screen: pygame.Surface,
    camera: Camera3D,
    clock: pygame.time.Clock,
    font_hud: pygame.font.Font,
    font_title: pygame.font.Font,
) -> None:
    hud = pygame.Surface((410, 145), pygame.SRCALPHA)
    hud.fill((10, 15, 30, 220))
    screen.blit(hud, (15, 15))
    pygame.draw.rect(screen, (0, 200, 255), (15, 15, 410, 145), 2)
    white, grey = (255, 255, 255), (200, 200, 200)
    info = [
        ("--- CAMÉRA 3D (EULER) ---", (0, 255, 200)),
        (f"YAW   (Axe Z)   : {camera.yaw:6.1f}°  [Flèches G/D, Clic-G]",
         white),
        (f"PITCH (Axe X)   : {camera.pitch:6.1f}°  [Flèches H/B, Clic-G]",
         white),
        (f"ROLL  (Axe vue) : {camera.roll:6.1f}°  [Clic-D]", white),
        (f"ZOOM  : {camera.zoom:.2f}x  |  FPS: {int(clock.get_fps())}",
         grey),
        ("W/S: avant/arrière | A/D: gauche/droite | Q/E: haut/bas", grey),
        ("Espace: Réinitialiser la vue | Échap: Quitter", grey),
    ]
    for i, (text, color) in enumerate(info):
        font = font_title if i == 0 else font_hud
        screen.blit(font.render(text, True, color), (25, 22 + i * 18))


def handle_mouse_motion(
    camera: Camera3D, mode: str, dx: int, dy: int
) -> None:
    if mode == "pan":
        camera.pan(dx, dy)
    elif mode == "yaw_pitch":
        camera.yaw += dx * MOUSE_SENSITIVITY
        camera.pitch -= dy * MOUSE_SENSITIVITY
    elif mode == "roll":
        camera.roll += dx * MOUSE_SENSITIVITY


def apply_held_keys(camera: Camera3D) -> None:
    keys = pygame.key.get_pressed()
    speed = 18.0 / max(camera.zoom, 0.03)
    if keys[pygame.K_w]:
        camera.move_local(forward=1.0, speed=speed)
    if keys[pygame.K_s]:
        camera.move_local(forward=-1.0, speed=speed)
    if keys[pygame.K_a]:
        camera.move_local(right=-1.0, speed=speed)
    if keys[pygame.K_d]:
        camera.move_local(right=1.0, speed=speed)
    if keys[pygame.K_q]:
        camera.move_local(up=-1.0, speed=speed)
    if keys[pygame.K_e]:
        camera.move_local(up=1.0, speed=speed)
    if keys[pygame.K_LEFT]:
        camera.yaw -= KEY_ROTATION_STEP
    if keys[pygame.K_RIGHT]:
        camera.yaw += KEY_ROTATION_STEP
    if keys[pygame.K_UP]:
        camera.pitch += KEY_ROTATION_STEP
    if keys[pygame.K_DOWN]:
        camera.pitch -= KEY_ROTATION_STEP


def run_template() -> None:
    map_path = parse_map_path()
    nb_drones, start_hub, end_hub, hubs, connections = \
        MapParser().parse_file(str(map_path))
    print(f"[MAP] Carte chargée : {map_path}")
    print(f"[MAP] Départ={start_hub}, arrivée={end_hub}, "
          f"drones={nb_drones}")

    router = Router(hubs, connections, start_hub, end_hub)
    paths_by_drone = router.plan_all_drones(nb_drones)

    types = list(DroneType)
    drones = [
        AnimatedDrone(
            i + 1, types[i % len(types)],
            [hubs[n] for n in paths_by_drone[f"D{i + 1}"]], WORLD_SCALE)
        for i in range(nb_drones)
    ]
    links = [(hubs[c.from_zone], hubs[c.to_zone]) for c in connections]
    bounds = map_bounds(hubs)
    fit_points = [world_pos(h) for h in hubs.values()]

    pygame.init()
    screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
    pygame.display.set_caption("Fly-in : caméra Euler 3D")
    clock = pygame.time.Clock()
    font_hud = pygame.font.SysFont("Consolas", 12, bold=True)
    font_title = pygame.font.SysFont("Arial", 15, bold=True)
    sprites = GhostSpriteManager()

    camera = Camera3D(screen_w=1024, screen_h=768)
    camera.fit_to_points(fit_points)

    sim_turn = 0.0
    drag_mode: str | None = None
    grid_visible = True
    last_mouse = (0, 0)
    drag_buttons = {1: "yaw_pitch", 2: "pan", 3: "roll"}
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                camera.update_screen_size(event.w, event.h)
                camera.fit_to_points(fit_points)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in drag_buttons:
                    drag_mode = drag_buttons[event.button]
                    last_mouse = event.pos
                elif event.button == 4:
                    camera.zoom_by(1.12)
                elif event.button == 5:
                    camera.zoom_by(1 / 1.12)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in drag_buttons:
                    drag_mode = None
            elif event.type == pygame.MOUSEMOTION and drag_mode:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                handle_mouse_motion(camera, drag_mode, dx, dy)
                last_mouse = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_g:
                    grid_visible = not grid_visible
                elif event.key == pygame.K_SPACE:
                    camera.reset_angles()
                    camera.fit_to_points(fit_points)

        apply_held_keys(camera)

        sim_turn += TURNS_PER_SECOND / FPS
        sim_end = max((d.total_turns for d in drones), default=0.0)
        if sim_turn > sim_end + END_PAUSE_TURNS:
            sim_turn = 0.0
        for drone in drones:
            drone.update(sim_turn)

        screen.fill((8, 10, 22))
        if grid_visible:
            draw_grid(screen, camera, bounds)
        draw_origin(screen, camera, font_hud, bounds)
        draw_connections(screen, camera, links)
        draw_entities(screen, camera, font_hud, sprites, hubs, drones)
        draw_3d_gizmo(screen, camera, pos_x=screen.get_width() - 70,
                      pos_y=75)
        draw_hud(screen, camera, clock, font_hud, font_title)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_template()
