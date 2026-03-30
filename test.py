import random
from itertools import combinations
from typing import List, Tuple
import copy
import time
from queue import PriorityQueue


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
"""Rundenübergreifende Variablen"""
core_gesamtzeit =0
bnb_gesamtzeit = 0
geeks_gesamtzeit =0
pareto_gesamtzeit =0
geeks_relaxzeit= 0
ichs_relaxzeit=0
geeks_runden =0
ichs_runden =0
richtig = 0
runden = 10
bound_time= 0
global suchen_time
suchen_time = 0
global sortieren_time
sortieren_time =0
set = 2
clusteranzahl = 4 #Wenn Set == 2 relevant


"""Anzahl Runden wird festgelegt und Array initialisiert"""
for i in range(runden):
    print(i)
    items = []
    elemente = 100
    gesamt_volumen = int(4*1e11)
    arr=[]

    """Die Items werden zufällig erstellt"""
    def items_create(set):
        if set == 0:
            """Komplett Zufällige Werte"""
            for i in range(elemente):
                weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                value = random.randint(1, int(1e10))  # zufälliger Wert zwischen 1 und 10000000000
                arr.append(Item(weight, value))
                stonks = value / weight  # Effizienz der Items
                number = i
                items.append((weight, value, stonks, number))
        if set == 1:
            """Value Wert knapp über Weight Wert"""
            for i in range(elemente):
                weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                value = int(weight * (1 + (random.random() / 10)))  # Value ist 0-1/X höher als Weight
                arr.append(Item(weight, value))
                stonks = value / weight  # Effizienz der Items
                number = i
                items.append((weight, value, stonks, number))
        if set == 2:
            for c in range(clusteranzahl):
                center_weight = random.randint(1, int(1e10))
                center_value = random.randint(1, int(1e10))  # zufälliger Wert zwischen 1 und 10000000000
                for i in range(int(elemente/clusteranzahl)):
                    weight = int(center_weight * (1 + (random.random() / 10)))
                    value = int(center_value * (1 + (random.random() / 10)))
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = (c*int(elemente/clusteranzahl))+i
                    items.append((weight, value, stonks, number))


    items_create(set)

    """Ausgabe der ersten 10 zur Kontrolle"""
    # for item in items[:10]:
    #    print(item)

    """Die Items werden nach Stonks absteigend sortiert"""
    def stonks_sort(e):
        return e[2]
    items.sort(key=stonks_sort, reverse=True)

    """Ausgabe der ersten 10 sortierten zur Kontrolle"""
    # for item in items[:10]:
    #   print(item)

    """Relaxierte Lösung Selbst Programmiert"""
    def relax_init(items, volumen, initierung):
        ichs_relax_start_time = time.perf_counter()
        global ichs_relaxzeit
        global ichs_runden
        ichs_runden+=1
        global greedy
        global greedy_weight
        core_item = -1
        inhalt = 0
        relaxierte_loesung = 0
        steigung_core = 0
        for item in items:
            core_item += 1
            """Solange noch ganze Items passen werden sie hinzugefügt"""
            if item[0] + inhalt < volumen:
                inhalt += item[0]
                relaxierte_loesung += item[1]
                if initierung == True:
                    greedy = relaxierte_loesung
                    greedy_weight = inhalt
            else:
                if initierung == True:
                    greedy = relaxierte_loesung
                    greedy_weight = inhalt
                """Das Letzte item wird noch anteilig hinzugefügt"""
                relaxierte_loesung += item[1] / (item[0] / (volumen - inhalt))
                inhalt = volumen
                steigung_core = item[2]
                break
        ichs_relaxzeit+=(time.perf_counter()-ichs_relax_start_time)
        return core_item, relaxierte_loesung, steigung_core


    core_item, relaxierte_loesung, steigung_core = relax_init(items, gesamt_volumen, True)#Relax Initialisierung für Core

    """Relaxierte Lösung von GeeksforGeeks"""
    def relax(u, n, W, arr):
        # Calculate the upper bound of profit for a node in the search tree
        if u.weight >= W:
            return 0

        profit_bound = u.profit
        j = u.level + 1
        total_weight = u.weight

        # Greedily add items to the knapsack until the weight limit is reached
        while j < n and total_weight + arr[j].weight <= W:
            total_weight += arr[j].weight
            profit_bound += arr[j].value
            j += 1

        # If there are still items left, calculate the fractional contribution of the next item
        if j < n:
            profit_bound += int((W - total_weight) * arr[j].value / arr[j].weight)

        return profit_bound

    """Tester für Relaxfunktion"""
    # print("Das Core Item ist: ", core_item)
    #print("Die Relaxierte Lösung ist: ", relaxierte_loesung)

    """Core Items werden Vorbereitet,Distanz zum Core Element wird hinzugefügt"""
    def make_core_items(items, steigung_core):

        items_for_core = []

        for w, v, s, n in items:
            dist = -((steigung_core * w) - v)

            items_for_core.append((w, v, s, dist, n))

        items_for_core.sort(key=lambda x: abs(x[3]))

        return items_for_core

    items_for_core = make_core_items(items,steigung_core)

    """Ausgabe der ersten 10 Items für Core nach Sortieren zur Kontrolle"""
    # for item in items_for_core[:10]:
    #   print(item)

    """Code zum Bruteforcen, wurde in früherer Iteration von Core verwendet"""
    def knapsack_bruteforce(items, capacity):
        n = len(items)
        best_value = 0
        best_combination = []
        """Teste alle Kombinationen von 0 bis n Items"""
        for r in range(n + 1):
            for combo in combinations(range(n), r):
                total_weight = sum(items[i][0] for i in combo)
                total_value = sum(items[i][1] for i in combo)

                if total_weight <= capacity and total_value > best_value:
                    best_value = total_value
                    best_combination = combo

        return best_value, best_combination

    """Pareto Lösung. Wird im Core verwendet"""
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


    def core(gesamt_volumen, items_for_core):
        # Start Initialisirung vom Core Rucksack
        core_start_time = time.perf_counter()
        core_volumen = gesamt_volumen-greedy_weight
        value_feste_items = greedy
        items_in_core = []
        items_in_core.append(items_for_core[0])
        current_core_value = 0


        for item in items_for_core[1:]:
            """Abbruchbedingung wenn Abstand größer als Differenz zwischen Relaxlösung und derzeitiger Core Lösung"""
            if abs(item[3]) > relaxierte_loesung - (value_feste_items + current_core_value):
                #print(f"Der Core war {len(items_in_core)} Groß")
                break
            else:
                """Nächstes Item wird dem Core hinzugefügt"""
                if item[3] > 0:  # Wenn Item über Dantzig Ray liegt
                    core_volumen += item[0]
                    value_feste_items -= item[1]
                items_in_core.append(item)
                current_core_value = pareto_knapsack(items_in_core, core_volumen)
                if len(items_in_core) == 100:
                    print("Alles im Core")
        core_end_time = time.perf_counter()
        core_laufzeit = core_end_time - core_start_time
        return value_feste_items+current_core_value, core_laufzeit

    """Startinitialisierung des Baumes"""
    bestes_blatt = []
    #print(greedy)
    bestes_blatt.append(greedy)

    bauminit = []
    bauminit.append(0)  # Aktuelle Branch Position
    bauminit.append(gesamt_volumen)
    bauminit.append(relaxierte_loesung)  # Wert Relaxlösung + feste Objekte
    bauminit.append(0)  # Wert von festen Objekten
    bauminit.append([])  # Elemente der Lösung
    baum = []
    baum.append(bauminit)
    branch_time = 0

    """Boundfunnktion um Überflüssig Knoten abzuschneiden"""
    def tom_bound(top):
        global ichs_runden
        ichs_runden += 1
        full_counter = 0
        # print(max(baum, key=lambda x: x[2])[2])
        for i in baum:
            """Wenn Upper Bound niedriger als Lower Bound wird gecuttet"""
            if i[2] < top:
                baum.pop(full_counter)
                # gelöscht +=1
            full_counter += 1


    def tom_branch(baumitem, top):
        """Das beste Item wird gewählt und auf 1 und 0 gesetzt
        Baumitem[0] = Knotenindex
        Baumitem[1] = Noch verfügbarer Platz
        Baumitem[2] = Relaxlösung der Freien Objekte + Festen Objekte (Upper Bound)
        Baumitem[3] = Wert der bereits festen Items
        """
        """Der Wert und das Gewicht des Aktuellen Branchpunktes werden aus Liste gezogen"""
        wert_item = items[baumitem[0]][1]
        gewicht_item = items[baumitem[0]][0]

        baumitem[0] += 1
        """Bestes Item wird auf 0 gesetzt"""
        baumitem[2] = relax_init(items[baumitem[0]:elemente], baumitem[1], False)[1] + baumitem[3]
        if baumitem[0] != elemente - 1 and baumitem[2] > top[0]:
            baum.append(copy.deepcopy(baumitem))

        """Bestes Item wird auf 1 gesetzt"""
        if baumitem[1] - gewicht_item >= 0:
            baumitem[3] += wert_item
            baumitem[1] -= gewicht_item
            baumitem[2] = relax_init(items[baumitem[0]:elemente], baumitem[1], False)[1] + baumitem[3]
            if baumitem[3] > top[0]:
                top[0] = baumitem[3]
                tom_bound(top[0])
            if baumitem[0] != elemente - 1 and baumitem[2] > top[0]:
                baum.append(copy.deepcopy(baumitem))

        return top
        # TODO Branchen an gebrochener Variable

    """Bruteforce auf Alles. Versagt nach 25 Elementen"""
    # best_value, best_items = knapsack_bruteforce(items_for_core, gesamt_volumen)
    # print("Bruteforce Lösung:", best_value)
    # print("Gewählte Items:", best_items)


    """Branch and Bound auf alles"""
    def BnB(bestes_blatt):
        bnb_start_time = time.perf_counter()
        while baum != []:
            index, _ = max(enumerate(baum), key=lambda x: x[1][2])
            zwischenspeicher = copy.deepcopy(baum[index])
            baum.pop(index)
            bestes_blatt = tom_branch(zwischenspeicher, bestes_blatt)
        bnb_laufzeit = time.perf_counter() - bnb_start_time
        return bestes_blatt, bnb_laufzeit



    class Node:
        def __init__(self, level, profit, weight):
            self.level = level  # Level of the node in the decision tree (or index in arr[])
            self.profit = profit  # Profit of nodes on the path from root to this node (including this node)
            self.weight = weight  # Total weight at the node

        def __lt__(self, other):
            return other.weight < self.weight  # Compare based on weight in descending order


    def bound(u, n, W, arr):
        geeks_relax_start_time = time.perf_counter()
        global geeks_relaxzeit
        # Calculate the upper bound of profit for a node in the search tree
        global geeks_runden
        geeks_runden+=1
        if u.weight >= W:
            return 0

        profit_bound = u.profit
        j = u.level + 1
        total_weight = u.weight

        # Greedily add items to the knapsack until the weight limit is reached
        while j < n and total_weight + arr[j].weight <= W:
            total_weight += arr[j].weight
            profit_bound += arr[j].value
            j += 1

        # If there are still items left, calculate the fractional contribution of the next item
        if j < n:
            profit_bound += int((W - total_weight) * arr[j].value / arr[j].weight)
        geeks_relaxzeit+=(time.perf_counter()-geeks_relax_start_time)
        return profit_bound


    def knapsack(W, arr, n):
        # Sort items based on value-to-weight ratio in non-ascending order
        arr.sort(key=lambda x: x.value / x.weight, reverse=True)

        priority_queue = PriorityQueue()
        u = Node(-1, 0, 0)  # Dummy node at the starting
        priority_queue.put(u)

        max_profit = 0

        while not priority_queue.empty():
            u = priority_queue.get()

            if u.level == -1:
                v = Node(0, 0, 0)  # Starting node
            elif u.level == n - 1:
                continue  # Skip if it is the last level (no more items to consider)
            else:
                v = Node(u.level + 1, u.profit, u.weight)  # Node without considering the next item

            v.weight += arr[v.level].weight
            v.profit += arr[v.level].value

            # If the cumulated weight is less than or equal to W and profit is greater than previous profit, update maxProfit
            if v.weight <= W and v.profit > max_profit:
                max_profit = v.profit

            v_bound = bound(v, n, W, arr)
            # If the bound value is greater than current maxProfit, add the node to the priority queue for further consideration
            if v_bound > max_profit:
                priority_queue.put(v)

            # Node considering the next item without adding it to the knapsack
            v = Node(u.level + 1, u.profit, u.weight)
            v_bound = bound(v, n, W, arr)
            # If the bound value is greater than current maxProfit, add the node to the priority queue for further consideration
            if v_bound > max_profit:
                priority_queue.put(v)

        return max_profit


    # Geeks Branch and Bound Funktion
    W = gesamt_volumen
    n = len(arr)
    geeks_start_time = time.perf_counter()
    max_profit = knapsack(W, arr, n)
    geeks_gesamtzeit += (time.perf_counter()-geeks_start_time)

    #Core Funktion
    core_value, core_laufzeit = core(gesamt_volumen, items_for_core)
    core_gesamtzeit += core_laufzeit

    # Meine BnB Funktion
    bestes_blatt, bnb_laufzeit = BnB(bestes_blatt)
    bnb_gesamtzeit += bnb_laufzeit

    # Nemhauser-Ulmann auf alles
    #pareto_start_time = time.perf_counter()
    #pareto_value = pareto_knapsack(items_for_core, gesamt_volumen)
    #pareto_gesamtzeit += time.perf_counter() - pareto_start_time

    # Tester ob alles stimmt
    if (core_value == max_profit == bestes_blatt[0]):
        richtig += 1


    if (max_profit < core_value):
        print(f"Core zu groß: {max_profit} < {core_value}")
        if max_profit ==0:
            print(items)
            print(min(enumerate(items), key=lambda x: x[0]))
        """for items in items_for_core:
            print(abs(items[3]))"""

    if (max_profit > core_value):
        print(f"Core zu klein: {max_profit} > {core_value}")
        """for items in items_for_core:
            print(abs(items[3]))"""



print("Die Durchschnittliche Core Laufzeit war:", core_gesamtzeit/runden)
#print("Die Durchschnittliche Nemhauser Ulmann Laufzeit war: ", pareto_gesamtzeit/runden)
print("Die Durchschnittliche Branch_Bound Laufzeit war:", bnb_gesamtzeit/runden)
print("Die Durchschnittliche Geeks Laufzeit war:", geeks_gesamtzeit/runden)
print("Deine Erfolgsrate liegt bei ", (richtig/runden)*100, "%")
print("Ich hab durchschnittlich so viele Runden gebraucht:", ichs_runden/runden)
print("Geeks hat durchschnittlich so viele Runden gebraucht:", geeks_runden/runden)
#print("Die Durchschnittliche Ichs_relax Laufzeit war:", ichs_relaxzeit/runden)
#print("Die Durchschnittliche Geeks_Relax Laufzeit war:", geeks_relaxzeit/runden)
#print("Die Durchschnittliche Ichs_bound Laufzeit war:", bound_time/runden)
#print("Das Kopieren hat durchschnittlich so lange geadauert:", suchen_time/runden)
#print("Das suchen des näächsten Elements dauert:", sortieren_time/runden)