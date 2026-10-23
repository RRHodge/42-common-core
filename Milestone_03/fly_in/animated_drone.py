from drone_type import DroneType
from zone import Zone


class AnimatedDrone:
    """
    Drone animated along the timed plan computed by the Router.

    One plan entry per action: a repeated hub = one turn of waiting, a
    move into a restricted zone lasts 2 turns, any other move 1 turn.
    All drones share the same clock (in turns) so that the router's
    reservations stay valid on screen.
    """

    def __init__(
        self,
        drone_id: int,
        drone_type: DroneType,
        path: list[Zone],
        scale: float = 1.0,
    ) -> None:
        self.drone_id = drone_id
        self.color_name = drone_type.value
        self.points = [(z.x * scale, z.y * scale, z.z * scale)
                       for z in path]

        # segments[i] = (t_start, t_end) of the move path[i-1] -> path[i]
        self.segments: list[tuple[float, float]] = [(0.0, 0.0)]
        elapsed = 0.0
        for prev, node in zip(path, path[1:]):
            duration = 1.0 if node.name == prev.name \
                else float(node.travel_turns)
            self.segments.append((elapsed, elapsed + duration))
            elapsed += duration
        self.total_turns = elapsed

        self.curr_x, self.curr_y, self.curr_z = \
            self.points[0] if self.points else (0.0, 0.0, 0.0)
        self.direction_col = 0  # 0 right, 1 left, 2 up, 3 down

    def update(self, sim_turn: float) -> None:
        """Places the drone at time sim_turn (fractional turns)."""
        pts = self.points
        if len(pts) < 2:
            return
        if sim_turn >= self.total_turns:
            self.curr_x, self.curr_y, self.curr_z = pts[-1]
            return

        for i in range(1, len(pts)):
            t0, t1 = self.segments[i]
            if t0 <= sim_turn < t1:
                start, end = pts[i - 1], pts[i]
                t = (sim_turn - t0) / (t1 - t0)
                break
        else:
            return

        self.curr_x = start[0] + (end[0] - start[0]) * t
        self.curr_y = start[1] + (end[1] - start[1]) * t
        self.curr_z = start[2] + (end[2] - start[2]) * t

        dx, dy = end[0] - start[0], end[1] - start[1]
        if dx == 0 and dy == 0:
            return  # waiting: keep the last direction
        if abs(dx) > abs(dy):
            self.direction_col = 0 if dx > 0 else 1
        else:
            self.direction_col = 2 if dy > 0 else 3  # +y is up on screen
