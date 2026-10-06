"""Ваши тесты. Реализацию берите из фикстуры impl, персонажей — из chars (см. conftest.py):

    python3 -m pytest -q                          # на вашем solution.py — должно быть зелёным
    python3 -m pytest -q --impl valera_adapter    # на коде Валеры — должно быть красным

Минимум восемь тестов, список обязательных — в README.
"""


def test_three_fires_hit_differently(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    book = impl.book_for(sonya)
    dmg = [impl.cast(book, name, sonya, marat, log=[])[0] for name in ("fire10", "fire20", "fire40")]
    assert dmg == [10, 20, 40]
