"""Общая часть тестов. Не меняйте: автопроверка кладёт рядом с вашими тестами
этот же файл, а не ваш.

Две фикстуры:

  impl  — модуль с книгой приёмов, который сейчас проверяется. По умолчанию ваш
          solution.py, но реализацию можно подменить:

            python3 -m pytest -q                          # ваш solution.py
            python3 -m pytest -q --impl valera_adapter    # те же тесты на коде Валеры

  chars — персонажи из characters.json, каждый раз свежие копии:

            sonya, marat = chars("Соня", "Марат")
"""
import copy
import importlib
import json
from pathlib import Path

import pytest

CHARACTERS = Path(__file__).with_name("characters.json")


def pytest_addoption(parser):
    parser.addoption("--impl", default="solution",
                     help="модуль с learn/cast/book_for, по умолчанию solution.py")


@pytest.fixture
def impl(request):
    return importlib.import_module(request.config.getoption("--impl"))


@pytest.fixture
def chars():
    data = {c["name"]: c for c in json.loads(CHARACTERS.read_text(encoding="utf-8"))}

    def fresh(*names):
        return [copy.deepcopy(data[n]) for n in names]
    return fresh
