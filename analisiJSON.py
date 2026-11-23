
import json

FILE = "dati/pokemon.json"


def carica(nomefile):
    """Legge il JSON, converte i numeri e scarta le righe sporche."""

    dati = []
    scartate = 0

    statistiche = [
        "hp", "attack", "defense",
        "special_attack", "special_defense", "speed"
    ]

    with open(nomefile, "r", encoding="utf-8") as file:
        pokemon = json.load(file)

        for riga in pokemon:
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
        generazione = str(p["generation_id"]).strip()

        if generazione == "" or generazione == "NA":
            generazione = "sconosciuta"

        if generazione not in generazioni:
            generazioni[generazione] = []

        generazioni[generazione].append(p["totale"])

    tabella = []

    for generazione, valori in generazioni.items():
        numero = len(valori)
        media = sum(valori) / numero

        tabella.append({
            "generazione": generazione,
            "numero_pokemon": numero,
            "media_statistica_totale": round(media, 2)
        })

    tabella.sort(
        key=lambda r: (
            r["generazione"] == "sconosciuta",
            int(r["generazione"])
            if r["generazione"] != "sconosciuta" else 99
        )
    )

    print("\n--- DOMANDA 3 ---")

    for riga in tabella:
        print(
            "Generazione:", riga["generazione"],
            "| Pokemon:", riga["numero_pokemon"],
            "| Media:", riga["media_statistica_totale"]
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

            rapporti.append({
                "pokemon": p["pokemon"],
                "peso": p["weight"],
                "altezza": p["height"],
                "rapporto": rapporto
            })

    rapporti.sort(
        key=lambda x: x["rapporto"],
        reverse=True
    )

    primi_cinque = rapporti[:5]

    print("\n--- DOMANDA 4 ---")

    print("Peso massimo:", peso_massimo, "kg")
    print("Pokemon più pesanti:", ", ".join(piu_pesanti))

    print("Peso minimo:", peso_minimo, "kg")
    print("Pokemon più leggeri:", ", ".join(piu_leggeri))

    print("\nPrimi 5 per rapporto peso/altezza^2:")

    for r in primi_cinque:
        print(
            r["pokemon"],
            "| Peso:", r["peso"],
            "| Altezza:", r["altezza"],
            "| Rapporto:", round(r["rapporto"], 2)
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

        medie.append({
            "tipo": tipo,
            "numero_pokemon": len(valori),
            "velocita_media": round(media, 2)
        })

    medie.sort(
        key=lambda x: x["velocita_media"],
        reverse=True
    )

    print("\n--- DOMANDA 5 ---")

    for r in medie:
        print(
            r["tipo"],
            "| Pokemon:", r["numero_pokemon"],
            "| Velocità media:", r["velocita_media"]
        )

    print("\nTipo più veloce:", medie[0]["tipo"])
    print("Velocità media:", medie[0]["velocita_media"])

    return medie


def scrivi_risultati(nomefile, tabella):
    """Scrive i risultati in un file JSON."""

    with open(nomefile, "w", encoding="utf-8") as file:

        json.dump(
            tabella,
            file,
            indent=4,
            ensure_ascii=False
        )

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

    domanda4(dati)

    domanda_nostra(dati)

    scrivi_risultati(
        "risultati.json",
        tabella
    )


if __name__ == "__main__":
    main()
