import csv

FILE = "dati/nome-del-vostro-file.csv"


def carica(nomefile):
    """Legge il file, converte i numeri, scarta le righe sporche.
    Restituisce la lista delle righe buone e il numero di righe scartate."""
    return [], 0


def domanda1(dati):
    """Risponde alla domanda 1 della scheda."""
    return None


def domanda2(dati):
    """Risponde alla domanda 2."""
    totale = []
    for p in dati():
        totale = (
                p["hp"] +
                p["attack"] +   
                p["defense"] +
                p["special_attack"] +
                p["special_defense"] +
                p["speed"] 
        )
        p["totale"] = totale
        totale.append(totale)

        minimo = min(totale)
        massimo = max(totale)
        media = sum(totale) / len(totale)

        deboli = [p["pokemon"] for p in dati if p ["totale"] == minimo]
        forti = [p["pokemon"] for p in dati if p ["totale"] == massimo]

    return {
        "minimo": minimo,
        "pokemon_deboli": deboli,
        "massimo": massimo,
        "pokemon_forti": forti,
        "media": round(media, 2)
    }


def domanda3(dati):
    """Risponde alla domanda 3. Restituisce la tabella
    che finirà in risultati.csv: una lista di righe."""
    generazioni = {}
    for p in dati:
        generazione = p["generazioni_id"].strip()
        if generazione == "" or generazione == "NA":
            generazione = "sconosciuta"

            if generazione not in generazioni:
                generazioni[generazione] = []
                generazioni[generazione].append(p["totale"])

                tabella = []

                for generazione, valori in generazioni.items():
                    numero = len (valori)
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
    return tabella


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return None


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""
    pass


def main():
    dati, scartate = carica(FILE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
    print("Domanda 1:", domanda1(dati))
    print("Domanda 2:", domanda2(dati))
    tabella = domanda3(dati)
    scrivi_risultati("risultati.csv", ["colonna1", "colonna2"], tabella)
    print("Domanda nostra:", domanda_nostra(dati))


main()