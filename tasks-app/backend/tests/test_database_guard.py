"""The tests empty every table, so they refuse to run on a database not named for tests."""

import pytest

from tests.conftest import is_test_database


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://tasks:pw@db:5432/tasks_test",
        "postgresql+psycopg://user:pw@localhost/my_app_test",
    ],
)
def test_a_database_named_for_tests_is_accepted(url: str) -> None:
    assert is_test_database(url)


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://user:pw@localhost:5432/tasks_dev",
        "postgresql+psycopg://user:pw@localhost:5432/tasks",
        "postgresql+psycopg://user:pw@localhost:5432/test_tasks",
        "postgresql+psycopg://user:pw@localhost:5432",
    ],
)
def test_any_other_database_is_refused(url: str) -> None:
    assert not is_test_database(url)
