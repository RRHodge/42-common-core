import os

import pygame

from drone_type import DroneType

SPRITE_PATHS = (
    "assets/PacManAssets-Ghosts.png",
    "assets/pacman/PacManAssets-Ghosts.png",
    "PacManAssets-Ghosts.png",
    "../assets/PacManAssets-Ghosts.png",
)

FALLBACK_COLORS: dict[str, tuple[int, int, int]] = {
    DroneType.BLINKY.value: (255, 0, 0),
    DroneType.PINKY.value: (255, 184, 255),
    DroneType.INKY.value: (0, 255, 255),
    DroneType.CLYDE.value: (255, 184, 82),
}


class GhostSpriteManager:
    """
    Loads PacManAssets-Ghosts.png and slices the sprites.
    Falls back to vector drawing when the file is missing.
    """

    def __init__(self) -> None:
        self.sprites: dict[tuple[str, int], pygame.Surface] = {}
        self.has_real_assets = False
        self._load_assets()

    def _load_assets(self) -> None:
        found_path = next((p for p in SPRITE_PATHS if os.path.exists(p)),
                          None)
        if found_path is None:
            return
        try:
            sheet = pygame.image.load(found_path).convert_alpha()
            frame_w = sheet.get_width() // 4
            frame_h = sheet.get_height() // 10
            # Columns: 0 right, 1 left, 2 up, 3 down.
            for row, drone_type in enumerate(DroneType):
                for col in range(4):
                    rect = pygame.Rect(col * frame_w, row * frame_h,
                                       frame_w, frame_h)
                    self.sprites[(drone_type.value, col)] = \
                        sheet.subsurface(rect)
            self.has_real_assets = True
            print(f"[ASSETS] Fichier chargé : {found_path}")
        except (pygame.error, OSError) as err:
            print(f"[ASSETS] Erreur lors du chargement des sprites ({err}).")

    def get_ghost_sprite(
        self,
        color_name: str,
        direction_col: int,
        target_size: int,
        flip_vert: bool = False,
    ) -> pygame.Surface:
        size = max(8, int(target_size))
        if self.has_real_assets and (color_name, direction_col) \
                in self.sprites:
            base = self.sprites[(color_name, direction_col)]
            surf = pygame.transform.smoothscale(base, (size, size))
        else:
            surf = self._draw_fallback(color_name, direction_col, size)
        if flip_vert:
            surf = pygame.transform.flip(surf, False, True)
        return surf

    @staticmethod
    def _draw_fallback(
        color_name: str, direction_col: int, size: int
    ) -> pygame.Surface:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        rgb = FALLBACK_COLORS.get(color_name, (255, 0, 0))
        radius = size // 2
        pygame.draw.circle(surf, rgb, (radius, radius), radius)
        pygame.draw.rect(surf, rgb, (0, radius, size, radius))

        off_x, off_y = [(2, 0), (-2, 0), (0, -2), (0, 2)][direction_col]
        eye_r = max(2, size // 5)
        pupil_r = max(1, eye_r // 2)
        for ex in (radius - radius // 2, radius + radius // 2):
            ey = radius - radius // 4
            pygame.draw.circle(surf, (255, 255, 255), (ex, ey), eye_r)
            pygame.draw.circle(surf, (0, 0, 200),
                               (ex + off_x, ey + off_y), pupil_r)
        return surf
