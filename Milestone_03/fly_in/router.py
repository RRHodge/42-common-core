import heapq
import math

from connection import Connection
from zone import Zone
from zone_type import ZoneType


class Router:
    """
    Spatio-temporal A* with a reservation table (multi-agent pathfinding).
    Supports 2D/3D hubs, capacity limits and zone types.
    """

    def __init__(
        self,
        hubs: dict[str, Zone],
        connections: list[Connection],
        start_hub: str,
        end_hub: str,
    ) -> None:
        self.hubs: dict[str, Zone] = hubs
        self.connections: list[Connection] = connections
        self.start_hub: str = start_hub
        self.end_hub: str = end_hub

        self.adj: dict[str, list[tuple[str, int]]] = {n: [] for n in hubs}
        for conn in connections:
            if conn.from_zone in self.adj and conn.to_zone in self.adj:
                cap = conn.max_link_capacity
                self.adj[conn.from_zone].append((conn.to_zone, cap))
                self.adj[conn.to_zone].append((conn.from_zone, cap))

        self.hub_reservations: dict[tuple[str, int], int] = {}
        self.link_reservations: dict[tuple[str, str, int], int] = {}
        self.heuristics: dict[str, float] = self._precompute_heuristics()

    def _precompute_heuristics(self) -> dict[str, float]:
        """Backward Dijkstra from end_hub (cost to reach end_hub)."""
        dist: dict[str, float] = {n: math.inf for n in self.hubs}
        dist[self.end_hub] = 0.0
        pq: list[tuple[float, str]] = [(0.0, self.end_hub)]

        while pq:
            cost, u = heapq.heappop(pq)
            if cost > dist[u]:
                continue
            if self.hubs[u].is_blocked:
                continue
            # moving v -> u costs the cost of entering u
            for v, _ in self.adj[u]:
                if self.hubs[v].is_blocked:
                    continue
                new_cost = cost + self.hubs[u].travel_turns
                if new_cost < dist[v]:
                    dist[v] = new_cost
                    heapq.heappush(pq, (new_cost, v))
        return dist

    def _bonus(self, path: tuple[str, ...], nxt: str) -> int:
        """Tie-break key: fewer priority zones crossed sorts later."""
        n = sum(
            1 for h in set(path + (nxt,))
            if self.hubs[h].zone_type == ZoneType.PRIORITY
        )
        return -n

    def _capacity(self, name: str) -> int:
        if name in (self.start_hub, self.end_hub):
            return 9999
        return self.hubs[name].max_drones

    def find_space_time_path(self, max_turn_limit: int = 1000) -> list[str]:
        """
        Returns the timed path: one entry per turn, a repeated hub name
        means the drone waits there. A restricted move (2 turns) appears
        as a single entry for the arrival turn.
        """
        if math.isinf(self.heuristics[self.start_hub]):
            raise ValueError("No path between start_hub and end_hub")

        pq: list[tuple[float, int, int, int, str, tuple[str, ...]]] = [
            (self.heuristics[self.start_hub], 0, 0, 0, self.start_hub,
             (self.start_hub,))
        ]
        counter = 0
        visited: set[tuple[str, int]] = set()

        while pq:
            _, g_time, _, _, u, path = heapq.heappop(pq)

            if u == self.end_hub:
                return list(path)
            if g_time >= max_turn_limit:
                continue
            if (u, g_time) in visited:
                continue
            visited.add((u, g_time))

            # Option 1: wait in place
            if self.hub_reservations.get((u, g_time + 1), 0) < \
                    self._capacity(u):
                counter += 1
                f = g_time + 1.0 + self.heuristics[u]
                heapq.heappush(
                    pq, (f, g_time + 1, self._bonus(path, u), counter, u,
                         path + (u,))
                )

            # Option 2: move to a neighbour
            for v, link_cap in self.adj[u]:
                v_zone = self.hubs[v]
                if v_zone.is_blocked:
                    continue
                if math.isinf(self.heuristics[v]):
                    continue

                arr_time = g_time + v_zone.travel_turns

                if any(
                    self.link_reservations.get((u, v, t), 0)
                    + self.link_reservations.get((v, u, t), 0) >= link_cap
                    for t in range(g_time, arr_time)
                ):
                    continue

                v_cap = self._capacity(v)
                if self.hub_reservations.get((v, arr_time), 0) >= v_cap:
                    continue

                counter += 1
                f = arr_time + self.heuristics[v]
                heapq.heappush(
                    pq, (f, arr_time, self._bonus(path, v), counter, v,
                         path + (v,))
                )

        raise ValueError("No feasible path within the turn limit")

    def reserve_path(self, path: list[str]) -> None:
        """Reserves hubs and links along a timed path."""
        curr_t = 0
        for i, hub_name in enumerate(path):
            if i > 0:
                prev = path[i - 1]
                if hub_name == prev:
                    curr_t += 1  # wait
                else:
                    duration = self.hubs[hub_name].travel_turns
                    for t in range(curr_t, curr_t + duration):
                        key = (prev, hub_name, t)
                        self.link_reservations[key] = \
                            self.link_reservations.get(key, 0) + 1
                    curr_t += duration
            if hub_name not in (self.start_hub, self.end_hub):
                hkey = (hub_name, curr_t)
                self.hub_reservations[hkey] = \
                    self.hub_reservations.get(hkey, 0) + 1

    def plan_all_drones(self, nb_drones: int) -> dict[str, list[str]]:
        """Timed paths per drone (a repeated hub = one turn of waiting)."""
        paths: dict[str, list[str]] = {}
        for i in range(1, nb_drones + 1):
            timed = self.find_space_time_path()
            self.reserve_path(timed)
            paths[f"D{i}"] = timed
        return paths
