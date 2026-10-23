import re

from connection import Connection
from utils_parser import extract_statement_data, parse_metadata_functional
from zone import Zone


class MapParser:
    VALID_KEYWORDS = {
        "nb_drones", "start_hub", "end_hub", "hub", "connection"
    }
    HUB_META_KEYS = {"zone", "color", "max_drones"}
    CONNECTION_META_KEYS = {"max_link_capacity"}

    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.start_hub: str | None = None
        self.end_hub: str | None = None
        self.hubs: dict[str, Zone] = {}
        self.connections: list[Connection] = []

    def _handle_nb_drones(self, right: str, line_num: int) -> None:
        try:
            value = int(right)
            if value <= 0:
                raise ValueError()
        except ValueError:
            raise ValueError(
                f"Line {line_num}: 'nb_drones' must be a positive "
                f"integer (got '{right}')"
            )

        if self.nb_drones is not None:
            raise ValueError(
                f"Line {line_num}: Multiple declaration of 'nb_drones'"
            )
        self.nb_drones = value

    def _handle_hub(self, keyword: str, right: str, line: int) -> None:
        data_part, meta_part = extract_statement_data(right)
        metadata = parse_metadata_functional(meta_part, self.HUB_META_KEYS)

        parts = data_part.split()
        if len(parts) == 3:
            name, x_str, y_str = parts
            z_str = "0"
        elif len(parts) == 4:
            name, x_str, y_str, z_str = parts
        else:
            raise ValueError(
                f"Line {line}: invalid hub format '{right}'. "
                "Expected: '<name> <x> <y> [z] [metadata]'"
            )

        if name in self.hubs:
            raise ValueError(f"Line {line}: Duplicate hub name '{name}'")
        if keyword == "start_hub" and self.start_hub is not None:
            raise ValueError(
                f"Line {line}: Multiple declaration of 'start_hub'"
            )
        if keyword == "end_hub" and self.end_hub is not None:
            raise ValueError(
                f"Line {line}: Multiple declaration of 'end_hub'"
            )

        try:
            zone = Zone(
                name=name,
                x=int(x_str),
                y=int(y_str),
                z=int(z_str),
                **metadata,  # type: ignore[arg-type]
            )
        except ValueError as err:
            raise ValueError(
                f"Line {line}: Error creating Zone '{name}': {err}"
            )

        self.hubs[name] = zone
        if keyword == "start_hub":
            self.start_hub = name
        elif keyword == "end_hub":
            self.end_hub = name

    def _handle_connection(self, right: str, line: int) -> None:
        data_part, meta_part = extract_statement_data(right)
        metadata = parse_metadata_functional(
            meta_part, self.CONNECTION_META_KEYS
        )

        if "-" not in data_part:
            raise ValueError(
                f"Line {line}: Invalid connection format '{right}'. "
                "Expected: '<zone1>-<zone2> [metadata]'"
            )

        from_zone, to_zone = map(str.strip, data_part.split("-", 1))

        missing = [z for z in (from_zone, to_zone) if z not in self.hubs]
        if missing:
            raise ValueError(
                f"Line {line}: Unknown zones in connection: "
                f"{'-'.join(missing)}"
            )
        if from_zone == to_zone:
            raise ValueError(
                f"Line {line}: Connection from '{from_zone}' to itself"
            )

        is_duplicate = any(
            {c.from_zone, c.to_zone} == {from_zone, to_zone}
            for c in self.connections
        )
        if is_duplicate:
            raise ValueError(
                f"Line {line}: Duplicate connection between "
                f"'{from_zone}' and '{to_zone}'"
            )

        try:
            self.connections.append(
                Connection(
                    from_zone=from_zone,
                    to_zone=to_zone,
                    **metadata,  # type: ignore[arg-type]
                )
            )
        except ValueError as err:
            raise ValueError(f"Line {line}: Error creating Connection: {err}")

    def parse_statement(self, stmt: str, line: int) -> None:
        stmt = stmt.strip()
        if not stmt or stmt.startswith("#"):
            return

        if ":" not in stmt:
            raise ValueError(f"Line {line}: Missing separator ':' in '{stmt}'")

        keyword, right = map(str.strip, stmt.split(":", 1))

        if keyword not in self.VALID_KEYWORDS:
            raise ValueError(
                f"Line {line}: Unknown keyword '{keyword}'. "
                f"Expected one of: {sorted(self.VALID_KEYWORDS)}"
            )

        if keyword == "nb_drones":
            self._handle_nb_drones(right, line)
        elif keyword in ("hub", "start_hub", "end_hub"):
            self._handle_hub(keyword, right, line)
        else:
            self._handle_connection(right, line)

    def parse_text(
        self, text: str
    ) -> tuple[int, str, str, dict[str, Zone], list[Connection]]:
        for index, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            statements = re.split(
                r"(?=\b(?:nb_drones|start_hub|end_hub|hub|connection):)",
                line,
            )
            for statement in statements:
                self.parse_statement(statement, index)

        if self.nb_drones is None:
            raise ValueError("Parsing Error: Missing 'nb_drones'.")
        if self.start_hub is None:
            raise ValueError("Parsing Error: Missing 'start_hub'.")
        if self.end_hub is None:
            raise ValueError("Parsing Error: Missing 'end_hub'.")

        return (
            self.nb_drones,
            self.start_hub,
            self.end_hub,
            self.hubs,
            self.connections,
        )

    def parse_file(
        self, file_path: str
    ) -> tuple[int, str, str, dict[str, Zone], list[Connection]]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Map file not found: '{file_path}'")
        except OSError as err:
            raise ValueError(f"Error reading file '{file_path}': {err}")

        return self.parse_text(content)
