"""
app.py - Server Flask della web app Drago di Heighway.

Questo file definisce il server web che gestisce le richieste HTTP
e restituisce le pagine HTML al browser.

Le 4 route principali sono:
  /          home page (introduzione ai frattali)
  /frattale  approfondimento sul Drago di Heighway
  /generatore  form per creare nuove immagini del frattale
  /archivio  galleria delle immagini gia' generate
"""

# Importiamo Flask e le funzioni che ci servono dal modulo flask:
# - Flask: la classe principale per creare l'app
# - render_template: per restituire una pagina HTML
# - request: per leggere i dati inviati dall'utente (form)
# - url_for: per costruire URL in modo sicuro (es. link ai file static)
from flask import Flask, render_template, request, url_for

# os: libreria standard per operare con file e cartelle
import os

# datetime: per gestire date e orari (servira' per l'archivio)
from datetime import datetime

# Creiamo l'oggetto app Flask.
# __name__ dice a Flask in quale file si trova: serve per
# trovare le cartelle templates/ e static/ vicino a questo file.
app = Flask(__name__)

# Cartella dove salveremo i PNG generati dal Drago.
# os.path.join unisce i pezzi del percorso usando il separatore
# giusto del sistema operativo (/ su Mac/Linux, \ su Windows).
GENERATED_DIR = os.path.join("static", "generated")


# === ROUTE 1: HOME ===
@app.route("/")
def home():
    """
    Quando l'utente apre l'URL principale (es. http://localhost:5000/),
    Flask esegue questa funzione.
    Restituisce la pagina home.html, passandole una variabile 'title'.
    """
    return render_template("home.html", title="Home")


# === ROUTE 2: PAGINA FRATTALE ===
@app.route("/frattale")
def frattale():
    """Pagina di approfondimento matematico sul Drago di Heighway."""
    return render_template("frattale.html", title="Drago di Heighway")


# === ROUTE 3: GENERATORE ===
# methods=["GET", "POST"] significa che questa route accetta sia
# richieste GET (utente apre la pagina) sia POST (utente invia il form).
@app.route("/generatore", methods=["GET", "POST"])
def generatore():
    """
    Generatore di frattali.
    - GET: mostra solo il form vuoto (con valori di default).
    - POST: l'utente ha inviato il form -> generiamo l'immagine.
    Per oggi (Giorno 1) la POST e' un placeholder. La logica vera
    arriva con il modulo dragon.py di Inter.
    """
    immagine = None       # nome del file appena generato (per ora None)
    angolo = 45           # valore di default per l'angolo alpha
    iterazioni = 12       # valore di default per le iterazioni

    if request.method == "POST":
        # Per ora non facciamo niente. Domani metteremo il codice
        # che chiama dragon.py per generare l'immagine.
        pass

    # Restituiamo la pagina generatore.html passandole le variabili.
    # Jinja (il motore di template) le inserira' nella pagina HTML.
    return render_template("generatore.html",
                           title="Generatore",
                           immagine=immagine,
                           angolo=angolo,
                           iterazioni=iterazioni)


# === ROUTE 4: ARCHIVIO ===
@app.route("/archivio")
def archivio():
    """
    Mostra le immagini gia' generate.
    Legge la cartella static/generated/ e crea una lista di
    dizionari (uno per ogni file PNG) da passare al template.
    """
    items = []  # lista che riempiremo con i dati dei PNG trovati

    # Controlla se la cartella esiste (potrebbe essere vuota all'inizio)
    if os.path.exists(GENERATED_DIR):
        # listdir() restituisce tutti i nomi di file/cartelle dentro.
        # sorted(..., reverse=True) li ordina dal piu' recente
        # (i file iniziano con timestamp tipo "drago_a45_i12_20250503_153000.png",
        #  in ordine alfabetico inverso = dal piu' nuovo al piu' vecchio).
        files = sorted(os.listdir(GENERATED_DIR), reverse=True)

        for f in files:
            # Consideriamo solo i file PNG (sicurezza)
            if f.endswith(".png"):
                # Costruiamo il percorso completo del file
                percorso = os.path.join(GENERATED_DIR, f)

                # getmtime() = "modification time", quando il file
                # e' stato modificato (in secondi dal 1970)
                ts = os.path.getmtime(percorso)

                # Convertiamo il timestamp in una data leggibile
                data = datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M")

                # Creiamo un dizionario con i dati che servono al template
                items.append({
                    "name": f,
                    "url": url_for("static", filename=f"generated/{f}"),
                    "data": data
                })

    return render_template("archivio.html", title="Archivio", items=items)


# Questo blocco viene eseguito SOLO se lanciamo il file direttamente
# (con "python app.py"). Se invece importiamo questo file da altri
# moduli, il blocco non viene eseguito.
if __name__ == "__main__":
    # debug=True: il server si ricarica automaticamente quando modifichi
    # il codice. Comodissimo durante lo sviluppo.
    app.run(debug=True)