import random
from itertools import combinations
from typing import List, Tuple
import copy
import time

core_gesamtzeit =0
bnb_gesamtzeit = 0
runden = 1000

for i in range(runden):
    items = []
    elemente = 1000
    gesamt_volumen = 400

    for i in range(elemente):
        weight = random.random()  # zufälliges Gewicht
        value = random.random()  # zufälliger Wert zwischen 0 und 1
        stonks = value / weight  # Effizienz der Items
        number = i
        items.append((weight, value, stonks, number))


    # Ausgabe der ersten 10 zur Kontrolle
    # for item in items[:10]:
    #    print(item)

    def stonks_sort(e):  # Hilfsfunktion für Sortieren
        return e[2]


    items.sort(key=stonks_sort, reverse=True)

    # Ausgabe der ersten 10 sortierten zur Kontrolle
    # for item in items[:10]:
    #   print(item)


    global greedy


    # Relaxierte Lösung
    def relax(items, volumen, initierung):
        global greedy
        core_item = -1
        inhalt = 0
        relaxierte_loesung = 0
        steigung_core = 0
        for item in items:
            core_item += 1
            if item[0] + inhalt < volumen:
                inhalt += item[0]
                relaxierte_loesung += item[1]
            else:
                if initierung == True:
                    greedy = relaxierte_loesung
                relaxierte_loesung += item[1] / (item[0] / (volumen - inhalt))
                inhalt = volumen
                steigung_core = item[2]
                break
        return core_item, relaxierte_loesung, steigung_core


    core_item, relaxierte_loesung, steigung_core = relax(items, gesamt_volumen, True)

    # print("Das Core Item ist: ", core_item)
    #print("Die Relaxierte Lösung ist: ", relaxierte_loesung)

    items_for_core = []

    for item in items:
        weight = item[0]  # Gewichtsübernahem
        value = item[1]  # Wertübernahme
        stonks = item[2]  # Stonkübernahme
        entfehrnung_core = -1 * ((steigung_core * weight) - value)
        number = item[3]  # Idexübernahme
        items_for_core.append((weight, value, stonks, entfehrnung_core, number))


    # Ausgabe der ersten 10 Items für Core zur Kontrolle
    # for item in items_for_core[:10]:
    #    print(item)

    def entfehrnung_sort(e):  # Hilfsfunktion für Sortieren
        return abs(e[3])


    items_for_core.sort(key=entfehrnung_sort)


    # Ausgabe der ersten 10 Items für Core nach Sortieren zur Kontrolle
    # for item in items_for_core[:10]:
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


    def pareto_knapsack(items, max_weight):
        """
        items: Liste von (gewicht, wert, indexnummer)
        max_weight: Maximales Volumen/Gewicht des Rucksacks

        Rückgabe:
        (bestes_gewicht, bester_wert) der besten Pareto-optimalen Lösung ≤ max_weight
        """

        # Start: leere Lösung
        pareto = [(0, 0)]  # (gewicht, wert)
        for w, v, x, y, z in items:
            neue_lösungen = []

            for pw, pv in pareto:
                nw, nv = pw + w, pv + v
                if nw <= max_weight:
                    neue_lösungen.append((nw, nv))

            pareto += neue_lösungen
            pareto = pareto_filter(pareto)

        # beste Lösung (maximaler Wert)
        return max(pareto, key=lambda x: x[1])[1]


    def pareto_filter(solutions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Entfernt dominierte Lösungen
        """
        solutions = sorted(solutions, key=lambda x: (x[0], -x[1]))
        pareto = []

        max_value_so_far = -1
        for weight, value in solutions:
            if value > max_value_so_far:
                pareto.append((weight, value))
                max_value_so_far = value

        return pareto


    # Start Initialisirung vom Core Rucksack
    core_start_time = time.perf_counter()
    core_volumen = gesamt_volumen
    core_value = 0
    items_in_core = []
    value_help = 0
    fehler = 0
    abstand_zu_ray = items_for_core[0][3]
    for item in items_for_core:
        if item[3] > abstand_zu_ray:
            fehler += 1
            if core_item + 1 <= fehler:
                print("Ich habe scheisse gebaut")
                print(item[3])
                print(fehler)
            core_volumen -= item[0]
            core_value += item[1]

    for item in items_for_core:
        if abs(item[3]) > relaxierte_loesung - (core_value + value_help):
            core_end_time = time.perf_counter()
            #print("Die Core Lösung ist: ", core_value + value_help)
            core_laufzeit = core_end_time - core_start_time
            #print("Die Core Laufzeit war: ", core_laufzeit )
            #print(f"Der Core war {len(items_in_core)} Groß")
            break
        else:
            if item[3] > 0:  # Wenn Item über Dantzig Ray liegt
                core_volumen += item[0]
                core_value -= item[1]
            items_in_core.append(item)
            # if len(items_in_core) > 20:
            # print("Aua es tut so weh")
            # value_help, items_help = knapsack_bruteforce(items_in_core, core_volumen)
            value_help = pareto_knapsack(items_in_core, core_volumen)

    bestes_blatt = []
    bestes_blatt.append(greedy)
    # bestes_blatt.append([])

    bauminit = []
    bauminit.append(0)  # Aktuelle Branch Position
    bauminit.append(gesamt_volumen)
    bauminit.append(relaxierte_loesung)  # Wert Relaxlösung + feste Objekte
    bauminit.append(0)  # Wert von festen Objekten
    bauminit.append([])  # Elemente der Lösung
    baum = []
    baum.append(bauminit)
    global bound_time
    bound_time = 0
    global suchen_time
    suchen_time = 0
    branch_time = 0


    # global hinzugefügt
    # hinzugefügt = 0
    # global gelöscht
    # gelöscht = 0
    # print(baum)

    def bound(top):
        global bound_time
        # global gelöscht
        # bound_start_time = time.perf_counter()
        # print(top)
        full_counter = 0
        # print(max(baum, key=lambda x: x[2])[2])
        for i in baum:
            if i[2] <= top:
                baum.pop(full_counter)
                # gelöscht +=1
            full_counter += 1
        # bound_time +=(time.perf_counter()-bound_start_time)


    def branch(baumitem, top):
        # global hinzugefügt
        # print(baumitem)
        # print(baumitem[0])
        global suchen_time
        wert_item = items[baumitem[0]][1]
        gewicht_item = items[baumitem[0]][0]
        # index_item = items[baumitem[0]][3]
        # Bestes Item wird auf 0 gesetzt
        baumitem[0] += 1
        baumitem[2] = relax(items[baumitem[0]:elemente], baumitem[1], False)[1] + baumitem[3]
        # print("2.aufrgu", baumitem)
        if baumitem[0] != elemente - 1 and baumitem[2] > top[0]:
            suchen_start_time = time.perf_counter()
            baum.append(copy.deepcopy(baumitem))
            suchen_time += (time.perf_counter() - suchen_start_time)
            # hinzugefügt +=1

        # Bestes Item wird auf 1 gesetzt
        if baumitem[1] - gewicht_item >= 0:
            baumitem[3] += wert_item
            baumitem[1] -= gewicht_item
            baumitem[2] = relax(items[baumitem[0]:elemente], baumitem[1], False)[1] + baumitem[3]
            # baumitem[4].append(index_item)
            # print("3.aufrgu", baumitem)
            if baumitem[3] > top[0]:
                top[0] = baumitem[3]
                # top[1] = baumitem[4]
                # print(top)
                bound(top[0])
            if baumitem[0] != elemente - 1 and baumitem[2] > top[0]:
                suchen_start_time = time.perf_counter()
                baum.append(copy.deepcopy(baumitem))
                suchen_time += (time.perf_counter() - suchen_start_time)
                # hinzugefügt += 1

        return top
        # Ein Element wird Gewählt und auf 1 und 0 gesetzt
        # TODO Branchen an gebrochener Variable


    # print("Gewählte Items:", items_help)

    # Bruteforce auf Alles. Versagt nach 25 Elementen
    # best_value, best_items = knapsack_bruteforce(items_for_core, gesamt_volumen)
    # print("Bruteforce Lösung:", best_value)
    # print("Gewählte Items:", best_items)

    # Nemhauser-Ulmann auf alles
    # pareto_start_time = time.perf_counter()
    # best_value = pareto_knapsack(items_for_core, gesamt_volumen)
    # pareto_end_time = time.perf_counter()
    # print("Pareto Lösung:", best_value)
    # print("Die Pareto Laufzeit war:", pareto_end_time-pareto_start_time)
    # TODO print("Gewählte Items:", best_items)

    # Branch and Bound auf alles
    aua = 0
    bnb_start_time = time.perf_counter()
    while baum != []:
        aua += 1
        index, _ = max(enumerate(baum), key=lambda x: x[1][2])
        # print(baum[index][2])
        # print(index)
        # print("Hier Baum Bruder", baum)
        suchen_start_time = time.perf_counter()
        zwischenspeicher = copy.deepcopy(baum[index])
        # print(zwischenspeicher)
        suchen_time += (time.perf_counter() - suchen_start_time)
        baum.pop(index)
        # gelöscht += 1
        # branch_start_time = time.perf_counter()
        bestes_blatt = branch(zwischenspeicher, bestes_blatt)
        # branch_time += (time.perf_counter() - branch_start_time)
        # print(baum)
        # if aua%1000==0:
        # print("Aua es tut so weh:", len(baum))
        # print("Es wurden so viele Knoten hinzugefügt und gelöscht", hinzugefügt, gelöscht)
        # hinzugefügt= 0
        # gelöscht = 0
        # print("Der beste Knoten könnte noch auf so viel kommen :", max(baum, key=lambda x: x[2])[2])
    #print("BnB hat so viele Runden gebraucht :", aua)
    bnb_end_time = time.perf_counter()
    #print("Die Branch_Bound Lösung ist: ", bestes_blatt[0])  # , "mit den Elementen:", sorted(bestes_blatt[1]))
    bnb_laufzeit = bnb_end_time - bnb_start_time
    #print("Die Branch_Bound Laufzeit war:", bnb_laufzeit)
    # print("Bound hat so lange gebraucht:", bound_time)
    #print("Das kopieren hat so lange gebraucht: ", suchen_time)
    # print("Branch hat so lange gebraucht: ", branch_time)
    bnb_gesamtzeit += bnb_laufzeit
    core_gesamtzeit += core_laufzeit

print("Die Durchschnittliche Core Laufzeit war:", core_gesamtzeit/runden)
print("Die Durchschnittliche Branch_Bound Laufzeit war:", bnb_gesamtzeit/runden)
