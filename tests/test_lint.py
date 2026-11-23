import pytest

from .conftest import Project


def test_clean_module_has_no_violations(project: Project) -> None:
  assert project.check(project.add_fixture("clean.py")) == []


@pytest.mark.parametrize(
  ("fixture", "expected"),
  [
    ("unused_import.py", "F401"),
    ("unsorted_imports.py", "I001"),
    ("mutable_default.py", "B006"),
    ("legacy_typing.py", "UP006"),
    ("semicolons.py", "E703"),
    ("class_name.py", "N801"),
    ("single_quotes.py", "Q000"),
  ],
)
def test_reports_rule(project: Project, fixture: str, expected: str) -> None:
  assert expected in project.check(project.add_fixture(fixture))


def test_reports_statement_separated_by_semicolon(project: Project) -> None:
  assert "E702" in project.check(project.add_fixture("semicolons.py"))


def test_init_module_may_have_unused_imports(project: Project) -> None:
  path = project.add_source("pkg/__init__.py", "import os\n")
  assert project.check(path) == []


def test_unused_import_is_reported_outside_init(project: Project) -> None:
  path = project.add_source("pkg/module.py", "import os\n")
  assert project.check(path) == ["F401"]


def test_tests_directory_ignores_test_naming(project: Project) -> None:
  source = "def test_Something():\n  assert True\n"
  assert project.check(project.add_source("tests/test_names.py", source)) == []
  assert project.check(project.add_source("src/test_names.py", source)) == ["N802"]


def test_line_length_limit_is_100(project: Project) -> None:
  within = f'VALUE = "{"a" * 90}"\n'
  beyond = f'VALUE = "{"a" * 95}"\n'
  assert project.check(project.add_source("within.py", within)) == []
  assert project.check(project.add_source("beyond.py", beyond)) == ["E501"]
