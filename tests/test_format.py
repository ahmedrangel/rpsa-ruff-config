from .conftest import Project


def test_clean_module_is_formatted(project: Project) -> None:
  assert project.format_check(project.add_fixture("clean.py"))


def test_messy_module_is_not_formatted(project: Project) -> None:
  assert not project.format_check(project.add_fixture("messy_format.py"))


def test_formats_with_two_space_indent_and_double_quotes(project: Project) -> None:
  formatted = project.format(project.add_fixture("messy_format.py"))
  assert '  return "hi"' in formatted
  assert "'" not in formatted


def test_collapses_trailing_commas(project: Project) -> None:
  formatted = project.format(project.add_fixture("messy_format.py"))
  assert "values = [1, 2]" in formatted
