import sys
import time

from map_parser import MapParser
from router import Router
from simulation_engine import SimulationEngine
from turn_result import TurnResult

MAX_SAFETY_TURNS = 1000


def run_simulation(map_file_path: str) -> int:
    print(f"=== Fly-In 3D Simulation Runner: {map_file_path} ===")

    nb_drones, start_hub, end_hub, hubs, connections = \
        MapParser().parse_file(map_file_path)

    is_3d = any(h.z != 0 for h in hubs.values())
    mode_str = "3D (x, y, z)" if is_3d else "2D (x, y)"
    print(
        f"Map loaded: {nb_drones} drones, {len(hubs)} hubs "
        f"(Start: '{start_hub}', Goal: '{end_hub}'), "
        f"{len(connections)} links."
    )
    print(f"Coordinates Mode: {mode_str}")

    t0 = time.perf_counter()
    router = Router(hubs, connections, start_hub, end_hub)
    assigned_paths = router.plan_all_drones(nb_drones)
    t1 = time.perf_counter()
    print(f"Spatio-temporal routes computed in {t1 - t0:.4f}s.")
    print("\n--- Simulation Turn-by-Turn Output (stdout) ---")

    engine = SimulationEngine.create(
        nb_drones=nb_drones,
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=hubs,
        connections=connections,
        paths_by_drone=assigned_paths,
    )

    while not engine.is_finished() and engine.current_turn < MAX_SAFETY_TURNS:
        turn: TurnResult = engine.step_turn()
        if turn.stdout_line:
            print(f"Turn {turn.turn_number:02d}: {turn.stdout_line}")

    if engine.is_finished():
        print(f"\nSUCCESS: all {nb_drones} drones reached '{end_hub}' "
              f"in {engine.current_turn} turns.")
        return 0
    print(f"\nFAILED: exceeded the safety limit ({MAX_SAFETY_TURNS} turns).")
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>", file=sys.stderr)
        return 2
    try:
        return run_simulation(sys.argv[1])
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
