from abc import ABC, abstractmethod
from sqlite3 import Connection

from design.Test import Test
from design.Problem import Problem
from design.Script import ScriptLine


class Model(ABC):
    @property
    @abstractmethod
    def table_name(self) -> str:
        ...

    def insert(self, connection: Connection) -> None:
        connection.execute(
            f"""
            INSERT INTO {self.table_name} {f"({', '.join(self.__dict__.keys())})"}
            VALUES (?{', ?'*(len(self.__dict__)-1)});
            """,
            tuple(self.__dict__.values()),
        )


class TestModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTestsm1"

    def __init__(self, test: Test, problem: Problem, test_id: str, user: str, time: str):
        self.test_id = test_id
        self.logical_name = test.item.number
        self.customer_barcode = test.item.number
        self.test_date = time
        self.sysmoduser = user
        self.problem_number = problem.number
        self.user_name = user
        self.comments = test.comments
        self.customer_id = str(problem.customer_number)
        self.company_name = problem.company
        self.location = problem.campus
        self.dept = problem.department
        self.pointsync_id = None
        self.overall = test.result
        self.building = ""
        self.floor = ""
        self.room = test.item.room
        self.model = test.item.model
        self.manufacturer = test.item.manufacturer
        self.description = test.item.description
        self.serial_no_ = test.item.serial
        self.pointsync_time = None
        self.sysmodtime = time
        self.interfaced = None


class ScriptTesterModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTesterNumbersm1"

    def __init__(self, test: Test, test_id: str):
        self.test_id = test_id
        self.script_number = test.script.number
        self.tester_number = test.script.tester_number


class ScriptLineModel(Model):
    @property
    def table_name(self) -> str:
        return "SCMobileTestLinesm1"

    def __init__(self, test: Test, line: ScriptLine, test_id: str, user: str):
        self.test_id = test_id
        self.script_number = test.script.number
        self.script_line = line.number
        self.result = line.result
        self.comments = None
        self.date_performed = None
        self.performed_by = user
        self.script_line_text = line.text
        self.set_point = 200 if (test.script.number == 1287 and line.number == 5) else None
        self.page = None
        self.orderprgn = None
