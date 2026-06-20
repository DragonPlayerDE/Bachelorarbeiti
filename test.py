import random
from itertools import combinations
from typing import List, Tuple
import copy
import time
from queue import PriorityQueue
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import matplotlib.pyplot as plt
from collections import deque

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
"""Setübergreifende Variablen"""
core_werte =[]
full_core_werte =[]
pbnb_werte =[]
pbnb_half_werte =[]
nullfirst_bnb_werte =[]
bnb_werte =[]
setsize=[10,18,32,57,100,179, 316, 566, 1000]

for f in setsize:
    """Rundenübergreifende Variablen"""
    core_gesamtzeit = 0
    full_core_gesamtzeit = 0
    core_pareto_gesamtzeit = 0
    relax_bnb_gesamtzeit = 0
    bnb_gesamtzeit = 0
    ichs2_gesamtzeit = 0
    ichs3_gesamtzeit = 0
    nullfirst_gesamtzeit = 0
    geeks_gesamtzeit = 0
    pareto_gesamtzeit = 0
    global geeks_start_time
    global ichs2_start_time
    global core
    core_pareto = 0
    geeks_runden = 0
    ichs_runden = 0
    ich2_runden = 0
    richtig = 0 # Laufvariable, ob die Algoryths richtig laufen die
    abbruch_zeit = 300 #Zeit bis die Algoryths Abbrechen
    setprint = True #sollen wa das Set drucken
    vergleich = True #True == Zeit, False == Additionen
    runden = 100
    set = 1
    clusteranzahl = 2  # Wenn Set == 2 relevant
    spread = 1e9 # Wenn Set == 3 relevant
    """Anzahl Runden wird festgelegt und Array initialisiert"""
    for i in range(runden):
        print(i)
        items = []
        elemente = f
        gesamt_volumen = int(4 * 1e9*f)
        arr = []

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
                    value = weight+random.randint(1, int(1*1e9))  # Value ist X% höher als maximal Gewicht
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = i
                    items.append((weight, value, stonks, number))
            if set == 2:
                """Cluster"""
                for c in range(clusteranzahl):
                    center_weight = random.randint(int(1e9), int(1e10))
                    center_value = random.randint(int(1e9), int(1e10))  # zufälliger Wert zwischen 1 und 10000000000
                    for i in range(int(elemente / clusteranzahl)):
                        lor = random.choice([1, -1]) # Left or Right
                        weight = center_weight + (lor * random.randint(1, int(1e9)))
                        hol = random.choice([1, -1]) #Highter or Lower
                        value = center_value + (hol * random.randint(1, int(1e9)))
                        arr.append(Item(weight, value))
                        stonks = value / weight  # Effizienz der Items
                        number = (c * int(elemente / clusteranzahl)) + i
                        items.append((weight, value, stonks, number))
            if set == 3:
                """Wahrscheinlichkeitsgrüppchen"""
                # Erster Punkt völlig zufällig
                weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                value = random.randint(1, int(1e10))  # zufälliger Wert zwischen 1 und 10000000000
                arr.append(Item(weight, value))
                stonks = value / weight  # Effizienz der Items
                number = 0
                items.append((weight, value, stonks, number))
                for i in range(elemente-1):
                    # Existierenden Punkt auswählen
                    base_weight, base_value, x,y = random.choice(items)

                    # Leichte Abweichung
                    new_weight = base_weight + random.uniform(-spread, spread)
                    new_value = base_weight + random.uniform(-spread, spread)
                    # Nicht Negativ
                    new_weight = max(1, new_weight)
                    new_value = max(1, new_value)
                    arr.append(Item(new_weight, new_value))
                    stonks = new_value / new_weight  # Effizienz der Items
                    number = i+1
                    items.append((new_weight, new_value, stonks, number))
            if set == 4:
                """75% Value Wert knapp über Weight Wert, 25% Arsch"""
                for i in range(int(elemente*0.75)):
                    weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                    value = weight + random.randint(1, int(1 * 1e9))  # Value ist X% höher als maximal Gewicht
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = i
                    items.append((weight, value, stonks, number))
                for i in range(int(elemente*0.25)):
                    weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                    value = random.randint(1, weight) # Value kleiner als Weight
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = i
                    items.append((weight, value, stonks, number))
            if set == 5:
                """75% Value Wert knapp über Weight Wert, 25% Sehr gut"""
                for i in range(int(elemente*0.75)):
                    weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                    value = weight + random.randint(1, int(1 * 1e9))  # Value ist X% höher als maximal Gewicht
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = i
                    items.append((weight, value, stonks, number))
                for i in range(int(elemente*0.25)):
                    weight = random.randint(1, int(1e10))  # zufälliges Gewicht
                    value = random.randint(weight+int(1 * 1e9), int(1e10)+int(1 * 1e9)) # Value sehr viel Größer als Weight
                    arr.append(Item(weight, value))
                    stonks = value / weight  # Effizienz der Items
                    number = i
                    items.append((weight, value, stonks, number))


        items_create(set)

        if (i ==1 and setprint == True and f==1000):
            x = [item[0] for item in items]
            y = [item[1] for item in items]
            plt.xlabel("Gewicht")
            plt.ylabel("Wert")
            if (set == 0):
                plt.title('Gleichverteiltes Set')
            elif (set == 1):
                plt.title('Ähnliches Verhältnis Gewicht und Wert')
            elif (set == 2):
                plt.title((clusteranzahl , 'Cluster'))
            elif (set == 3):
                plt.title("Random Cluster")
            elif (set == 4):
                plt.title("Ähnliches Verhältnis Gewicht und Wert+schlechte Abweicher")
            plt.scatter(x, y)
            plt.axis("equal")
            plt.show()

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
            global ichs_runden
            ichs_runden += 1
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
            return core_item, relaxierte_loesung, steigung_core


        core_item, relaxierte_loesung, steigung_core = relax_init(items, gesamt_volumen, True)  # Relax Initialisierung für Core


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
        # print("Die Relaxierte Lösung ist: ", relaxierte_loesung)

        """Core Items werden Vorbereitet,Distanz zum Core Element wird hinzugefügt"""


        def make_core_items(items, steigung_core):

            items_for_core = []

            for w, v, s, n in items:
                dist = -((steigung_core * w) - v)

                items_for_core.append((w, v, s, dist, n))

            items_for_core.sort(key=lambda x: abs(x[3]))

            return items_for_core


        items_for_core = make_core_items(items, steigung_core)

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
            global core_pareto
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
                    core_pareto +=1
                    if nw <= max_weight:
                        neue_lösungen.append((nw, nv))

                pareto += neue_lösungen
                pareto = pareto_filter(pareto)
                #core_pareto += pareto.__len__()
            # beste Lösung (maximaler Wert)
            return max(pareto, key=lambda x: x[1])[1]

        def pareto_knapsack_full(item, pareto, core_volumen):
            global core_pareto
            global gesamt_volumen
            global core_pareto_gesamtzeit
            neue_lösungen = []
            max = 0
            pareto_start_time = time.perf_counter()
            for pw, pv in pareto:
                nw, nv = pw + item[0], pv + item[1]
                core_pareto += 1
                if nw <= gesamt_volumen:
                    neue_lösungen.append((nw, nv))
            core_pareto_gesamtzeit += time.perf_counter()-pareto_start_time

            pareto = pareto_filter(pareto,neue_lösungen)
                # core_pareto += pareto.__len__()
            # beste Lösung (maximaler Wert)
            for pw, pv in pareto:
                if pw > core_volumen:
                    break
                max = pv

            return max, pareto

        #neuer Pareto Filter, führt Sweep ohne sortieren aus
        def pareto_filter(alte_lösungen, neue_lösungen):
            """
            Entfernt dominierte Lösungen
            """
            pareto = []
            max_value_so_far = -1

            al = 0
            nl = 0

            while al < len(alte_lösungen) and nl < len(neue_lösungen):
                if alte_lösungen[al][0] <= neue_lösungen[nl][0]:
                    if alte_lösungen[al][1]  > max_value_so_far:
                        pareto.append((alte_lösungen[al][0], alte_lösungen[al][1]))
                        max_value_so_far = alte_lösungen[al][1]
                    al += 1
                else:
                    if neue_lösungen[nl][1] > max_value_so_far:
                        pareto.append((neue_lösungen[nl][0], neue_lösungen[nl][1]))
                        max_value_so_far = neue_lösungen[nl][1]
                    nl += 1

            # Restliche Elemente ausgeben
            while al < len(alte_lösungen):
                if alte_lösungen[al][1] > max_value_so_far:
                    pareto.append((alte_lösungen[al][0], alte_lösungen[al][1]))
                    max_value_so_far = alte_lösungen[al][1]
                al += 1

            while nl < len(neue_lösungen):
                if neue_lösungen[nl][1] > max_value_so_far:
                    pareto.append((neue_lösungen[nl][0], neue_lösungen[nl][1]))
                    max_value_so_far = neue_lösungen[nl][1]
                nl += 1


            return pareto

        #Alter Pareto filter, muss sortieren
        def pareto_filter_old(solutions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
            """
            Entfernt dominierte Lösungen
            """
            global core_pareto_gesamtzeit
            pareto_calc = time.perf_counter()
            solutions = sorted(solutions, key=lambda x: (x[0], -x[1]))
            core_pareto_gesamtzeit += (time.perf_counter() - pareto_calc)
            pareto = []
            max_value_so_far = -1
            for weight, value in solutions:
                if value > max_value_so_far:
                    pareto.append((weight, value))
                    max_value_so_far = value

            return pareto

        def core(gesamt_volumen, items_for_core, full):
            # Start Initialisirung vom Core Rucksack
            core_start_time = time.perf_counter()
            core_volumen = gesamt_volumen - greedy_weight
            value_feste_items = greedy
            items_in_core = []
            items_in_core.append(items_for_core[0])
            current_core_value = 0
            if full == True:
                pareto=[(0,0)]
                pareto.append((items_in_core[0][0],items_in_core[0][1]))

            for item in items_for_core[1:]:
                """Abbruchbedingung wenn Abstand größer als Differenz zwischen Relaxlösung und derzeitiger Core Lösung"""
                if abs(item[3]) > relaxierte_loesung - (value_feste_items + current_core_value):
                    # print(f"Der Core war {len(items_in_core)} Groß")
                    break
                else:
                    """Nächstes Item wird dem Core hinzugefügt"""
                    if item[3] > 0:  # Wenn Item über Dantzig Ray liegt
                        core_volumen += item[0]
                        value_feste_items -= item[1]
                    items_in_core.append(item)
                    if full == True:
                        current_core_value, pareto = pareto_knapsack_full(item, pareto, core_volumen)
                    if full == False:
                        current_core_value = pareto_knapsack(items_in_core, core_volumen)
                    #if len(items_in_core) == 100:
                    #    print("Alles im Core")
                    if (time.perf_counter() - core_start_time > abbruch_zeit):
                        print("Core Abbruch")
                        core_laufzeit = time.perf_counter() - core_start_time
                        return value_feste_items + current_core_value, core_laufzeit
            core_laufzeit = time.perf_counter() - core_start_time
            return value_feste_items + current_core_value, core_laufzeit


        """Startinitialisierung des Baumes"""
        bestes_blatt = []
        # print(greedy)
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


        """Branch and Bound Klappe die 2. mit Nodes und Proirity Queue"""


        class Toms_Node:
            def __init__(self, level, space, profit_bound, festwert):
                self.level = level  # Level of the node in the decision tree (or index in arr[])
                self.space = space  # Übriger Platz nach festen Items
                self.profit_bound = profit_bound  # Upper Bound
                self.festwert = festwert  # Wert der Festen Items

            def __lt__(self, other):
                return other.profit_bound < self.profit_bound  # Compare based on Upper Bound in descending order


        def priority_bound(u, n, arr):
            # Calculate the upper bound of profit for a node in the search tree
            global ich2_runden
            global relax_bnb_gesamtzeit
            if u.space < 0:
                return 0
            if u.level == 0:
                return 0

            profit_bound = u.festwert
            j = u.level + 1
            restspace = u.space
            # print(j,profit_bound)

            # Greedily add items to the knapsack until the weight limit is reached
            relax_time= time.perf_counter()
            while j < n and restspace >= arr[j].weight:
                ich2_runden += 1
                restspace -= arr[j].weight
                profit_bound += arr[j].value
                j += 1

            # If there are still items left, calculate the fractional contribution of the next item
            if j < n:
                profit_bound += int(restspace * arr[j].value / arr[j].weight)
            relax_bnb_gesamtzeit += (time.perf_counter() - relax_time)
            return profit_bound


        def priority_BnB(W, arr, n, greedy,half):
            # Sort items based on value-to-weight ratio in non-ascending order
            arr.sort(key=lambda x: x.value / x.weight, reverse=True)

            priority_queue = PriorityQueue()
            u = Toms_Node(-1, W, 0, 0)  # Dummy node at the starting
            priority_queue.put(u)

            max_profit = greedy

            while not priority_queue.empty():
                u = priority_queue.get()

                if u.level == -1:
                    v = Toms_Node(0, W, int(relaxierte_loesung), 0)  # Starting node
                elif u.profit_bound < max_profit:
                    continue  # Skip if best upper Bound < best Lower Bound
                else:
                    v = Toms_Node(u.level + 1, u.space, u.profit_bound, u.festwert)  # Nächstes Item wird hinzugefügt

                v.space -= arr[v.level].weight
                v.festwert += arr[v.level].value

                # If the cumulated weight is less than or equal to W and profit is greater than previous profit, update maxProfit
                if v.space >= 0 and v.festwert > max_profit:
                    max_profit = v.festwert

                if half == False:
                    v.profit_bound = priority_bound(v, n, arr)


                # If the bound value is greater than current maxProfit, add the node to the priority queue for further consideration
                if v.profit_bound > max_profit and v.space >0:
                    priority_queue.put(v)

                # Nächstes Item wird nicht hinzugefügt
                v = Toms_Node(u.level + 1, u.space, u.profit_bound, u.festwert)
                v.profit_bound = priority_bound(v, n, arr)
                # If the profit_bound value is greater than current maxProfit, add the node to the priority queue for further consideration
                if v.profit_bound > max_profit:
                    priority_queue.put(v)
                if(time.perf_counter()-ichs3_start_time > abbruch_zeit):
                    print("Priority Abbruch")
                    return max_profit
            return max_profit

        def nullfirst_BnB(W, arr, n, greedy,half):
            # Sort items based on value-to-weight ratio in non-ascending order
            arr.sort(key=lambda x: x.value / x.weight, reverse=True)

            nullfirst_queue = deque()
            u = Toms_Node(-1, W, int(relaxierte_loesung), 0)  # Dummy node at the starting
            nullfirst_queue.append(u)

            max_profit = greedy

            while nullfirst_queue:
                u = nullfirst_queue.popleft()

                if u.profit_bound >= max_profit and u.level < n-1:
                    v = Toms_Node(u.level + 1, u.space, u.profit_bound, u.festwert)  # Nächstes Item wird nicht hinzugefügt

                    v.profit_bound = priority_bound(v, n, arr)
                    # If the profit_bound value is greater than current maxProfit, add the node to the priority queue for further consideration
                    if v.profit_bound > max_profit:
                        nullfirst_queue.append(v)

                    # Nächstes Item wird hinzugefügt
                    v = Toms_Node(u.level + 1, u.space, u.profit_bound, u.festwert)
                    if v.level == n:
                        print("Ja scheise", n,v.level)
                    v.space -= arr[v.level].weight
                    v.festwert += arr[v.level].value

                    # If the cumulated weight is less than or equal to W and profit is greater than previous profit, update maxProfit
                    if v.space >= 0 and v.festwert > max_profit:
                        max_profit = v.festwert

                    if half == False:
                        v.profit_bound = priority_bound(v, n, arr)

                    # If the bound value is greater than current maxProfit, add the node to the priority queue for further consideration
                    if v.profit_bound > max_profit and v.space > 0:
                        nullfirst_queue.append(v)


                if(time.perf_counter()-ichs3_start_time > abbruch_zeit):
                    print("Priority Abbruch")
                    return max_profit
            return max_profit

        # Branch and Bound von Geeks for Geeks, wird nicht mehr verwendet
        class Node:
            def __init__(self, level, profit, weight):
                self.level = level  # Level of the node in the decision tree (or index in arr[])
                self.profit = profit  # Profit of nodes on the path from root to this node (including this node)
                self.weight = weight   # Total weight at the node(Nur Feste Items)

            def __lt__(self, other):
                return other.weight < self.weight  # Compare based on weight in descending order


        def bound(u, n, W, arr):
            # Calculate the upper bound of profit for a node in the search tree
            global geeks_runden
            geeks_runden += 1
            if u.weight >= W:
                return 0

            profit_bound = u.profit
            j = u.level + 1
            total_weight = u.weight
            # print(j,profit_bound)

            # Greedily add items to the knapsack until the weight limit is reached
            while j < n and total_weight + arr[j].weight <= W:
                total_weight += arr[j].weight
                profit_bound += arr[j].value
                j += 1

            # If there are still items left, calculate the fractional contribution of the next item
            if j < n:
                profit_bound += int((W - total_weight) * arr[j].value / arr[j].weight)
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

                if (time.perf_counter() - geeks_start_time > abbruch_zeit):
                    print("Geek Abbruch")
                    return max_profit

            return max_profit

        def dantzig_heuristik(items_for_core,n):
            avg_dist = 0
            max_value = 0
            for w,v,s,dist in items_for_core:
                avg_dist += dist
                if w > max_value:
                    max_value = w
            avg_dist = int(avg_dist/n)
            if avg_dist < 0.1*max_value





        # Geeks Branch and Bound Funktion
        W = gesamt_volumen
        n = len(arr)
        #geeks_start_time = time.perf_counter()
        #max_profit = knapsack(W, arr, n)
        #geeks_gesamtzeit += (time.perf_counter()-geeks_start_time)

        # Meine 2. BnB Version mit Nodes und Proirity Queue
        #ichs2_start_time = time.perf_counter()
        #mein_max_profit = priority_BnB(W, arr, n, greedy,False)
        #ichs2_gesamtzeit += (time.perf_counter() - ichs2_start_time)

        # Meine 3. BnB Version mit Nodes und Proirity Queue die Sortierung besser nutzt
        ichs3_start_time = time.perf_counter()
        mein_2_max_profit = priority_BnB(W, arr, n, greedy,True)
        ichs3_gesamtzeit += (time.perf_counter() - ichs3_start_time)

        # Meine 4. BnB Version, mit Andys Idee, erst den Pfad des nicht gewählten Elementes zu gehen
        #nullfirst_start_time = time.perf_counter()
        #nullfirst_max_profit = nullfirst_BnB(W, arr, n, greedy, True)
        #nullfirst_gesamtzeit += (time.perf_counter() - ichs3_start_time)

        # Core Funktion
        #core_value, core_laufzeit = core(gesamt_volumen, items_for_core, False)
        #core_gesamtzeit += core_laufzeit

        # Full Core Funktion
        full_core_value, core_laufzeit = core(gesamt_volumen, items_for_core, True)
        full_core_gesamtzeit += core_laufzeit


        # Meine BnB Funktion
        # bestes_blatt, bnb_laufzeit = BnB(bestes_blatt)
        # bnb_gesamtzeit += bnb_laufzeit

        # Nemhauser-Ulmann auf alles
        # pareto_start_time = time.perf_counter()
        # pareto_value = pareto_knapsack(items_for_core, gesamt_volumen)
        # pareto_gesamtzeit += time.perf_counter() - pareto_start_time

        # Tester ob alles stimmt
        if ( full_core_value ==mein_2_max_profit ):
            #core_value == mein_max_profit == == max_profit== nullfirst_max_profit
            richtig += 1

        """
        if (max_profit < core_value):
            print(f"Core zu groß: {max_profit} < {core_value}")
            if max_profit ==0:
                print(items)
                print(min(enumerate(items), key=lambda x: x[0]))
            for items in items_for_core:
                print(abs(items[3]))

        if (max_profit > core_value):
            print(f"Core zu klein: {max_profit} > {core_value}")
            for items in items_for_core:
                print(abs(items[3]))
        """

    #print("Die Durchschnittliche Core Laufzeit war:", core_gesamtzeit / runden)
    print("Die Durchschnittliche Full_Core Laufzeit war:", full_core_gesamtzeit / runden)
    print("Dabei ging soviel Zeit für die Pareto rechnung drauf:", core_pareto_gesamtzeit/runden)
    # print("Die Durchschnittliche Nemhauser Ulmann Laufzeit war: ", pareto_gesamtzeit/runden)
    # print("Die Durchschnittliche Branch_Bound Laufzeit war:", bnb_gesamtzeit/runden)
    #print("Die Durchschnittliche Geeks BnB Laufzeit war:", geeks_gesamtzeit/runden)
    #print("Die Durchschnittliche Priority BnB Laufzeit war:", ichs2_gesamtzeit / runden)
    print("Die Durchschnittliche Priority BnB Laufzeit war:", ichs3_gesamtzeit / runden)
    print("Dabei ging soviel Zeit für die Relax Berechnung drauf:", relax_bnb_gesamtzeit / runden)
    #print("Die Durchschnittliche Nullfirst BnB Laufzeit war:", nullfirst_gesamtzeit / runden)
    print("Deine Erfolgsrate liegt bei ", (richtig / runden) * 100, "%")
    # print("Ich hab durchschnittlich so viele Runden gebraucht:", ichs_runden/runden)
    print("Priority BnB hat durchschnittlich so viele Runden gebraucht:", ich2_runden / runden)
    #print("Geeks hat durchschnittlich so viele Runden gebraucht:", geeks_runden/runden)
    print("Core hat Durchschnittlich soviele Pareto Lösungen produziert:", core_pareto/runden)
    if vergleich == True:
        # core_werte.append(core_gesamtzeit/runden)
        full_core_werte.append(full_core_gesamtzeit / runden)
        # pbnb_werte.append(ichs2_gesamtzeit/runden)
        pbnb_half_werte.append(ichs3_gesamtzeit / runden)
        #bnb_werte.append(geeks_gesamtzeit / runden)
        #nullfirst_bnb_werte.append(nullfirst_gesamtzeit/runden)

    else :
        full_core_werte.append(core_pareto / runden)
        pbnb_half_werte.append(ich2_runden / runden)

# line 1 points
#x1 = setsize
#y1 = core_werte
# plotting the line 1 points
#plt.plot(x1, y1, label = "Core")

# line 1.5 points
x1 = setsize
y1 = full_core_werte
# plotting the line 1 points
plt.plot(x1, y1, label = "Core")

# line 2 points
#x2 = setsize
#y2 = pbnb_werte
# plotting the line 2 points
#plt.plot(x2, y2, label = "BnB")

# line 2.1 points
x2 = setsize
y2 = pbnb_half_werte
# plotting the line 2 points
plt.plot(x2, y2, label = "BnB")

# line 2.2 points
#x3 = setsize
#y3 = nullfirst_bnb_werte
# plotting the line 2 points
#plt.plot(x3, y3, label = "Nullfirst_BnB")

# line 2.5 points
#x2 = setsize
#y2 = bnb_werte
# plotting the line 3 points
#plt.plot(x2, y2, label = "Geek-BnB")

#scaling the axis log
plt.xscale('log')
plt.yscale('log')

# naming the x axis
plt.xlabel('Anzahl Elemente')
# naming the y axis
if vergleich == True:
    plt.ylabel('Durchschnittliche Dauer pro Runde')
else:
    plt.ylabel('Anzahl Additionen')
# giving a title to my graph
if (set==0):
    plt.title('Gleichverteiltes Set')
elif (set==1):
    plt.title('Ähnliches Verhältnis Gewicht und Wert')
elif (set==2):
    plt.title((clusteranzahl , 'Cluster'))

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()