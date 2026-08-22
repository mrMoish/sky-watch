from pytest import MonkeyPatch
from main import user_interaction
import runpy

def test_user_interaction(monkeypatch: MonkeyPatch) -> None:

    monkeypatch.setattr("builtins.input", lambda _: "Moscow")
    user_interaction()
    inputs = iter(["Siria", 'ff', '5', 'Turkey'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    runpy.run_module('main', run_name="__main__")
