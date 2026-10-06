"""Код Валеры, натянутый на интерфейс из README — чтобы ваши тесты можно было
прогнать на нём той же командой:

    python3 -m pytest -q --impl valera_adapter

Ничего не чинит: книга одна на всех, журнал и заряды живут в значениях по
умолчанию, три огня — те самые три лямбды, лечения у Валеры нет вовсе.
"""
import valera_moves as v


def learn(book, move):
    book[move.__name__] = move                 # сигнатуру не смотрит
    return move


def cast(book, name, user, /, *targets, log=None, **effects):
    return book[name](user, *targets, **effects)       # журнал «ведётся сам», log не нужен


def make_strike(power, element):
    if element == "fire" and power in (10, 20, 40):
        return v.fires[(10, 20, 40).index(power)]
    return lambda user, *targets: (v.hit(targets, power), {element: True})


def limited(move, charges, state={}):
    left = state.setdefault(move, {"left": charges})   # один счётчик на приём, кто бы ни звал

    def charged(user, *targets, **effects):
        if left["left"] == 0:
            return None
        left["left"] -= 1
        return move(user, *targets, **effects)
    charged.__name__ = move.__name__
    return charged


BOOK = dict(v.BOOK, fire10=v.fires[0], fire20=v.fires[1], fire40=v.fires[2])


def book_for(character, charges=3):
    return BOOK                                # одна и та же книга, кого ни спроси
