"""
app.py - Server Flask della web app Drago di Heighway.
Versione del Lunedi': integra dragon.py per la generazione vera.
"""

from flask import Flask, render_template, request, url_for
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Fuso orario italiano (gestisce automaticamente ora legale/solare)
FUSO_ITALIA = ZoneInfo("Europe/Rome")

# Importiamo le funzioni che Inter ha scritto in dragon.py.
# Adesso possiamo davvero generare il frattale!
from dragon import salva_drago_png, parametri_casuali_plausibili

app = Flask(__name__)
GENERATED_DIR = os.path.join("static", "generated")


@app.route("/")
def home():
    """Home page: introduzione ai frattali."""
    return render_template("home.html", title="Home")


@app.route("/frattale")
def frattale():
    """Pagina con la matematica del Drago di Heighway."""
    return render_template("frattale.html", title="Drago di Heighway")


@app.route("/generatore", methods=["GET", "POST"])
def generatore():
    """
    Generatore: GET mostra il form, POST genera l'immagine.
    """
    immagine = None
    angolo = 45
    iterazioni = 12

    if request.method == "POST":
        # request.form e' un dizionario con i dati inviati dal form.
        # try/except gestisce il caso in cui l'utente inserisce
        # qualcosa che non e' un numero (ValueError).
        try:
            # int(...) converte la stringa del form in numero.
            # .get("angolo", 45) restituisce 45 se "angolo" manca.
            angolo = int(request.form.get("angolo", 45))
            iterazioni = int(request.form.get("iterazioni", 12))

            # Validazione: limiti sensati.
            # - Angolo troppo basso/alto: drago degenere.
            # - Iterazioni troppe: file enormi e generazione lenta.
            if angolo < 10 or angolo > 80:
                angolo = 45
            if iterazioni < 1 or iterazioni > 18:
                iterazioni = 12

            # Genera il PNG e ottiene il nome del file salvato
            nome_file = salva_drago_png(angolo, iterazioni)
            immagine = nome_file
        except ValueError:
            # Se l'utente ha inserito qualcosa di non numerico, ignora
            pass

    return render_template("generatore.html",
                           title="Generatore",
                           immagine=immagine,
                           angolo=angolo,
                           iterazioni=iterazioni)


@app.route("/casuale")
def casuale():
    """
    Genera parametri casuali plausibili e li mostra nel form.
    L'utente deve poi cliccare Genera per creare l'immagine.
    """
    angolo, iterazioni = parametri_casuali_plausibili()
    return render_template("generatore.html",
                           title="Generatore",
                           immagine=None,
                           angolo=angolo,
                           iterazioni=iterazioni,
                           casuale=True)


@app.route("/archivio")
def archivio():
    """Mostra le immagini gia' generate, ordinate dalla piu' recente."""
    items = []
    if os.path.exists(GENERATED_DIR):
        files = sorted(os.listdir(GENERATED_DIR), reverse=True)
        for f in files:
            if f.endswith(".png"):
                percorso = os.path.join(GENERATED_DIR, f)
                ts = os.path.getmtime(percorso)
                # Converte il timestamp del file usando il fuso italiano
                data = datetime.fromtimestamp(ts, FUSO_ITALIA).strftime("%d/%m/%Y %H:%M")
                items.append({
                    "name": f,
                    "url": url_for("static", filename=f"generated/{f}"),
                    "data": data
                })
    return render_template("archivio.html", title="Archivio", items=items)


if __name__ == "__main__":
    app.run(debug=True)