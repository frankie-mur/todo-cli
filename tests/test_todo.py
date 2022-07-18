# tests/test_todo.py

from typer.testing import CliRunner

from todo import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} {__version__}" in result.output
