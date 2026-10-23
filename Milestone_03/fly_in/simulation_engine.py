from __future__ import annotations

from pydantic import BaseModel, Field

from common_types import NonEmptyStr
from connection import Connection
from drone import Drone
from drone_movement import DroneMovement
from turn_result import TurnResult
from zone import Zone


class SimulationEngine(BaseModel):
    """Turn-by-turn simulation engine (state validated by Pydantic)."""

    model_config = {"validate_assignment": True}

    start_hub: NonEmptyStr
    end_hub: NonEmptyStr
    hubs: dict[str, Zone]
    connections: list[Connection]

    current_turn: int = Field(default=0, ge=0)
    drones: list[Drone] = Field(default_factory=list)
    delivered_drone_ids: set[str] = Field(default_factory=set)
    history: list[TurnResult] = Field(default_factory=list)

    @classmethod
    def create(
        cls,
        nb_drones: int,
        start_hub: str,
        end_hub: str,
        hubs: dict[str, Zone],
        connections: list[Connection],
        paths_by_drone: dict[str, list[str]] | None = None,
    ) -> SimulationEngine:
        """Builds the fleet at start_hub with its assigned paths."""
        drones: list[Drone] = []
        for i in range(1, nb_drones + 1):
            drone_id = f"D{i}"
            path = (paths_by_drone or {}).get(drone_id, [])
            drones.append(
                Drone(
                    id=drone_id,
                    current_position=start_hub,
                    assigned_path=path,
                )
            )
        return cls(
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=connections,
            drones=drones,
        )

    def is_finished(self) -> bool:
        return len(self.delivered_drone_ids) == len(self.drones)

    def step_turn(self) -> TurnResult:
        """
        Executes one turn by following each drone's timed plan
        (computed by the Router, capacity-safe by construction).
        A hub repeated in the plan = the drone waits one turn.
        """
        if self.is_finished():
            return TurnResult(turn_number=self.current_turn or 1)

        self.current_turn += 1
        movements: list[DroneMovement] = []

        for drone in self.drones:
            if drone.id in self.delivered_drone_ids:
                continue

            # Second turn of a restricted move
            if drone.transit_remaining_turns > 0:
                drone.transit_remaining_turns -= 1
                movements.append(DroneMovement(
                    drone_id=drone.id, destination=drone.current_position))
            else:
                path = drone.assigned_path
                if drone.path_index + 1 >= len(path):
                    raise RuntimeError(
                        f"{drone.id}: plan ended before reaching "
                        f"'{self.end_hub}'")
                nxt = path[drone.path_index + 1]
                drone.path_index += 1
                if nxt == drone.current_position:
                    continue  # waiting
                if nxt not in self.hubs or self.hubs[nxt].is_blocked:
                    raise RuntimeError(f"{drone.id}: illegal move to {nxt}")
                drone.current_position = nxt
                drone.transit_remaining_turns = \
                    self.hubs[nxt].travel_turns - 1
                movements.append(
                    DroneMovement(drone_id=drone.id, destination=nxt))

            if (drone.current_position == self.end_hub
                    and drone.transit_remaining_turns == 0):
                self.delivered_drone_ids.add(drone.id)

        result = TurnResult(turn_number=self.current_turn,
                            movements=movements)
        self.history.append(result)
        return result
