import random
from itertools import combinations

items = []

for i in range(20):
    weight = random.random()         # zufälliges Gewicht
    value = random.random()          # zufälliger Wert zwischen 0 und 1
    stonks = value / weight          # Effizienz der Items
    items.append((weight, value, stonks))

# Ausgabe der ersten 10 zur Kontrolle
#for item in items[:10]:
#    print(item)

def stonks_sort(e):      # Hilfsfunktion für Sortieren
  return e[2]


items.sort(key=stonks_sort, reverse=True)

# Ausgabe der ersten 10 sortierten zur Kontrolle
#for item in items[:10]:
#   print(item)

gesamt_volumen = 1
inhalt = 0
relaxierte_loesung = 0
steigung_core = 0
core_item = -1

#Relaxierte Lösung
for item in items:
    core_item +=1
    if item[0] + inhalt < gesamt_volumen:
        inhalt += item[0]
        relaxierte_loesung += item[1]
    else:
        relaxierte_loesung += item[1] / (item[0] / (gesamt_volumen - inhalt))
        inhalt = gesamt_volumen
        steigung_core = item[2]
        break

print("Das Core Item ist: ", core_item)
print("Die Relaxierte Lösung ist: ", relaxierte_loesung)

items_for_core = []

for item in items:
    weight = item[0]  # Gewichtsübernahem
    value = item[1]  # Wertübernahme
    stonks = item[2] # Stonkübernahme
    entfehrnung_core = -1*((steigung_core*weight)-value)
    items_for_core.append((weight, value, stonks, entfehrnung_core))


# Ausgabe der ersten 10 Items für Core zur Kontrolle
#for item in items_for_core[:10]:
#    print(item)

def entfehrnung_sort(e):      # Hilfsfunktion für Sortieren
    return abs(e[3])

items_for_core.sort(key=entfehrnung_sort)

# Ausgabe der ersten 10 Items für Core nach Sortieren zur Kontrolle
#for item in items_for_core[:10]:
 #   print(item)

def knapsack_bruteforce(items, capacity):
    n = len(items)
    best_value = 0
    best_combination = []

    # teste alle Kombinationen von 0 bis n Items
    for r in range(n + 1):
        for combo in combinations(range(n), r):
            total_weight = sum(items[i][0] for i in combo)
            total_value = sum(items[i][1] for i in combo)

            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_combination = combo

    return best_value, best_combination


# Start Initialisirung vom Core Rucksack
core_volumen = gesamt_volumen
core_value = 0
items_in_core = []
value_help = 0
fehler = 0
abstand_zu_ray = items_for_core[0][3]
for item in items_for_core:
    if item[3] > abstand_zu_ray:
        fehler += 1
        if core_item+1 <= fehler:
            print("Ich habe scheisse gebaut")
            print(item[3])
            print(fehler)
        core_volumen -= item[0]
        core_value += item[1]


for item in items_for_core:
    if abs(item[3]) > relaxierte_loesung-(core_value+value_help):
        print("Die Core Lösung ist: ", core_value+value_help)
        print(f"Der Core war {len(items_in_core)} Groß: ")
        break
    else:
        if item[3] > 0: #Wenn Item über Dantzig Ray liegt
            core_volumen += item[0]
            core_value -= item[1]
        items_in_core.append(item)
        if len(items_in_core) > 20:
            print("Aua es tut so weh")
        value_help, items_help = knapsack_bruteforce(items_in_core, core_volumen)

print("Gewählte Items:", items_help)

best_value, best_items = knapsack_bruteforce(items_for_core, gesamt_volumen)

print("Bruteforce Lösung:", best_value)
print("Gewählte Items:", best_items)