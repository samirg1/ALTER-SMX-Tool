from design.Item import Item
from design.Job import Job
from design.Test import Test
from design.Script import Script
from design.data import get_all_scripts
from testing.conftest import MockSqlObject

Test.__test__ = False  # type: ignore


def test_job_creation_and_properties() -> None:
    job = Job("CAMPEYN - ABLE VICTORIA", "CampusA", "DepartmentY", "123", 123)

    assert job.company == "ABLE"
    assert job.campus == "CampusA"
    assert job.department == "DepartmentY"
    assert job.number == "123"
    assert job.customer_number == 123
    assert len(job.tests) == 0


def test_job_add_test(mock_sql_connect_scripts: MockSqlObject) -> None:
    job = Job("CompanyX", "CampusA", "DepartmentY", "123", 123)

    test1 = Test(Item("001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019"))
    test2 = Test(Item("002", "Test Item 2", "ModelY", "ManufacturerY", "XYZ002", "RM1", "2019"))

    custom1 = Script("Custom1", "Custom Script", 1, (), exact_matches=["Test Item 1"])
    get_all_scripts()["Custom1"] = custom1
    test1.script = test1.determine_script()
    custom2 = Script("Custom2", "Custom Script", 1, (), exact_matches=["Test Item 2"])
    get_all_scripts()["Custom2"] = custom2
    test2.script = test2.determine_script()

    job.add_test(test1)
    job.add_test(test1)
    job.add_test(test2)

    assert len(job.tests) == 3
    assert len(job.test_breakdown) == 2
    assert job.test_breakdown["Custom1"] == 2
    assert job.test_breakdown["Custom2"] == 1


def test_job_remove_test(mock_sql_connect_scripts: MockSqlObject) -> None:
    custom1 = Script("Custom1", "Custom Script", 1, (), exact_matches=["Test Item 1"])
    get_all_scripts()["Custom1"] = custom1
    test1 = Test(Item("001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019"))
    test1.script = test1.determine_script()
    job = Job("CompanyX", "CampusA", "DepartmentY", "123", 123)
    job.add_test(test1)
    job.remove_test(test1)

    assert len(job.tests) == 0
    assert len(job.test_breakdown) == 0
    assert "Custom1" not in job.test_breakdown


def test_job_string_representation() -> None:
    job1 = Job("CAMPEYN - YOORALLA", "CampusA", "DepartmentY", "123", 123)
    job2 = Job("BENETAS - ST PAULS", "CampusA", "DepartmentY", "123", 123)
    job3 = Job("JEWISH ST KILDA", "CampusA", "DepartmentY", "123", 123)

    assert str(job1) == "CampusA\nCAMPEYN\n123"
    assert str(job2) == "CampusA\nBENETAS\n123"
    assert str(job3) == "CampusA\nJEWISH CARE\n123"


def test_job_hashing_and_eq() -> None:
    job1 = Job("CompanyX", "CampusA", "DepartmentY", "123", 123)
    job2 = Job("CompanyY", "CampusB", "DepartmentZ", "123", 123)
    job3 = Job("CompanyZ", "CampusA", "DepartmentZ", "123", 123)
    assert len({job1, job2}) == 2
    assert len({job1, job3}) == 1
    assert hash(job1) != hash(job2)
    assert hash(job1) == hash(job3)
