import csv

FILE = "dati/pokemon.csv"


def carica(nomefile):
    dati = []
    scartate = 0

    statistiche = [
        "hp", "attack", "defense",
        "special_attack", "special_defense", "speed"
    ]

    with open(nomefile, "r", encoding="utf-8-sig", newline="") as file:
        lettore = csv.DictReader(file)

        for riga in lettore:
            try:
                riga["height"] = float(riga["height"])
                riga["weight"] = float(riga["weight"])

                for stat in statistiche:
                    riga[stat] = int(riga[stat])

                if riga["pokemon"].strip() == "":
                    continue

                if riga["type_1"].strip() == "":
                    continue

                dati.append(riga)

            except (ValueError, TypeError, KeyError):
                scartate += 1

    return dati, scartate


def domanda1(dati):
    conteggio = {}

    for p in dati:
        tipo = p["type_1"]

        if tipo not in conteggio:
            conteggio[tipo] = 0

        conteggio[tipo] += 1

    tipo_comune = max(conteggio, key=conteggio.get)

    secondo_tipo = 0

    for p in dati:
        if p["type_2"].strip() != "" and p["type_2"].strip() != "NA":
            secondo_tipo += 1

    print("\n--- DOMANDA 1 ---")

    for tipo, numero in sorted(
        conteggio.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(tipo, "-", numero)

    print("Tipo più comune", tipo_comune)
    print("Pokemon con secondo tipo", secondo_tipo)

    return conteggio, tipo_comune, secondo_tipo


def domanda2(dati):
    totali = []

    for p in dati:
        totale = 0

        totale += p["hp"]
        totale += p["attack"]
        totale += p["defense"]
        totale += p["special_attack"]
        totale += p["special_defense"]
        totale += p["speed"]

        p["totale"] = totale
        totali.append(totale)

    minimo = min(totali)
    massimo = max(totali)
    media = sum(totali) / len(totali)

    piu_deboli = []
    piu_forti = []

    for p in dati:
        if p["totale"] == minimo:
            piu_deboli.append(p["pokemon"])

        if p["totale"] == massimo:
            piu_forti.append(p["pokemon"])

    print("\n--- DOMANDA 2 ---")

    print("Statistica minima", minimo)
    print("Pokemon più deboli", ", ".join(piu_deboli))

    print("Statistica massima", massimo)
    print("Pokemon più forti", ", ".join(piu_forti))

    print("Statistica media", round(media, 2))

    return minimo, piu_deboli, massimo, piu_forti, round(media, 2)


def domanda3(dati):
    generazioni = {}

    for p in dati:
        generazione = p["generation_id"].strip()

        if generazione == "" or generazione == "NA":
            generazione = "sconosciuta"

        if generazione not in generazioni:
            generazioni[generazione] = []

        generazioni[generazione].append(p["totale"])

    tabella = []

    for generazione in generazioni:
        valori = generazioni[generazione]

        numero = len(valori)
        media = sum(valori) / numero

        tabella.append([
            generazione,
            numero,
            round(media, 2)
        ])

    tabella.sort(
        key=lambda x: (
            x[0] == "sconosciuta",
            int(x[0]) if x[0] != "sconosciuta" else 99
        )
    )

    print("\n--- DOMANDA 3 ---")

    for riga in tabella:
        print(
            "Generazione", riga[0],
            "| Pokemon", riga[1],
            "| Media", riga[2]
        )

    return tabella


def domanda4(dati):
    peso_massimo = max(p["weight"] for p in dati)
    peso_minimo = min(p["weight"] for p in dati)

    piu_pesanti = []
    piu_leggeri = []

    for p in dati:
        if p["weight"] == peso_massimo:
            piu_pesanti.append(p["pokemon"])

        if p["weight"] == peso_minimo:
            piu_leggeri.append(p["pokemon"])

    rapporti = []

    for p in dati:
        if p["height"] > 0:
            rapporto = p["weight"] / (p["height"] ** 2)

            rapporti.append([
                p["pokemon"],
                p["weight"],
                p["height"],
                rapporto
            ])

    rapporti.sort(key=lambda x: x[3], reverse=True)

    primi_cinque = rapporti[:5]

    print("\n--- DOMANDA 4 ---")

    print("Peso massimo", peso_massimo, "kg")
    print("Pokemon più pesanti", ", ".join(piu_pesanti))

    print("Peso minimo", peso_minimo, "kg")
    print("Pokemon più leggeri", ", ".join(piu_leggeri))

    print("\nPrimi 5 per rapporto peso/altezza^2")

    for p in primi_cinque:
        print(
            p[0],
            "| Peso", p[1],
            "| Altezza", p[2],
            "| Rapporto", round(p[3], 2)
        )

    return peso_massimo, piu_pesanti, peso_minimo, piu_leggeri, primi_cinque


def domanda_nostra(dati):
    velocita = {}

    for p in dati:
        tipo = p["type_1"]

        if tipo not in velocita:
            velocita[tipo] = []

        velocita[tipo].append(p["speed"])

    medie = []

    for tipo in velocita:
        valori = velocita[tipo]

        media = sum(valori) / len(valori)

        medie.append([
            tipo,
            len(valori),
            round(media, 2)
        ])

    medie.sort(key=lambda x: x[2], reverse=True)

    print("\n--- DOMANDA 5 ---")

    for riga in medie:
        print(
            riga[0],
            "| Pokemon", riga[1],
            "| Velocità media", riga[2]
        )

    print("\nTipo più veloce", medie[0][0])
    print("Velocità media", medie[0][2])

    return medie


def scrivi_risultati(nomefile, intestazione, tabella):
    with open(nomefile, "w", encoding="utf-8", newline="") as file:
        scrittore = csv.writer(file)

        scrittore.writerow(intestazione)

        for riga in tabella:
            scrittore.writerow(riga)

    print("\nFile", nomefile, "creato correttamente!")


def main():
    dati, scartate = carica(FILE)

    print("Righe buone", len(dati))
    print("Righe scartate", scartate)

    if len(dati) == 0:
        print("Nessun dato valido da analizzare.")
        return

    domanda1(dati)

    domanda2(dati)

    tabella = domanda3(dati)

    scrivi_risultati(
        "risultati.csv",
        [
            "generazione",
            "numero_pokemon",
            "media_statistica_totale"
        ],
        tabella
    )

    domanda4(dati)

    domanda_nostra(dati)


if __name__ == "__main__":
    main()