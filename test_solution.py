import pytest


def test_three_fires_hit_differently(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    book = impl.book_for(sonya)
    dmg = [impl.cast(book, name, sonya, marat, log=[])[0]
           for name in ("fire10", "fire20", "fire40")]
    assert dmg == [10, 20, 40]


def test_charges_independent(impl, chars):
    sonya, lina, marat = chars("Соня", "Лина", "Марат")
    sonya_book = impl.book_for(sonya)
    lina_book = impl.book_for(lina)

    for _ in range(3):
        assert impl.cast(sonya_book, "nova", sonya, marat, log=[]) is not None
    assert impl.cast(sonya_book, "nova", sonya, marat, log=[]) is None

    assert impl.cast(lina_book, "nova", lina, marat, log=[]) is not None


def test_two_battles_two_logs(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    book = impl.book_for(sonya)

    log1 = []
    log2 = []
    impl.cast(book, "strike", sonya, marat, log=log1)
    impl.cast(book, "strike", sonya, marat, log=log2)

    assert len(log1) == 1
    assert len(log2) == 1


def test_learn_rejects_bad_signature(impl):
    def bad(user, target):
        return 0, {}

    with pytest.raises(TypeError):
        impl.learn({}, bad)


def test_positional_crit_raises(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    book = impl.book_for(sonya)

    with pytest.raises(TypeError):
        impl.cast(book, "strike", sonya, marat, True, log=[])


def test_critical_strike_hits_harder(impl, chars):
    sonya, marat, lina = chars("Соня", "Марат", "Лина")
    book = impl.book_for(sonya)

    normal = impl.cast(book, "critical_strike", sonya, marat, log=[])
    crit = impl.cast(book, "critical_strike", sonya, lina, crit=True, log=[])

    assert crit[0] > normal[0]


def test_no_mana_returns_none(impl, chars):
    valera, marat = chars("Валера", "Марат")
    book = impl.book_for(valera)
    hp = marat["hp"]

    assert impl.cast(book, "strike", valera, marat, log=[]) is None
    assert marat["hp"] == hp


def test_status_applies_effect(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    book = impl.book_for(sonya)

    result = impl.cast(book, "status", sonya, marat, burn=True, log=[])

    assert isinstance(result, tuple)
    assert marat["effects"]["burn"] is True


def test_heal_restores_self(impl, chars):
    sonya, marat = chars("Соня", "Марат")
    sonya["hp"] = 30
    book = impl.book_for(sonya)

    impl.cast(book, "heal", sonya, log=[])

    assert sonya["hp"] == 50
    assert marat["hp"] == 100
