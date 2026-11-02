
import csv

FILE = "dati/pokemon.csv"


def carica(nomefile):
    """Legge il CSV, converte i numeri e scarta le righe sporche."""

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

                for colonna in statistiche:
                    riga[colonna] = int(riga[colonna])

                if not riga["pokemon"] or not riga["type_1"]:
                    raise ValueError

                dati.append(riga)

            except (ValueError, TypeError, KeyError):
                scartate += 1

    return dati, scartate


def domanda1(dati):
    """Conta i Pokemon per tipo principale e i secondi tipi."""

    conteggio = {}

    for p in dati:
        tipo = p["type_1"]

        conteggio[tipo] = conteggio.get(tipo, 0) + 1

    tipo_comune = max(conteggio, key=conteggio.get)

    secondo_tipo = sum(
        1 for p in dati
        if p["type_2"].strip() not in ("", "NA")
    )

    print("\n--- DOMANDA 1 ---")

    for tipo, numero in sorted(
        conteggio.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(tipo, ":", numero)

    print("Tipo più comune:", tipo_comune)
    print("Pokemon con secondo tipo:", secondo_tipo)

    return {
        "conteggi": conteggio,
        "tipo_piu_comune": tipo_comune,
        "secondo_tipo": secondo_tipo
    }


def domanda2(dati):
    """Calcola minimo, massimo e media della statistica totale."""

    totali = []

    for p in dati:
        totale = (
            p["hp"] +
            p["attack"] +
            p["defense"] +
            p["special_attack"] +
            p["special_defense"] +
            p["speed"]
        )

        p["totale"] = totale
        totali.append(totale)

    minimo = min(totali)
    massimo = max(totali)
    media = sum(totali) / len(totali)

    piu_deboli = [
        p["pokemon"] for p in dati
        if p["totale"] == minimo
    ]

    piu_forti = [
        p["pokemon"] for p in dati
        if p["totale"] == massimo
    ]

    print("\n--- DOMANDA 2 ---")

    print("Statistica minima:", minimo)
    print("Pokemon più deboli:", ", ".join(piu_deboli))

    print("Statistica massima:", massimo)
    print("Pokemon più forti:", ", ".join(piu_forti))

    print("Statistica media:", round(media, 2))

    return {
        "minimo": minimo,
        "pokemon_deboli": piu_deboli,
        "massimo": massimo,
        "pokemon_forti": piu_forti,
        "media": round(media, 2)
    }


def domanda3(dati):
    """Conta i Pokemon per generazione e calcola la media."""

    generazioni = {}

    for p in dati:
        generazione = p["generation_id"].strip()

        if generazione == "" or generazione == "NA":
            generazione = "sconosciuta"

        if generazione not in generazioni:
            generazioni[generazione] = []

        generazioni[generazione].append(p["totale"])

    tabella = []

    for generazione, valori in generazioni.items():
        numero = len(valori)
        media = sum(valori) / numero

        tabella.append([
            generazione,
            numero,
            round(media, 2)
        ])

    tabella.sort(
        key=lambda r: (
            r[0] == "sconosciuta",
            int(r[0]) if r[0] != "sconosciuta" else 99
        )
    )

    print("\n--- DOMANDA 3 ---")

    for riga in tabella:
        print(
            "Generazione:", riga[0],
            "| Pokemon:", riga[1],
            "| Media:", riga[2]
        )

    return tabella


def domanda4(dati):
    """Trova i Pokemon più pesanti, leggeri e il rapporto più alto."""

    peso_massimo = max(p["weight"] for p in dati)
    peso_minimo = min(p["weight"] for p in dati)

    piu_pesanti = [
        p["pokemon"] for p in dati
        if p["weight"] == peso_massimo
    ]

    piu_leggeri = [
        p["pokemon"] for p in dati
        if p["weight"] == peso_minimo
    ]

    rapporti = []

    for p in dati:
        if p["height"] > 0:
            rapporto = p["weight"] / (p["height"] ** 2)

            rapporti.append((
                p["pokemon"],
                p["weight"],
                p["height"],
                rapporto
            ))

    rapporti.sort(key=lambda x: x[3], reverse=True)

    soglia = rapporti[4][3]

    primi_cinque = [
        r for r in rapporti
        if r[3] >= soglia
    ]

    print("\n--- DOMANDA 4 ---")

    print("Peso massimo:", peso_massimo, "kg")
    print("Pokemon più pesanti:", ", ".join(piu_pesanti))

    print("Peso minimo:", peso_minimo, "kg")
    print("Pokemon più leggeri:", ", ".join(piu_leggeri))

    print("\nPrimi 5 per rapporto peso/altezza^2:")

    for nome, peso, altezza, rapporto in primi_cinque:
        print(
            nome,
            "| Peso:", peso,
            "| Altezza:", altezza,
            "| Rapporto:", round(rapporto, 2)
        )

    return {
        "peso_massimo": peso_massimo,
        "piu_pesanti": piu_pesanti,
        "peso_minimo": peso_minimo,
        "piu_leggeri": piu_leggeri,
        "primi_cinque": primi_cinque
    }


def domanda_nostra(dati):
    """Quale tipo principale di Pokemon è più veloce in media?"""

    velocita = {}

    for p in dati:
        tipo = p["type_1"]

        if tipo not in velocita:
            velocita[tipo] = []

        velocita[tipo].append(p["speed"])

    medie = []

    for tipo, valori in velocita.items():
        media = sum(valori) / len(valori)
        medie.append((tipo, len(valori), round(media, 2)))

    medie.sort(key=lambda x: x[2], reverse=True)

    print("\n--- DOMANDA 5 ---")

    for tipo, numero, media in medie:
        print(
            tipo,
            "| Pokemon:", numero,
            "| Velocità media:", media
        )

    print("\nTipo più veloce:", medie[0][0])
    print("Velocità media:", medie[0][2])

    return medie


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""

    with open(nomefile, "w", encoding="utf-8",
              newline="") as file:

        scrittore = csv.writer(file)

        scrittore.writerow(intestazione)
        scrittore.writerows(tabella)

    print("\nFile", nomefile, "creato correttamente!")


def main():
    dati, scartate = carica(FILE)

    print("Righe buone:", len(dati))
    print("Righe scartate:", scartate)

    if not dati:
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

    main()
