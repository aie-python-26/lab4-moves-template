import inspect


_CONTRACT = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.VAR_POSITIONAL,
             inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD)


def learn(book, move):
    kinds = tuple(p.kind for p in inspect.signature(move).parameters.values())
    if kinds != _CONTRACT:
        raise TypeError("сигнатура приёма не совпадает с контрактом")
    book[move.__name__] = move
    return move


def cast(book, name, user, /, *targets, log, **effects):
    move = book[name]
    bound = inspect.signature(move).bind(user, *targets, **effects)
    result = move(*bound.args, **bound.kwargs)
    if result is not None:
        log.append((user["name"], name, result[0]))
    return result


def make_strike(power, element):
    def move(user, /, *targets, crit=False, **effects):
        for target in targets:
            target["hp"] -= power
        return power * len(targets), {element: True}

    move.__name__ = element + str(power)
    return move


def limited(move, charges):
    left = charges

    def wrapped(user, /, *targets, crit=False, **effects):
        nonlocal left
        if left == 0:
            return None
        left -= 1
        return move(user, *targets, crit=crit, **effects)

    wrapped.__name__ = move.__name__
    return wrapped


def strike(user, /, *targets, crit=False, **effects):
    if user["mana"] < 5:
        return None
    user["mana"] -= 5
    for target in targets:
        target["hp"] -= 10
    return 10 * len(targets), {}


def nova(user, /, *targets, crit=False, **effects):
    if user["mana"] < 10:
        return None
    user["mana"] -= 10
    for target in targets:
        target["hp"] -= 30
    return 30 * len(targets), {"burn": True}


def heal(user, /, *targets, crit=False, **effects):
    if user["mana"] < 5:
        return None
    user["mana"] -= 5
    user["hp"] += 20
    return 0, {}


def status(user, /, *targets, crit=False, **effects):
    for target in targets:
        for key, value in effects.items():
            target["effects"][key] = value
    return 0, dict(effects)


def critical_strike(user, /, *targets, crit=False, **effects):
    if user["mana"] < 5:
        return None
    user["mana"] -= 5
    dmg = 20 if crit else 10
    for target in targets:
        target["hp"] -= dmg
    return dmg * len(targets), {}


def book_for(character):
    book = {}
    learn(book, strike)
    learn(book, limited(nova, 3))
    learn(book, heal)
    learn(book, status)
    learn(book, critical_strike)
    learn(book, make_strike(10, "fire"))
    learn(book, make_strike(20, "fire"))
    learn(book, make_strike(40, "fire"))
    return book
