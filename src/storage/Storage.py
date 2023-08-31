import json
import os
import pathlib
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Mapping, Sequence

from attrs import asdict, define, field

_APPLICATION_PATH = os.path.dirname(sys.executable)


def _tuple_converter(value: Sequence[int] | None) -> tuple[int, ...] | None:
    return tuple(value) if value is not None else value


@define(repr=False, eq=False)
class Positions:
    testing_tab: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    assets_tab: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    show_all_script: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    comment_box: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    window: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    track_weight_field: tuple[int, int] | None = field(default=None, converter=_tuple_converter)
    sm_incident_tab: tuple[int, int] | None = field(default=None, converter=_tuple_converter)

    @classmethod
    def keys(cls):
        return cls.__annotations__.keys()

    @classmethod
    def from_dict(cls, data: Mapping[str, Sequence[int]]):
        return cls(**data)


@define(repr=False, eq=False)
class Storage:
    _json_file_path: Path | str = field(default=pathlib.Path(_APPLICATION_PATH, "store.json"))
    tutorial_complete: bool = field(default=False, init=False)
    calibrated: bool = field(default=False, init=False)
    total_tests: int = field(default=0, init=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False)
    positions: Positions = field(factory=Positions, init=False)
    item_model_to_script_answers: dict[str, list[str]] = field(factory=dict, init=False)

    def __attrs_post_init__(self) -> None:
        try:
            with open(self._json_file_path) as file:
                data = json.load(file)
                if not data:
                    return self._save()

                for key, value in data.items():
                    data = value if key != "positions" else Positions.from_dict(value)
                    setattr(self, key, data)

        except (FileNotFoundError, json.JSONDecodeError):
            self._save()

    def _save(self) -> None:
        with open(self._json_file_path, "w") as file:
            data = asdict(self)
            data["_json_file_path"] = str(data["_json_file_path"])
            json.dump(data, file, indent=4)

    @contextmanager
    def edit(self):
        try:
            yield self
        finally:
            self._save()
