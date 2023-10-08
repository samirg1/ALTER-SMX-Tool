from db.get_connection import get_connection
from db.convert_stringed_date import convert_stringed_date
from typing import NamedTuple


class Problem(NamedTuple):
    number: str
    description: str
    date_opened: str
    asset_description: str
    asset_serial: str

    def __repr__(self) -> str:
        date_opened = convert_stringed_date(self.date_opened).strftime(r"%d-%m-%Y")
        return f"{self.number} - {date_opened}\n{self.description}\n{self.asset_description} ({self.asset_serial})"


def get_open_problems(location: str) -> list[Problem]:
    with get_connection("SCMLookup") as connection:
        results = connection.execute(
            """
            SELECT number, brief_description, open_time, asset_description, serial_no_
            FROM probsummarym1
            WHERE location == ? AND problem_status == 'open';
            """,
            (location,),
        ).fetchall()

    return [Problem(*res) for res in results]
