#!/usr/bin/env python3
"""Четыре прогона кода Валеры — выводы для ТЗ.   python3 check_valera.py"""
import copy
import json
import traceback

import valera_moves as v

chars = {c["name"]: c for c in json.load(open("characters.json"))}
def fresh(*names):
    return [copy.deepcopy(chars[n]) for n in names]

print("1. общий журнал")
sonya, marat, lina = fresh("Соня", "Марат", "Лина")
v.strike(sonya, marat)
v.strike(lina, marat)
print("   журнал не передавали, записей в нём:", len(v.strike.__defaults__[1]), "| strike.__defaults__:", v.strike.__defaults__)

print("2. общие заряды")
sonya, lina, marat = fresh("Соня", "Лина", "Марат")
print("   Соня:", [v.nova(sonya, marat) is not None for _ in range(2)], "| Лина:", [v.nova(lina, marat) is not None for _ in range(2)])
print("   nova.__kwdefaults__:", v.nova.__kwdefaults__)

print("3. три огня")
marat, = fresh("Марат")
print("   урон fire1, fire2, fire3:", [f(None, marat)[0] for f in v.fires])

print("4. крит позиционно")
sonya, marat = fresh("Соня", "Марат")
v.nova.__kwdefaults__["charges"]["left"] = 3        # заряды общие и уже потрачены в п. 2 — иначе nova молча вернёт None
try:
    v.cast("nova", sonya, marat, True)
except TypeError:
    print("   " + "   ".join(traceback.format_exc().splitlines(True)[-3:]), end="")
