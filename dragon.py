"""
dragon.py

Modulo per la generazione del frattale Drago di Heighway con il
metodo delle trasformazioni iterate.

ALGORITMO
=========
Si parte da un segmento di lunghezza L (lista di 2 punti).
Ad ogni iterazione si applicano DUE trasformazioni:
  T1: rotazione di angolo alpha    +  scala di cos(alpha)
  T2: rotazione di (90 + alpha)    +  scala di sin(alpha)
                                   +  traslazione (L, 0)

Si combinano i due risultati: punti1 concatenati a punti2 letti al
contrario (escluso l'ultimo punto, perche' coincide col primo di punti1).

Dopo N iterazioni il numero totale di punti e' 2^N + 1.
Es. 12 iterazioni -> 4097 punti, 16 iterazioni -> 65537 punti.
"""

# numpy: libreria per calcoli numerici. Indispensabile per gestire
# matrici e operazioni vettoriali (molto piu' veloce di liste Python).
import numpy as np

# matplotlib serve per disegnare il frattale come immagine.
# Importante: per i server (come Codespaces) bisogna usare il backend
# "Agg", che non cerca di aprire una finestra grafica (non c'e' display).
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Librerie standard Python
import os                                # per cartelle/file
import random                            # per parametri casuali
from datetime import datetime            # per timestamp nei nomi


def matrice_rotazione(angolo_rad):
    """
    Restituisce la matrice 2x2 di rotazione per un angolo (in radianti).

    La matrice di rotazione in 2D di angolo theta e':
        | cos(theta)  -sin(theta) |
        | sin(theta)   cos(theta) |

    Moltiplicandola per un vettore (x, y) si ottiene il vettore
    ruotato di theta in senso antiorario.
    """
    c = np.cos(angolo_rad)
    s = np.sin(angolo_rad)
    # np.array crea una matrice 2x2
    return np.array([[c, -s],
                     [s,  c]])


def genera_drago(angolo_deg=45, iterazioni=12, lunghezza=1.0):
    """
    Genera l'array di punti del Drago di Heighway.

    Args:
        angolo_deg (int): angolo alpha in gradi (consigliato 20-60).
            45 e' il caso classico (triangolo isoscele).
        iterazioni (int): numero di passi (consigliato 8-16).
        lunghezza (float): lunghezza L del segmento iniziale.

    Returns:
        np.ndarray: matrice (2, N) con coordinate x (riga 0) e y (riga 1).
            N = 2^iterazioni + 1
    """
    # Conversione angolo in radianti (numpy lavora in radianti, non gradi)
    alpha = np.radians(angolo_deg)
    cos_a = np.cos(alpha)
    sin_a = np.sin(alpha)

    # === Definiamo le 2 matrici di trasformazione ===
    # Moltiplicare la matrice di rotazione per uno scalare equivale
    # a fare la rotazione e poi una contrazione (scala).
    R1 = matrice_rotazione(alpha) * cos_a
    R2 = matrice_rotazione(np.pi / 2 + alpha) * sin_a

    # Vettore traslazione per T2: spostamento di L verso destra.
    # Forma colonna (2x1) cosi' si somma riga per riga ai punti
    # grazie al "broadcasting" di numpy.
    traslazione = np.array([[lunghezza], [0.0]])

    # === Segmento iniziale: 2 punti ===
    # Riga 0 = coordinate x (primo punto in 0, secondo in L).
    # Riga 1 = coordinate y (entrambi a 0: segmento orizzontale).
    punti = np.array([[0.0, lunghezza],
                      [0.0, 0.0]])

    # === Loop principale: ad ogni iter raddoppia il numero di punti ===
    for _ in range(iterazioni):
        # Applica T1 a tutti i punti (l'operatore @ di numpy
        # e' la moltiplicazione tra matrici)
        punti1 = R1 @ punti

        # Applica T2 ai punti, poi trasla
        punti2 = R2 @ punti + traslazione

        # Combiniamo le due liste:
        # - punti1 in ordine normale
        # - punti2 in ordine inverso, escludendo l'ultimo punto
        #   (perche' coincide col primo punto di punti1)
        # punti2[:, -2::-1] significa:
        #   :       prendi tutte le righe (x e y)
        #   -2::-1  parti dal penultimo, vai all'inizio, passo -1
        # np.hstack concatena orizzontalmente (affianca)
        punti = np.hstack([punti1, punti2[:, -2::-1]])

    return punti


def salva_drago_png(angolo_deg, iterazioni,
                    output_dir="static/generated",
                    colore="#0f172a"):
    """
    Genera il Drago, salva PNG, restituisce il nome del file.

    Args:
        angolo_deg (int): angolo alpha in gradi
        iterazioni (int): numero di iterazioni
        output_dir (str): cartella destinazione del PNG
        colore (str): colore della linea in formato hex

    Returns:
        str: nome del file generato (senza percorso completo)
    """
    # 1. Genera l'array dei punti
    punti = genera_drago(angolo_deg, iterazioni)

    # 2. Adatta lo spessore della linea al numero di punti.
    # Frattali con tanti punti vicini, se hanno linee spesse,
    # diventano blocchi neri illeggibili.
    n_punti = punti.shape[1]
    if n_punti > 50000:
        linewidth = 0.3
    elif n_punti > 10000:
        linewidth = 0.5
    else:
        linewidth = 0.8

    # 3. Crea la figura matplotlib (10x10 pollici, 120 DPI)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=120)

    # Disegna la linea che collega tutti i punti (riga 0 = x, riga 1 = y)
    ax.plot(punti[0], punti[1], color=colore, linewidth=linewidth)

    # set_aspect("equal") = stessa scala su x e y (sennò si deforma)
    ax.set_aspect("equal")

    # Niente assi: vogliamo solo il frattale
    ax.axis("off")

    # 4. Crea cartella di destinazione se non esiste
    os.makedirs(output_dir, exist_ok=True)

    # 5. Costruisci nome file unico con timestamp.
    # Formato: drago_a45_i12_20250503_153022.png
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_file = f"drago_a{angolo_deg}_i{iterazioni}_{timestamp}.png"
    percorso = os.path.join(output_dir, nome_file)

    # 6. Salva l'immagine.
    # transparent=True: sfondo trasparente.
    # bbox_inches="tight": ritaglia bordi vuoti.
    plt.savefig(percorso,
                transparent=True,
                bbox_inches="tight",
                pad_inches=0.1)

    # 7. Chiudi la figura per liberare memoria
    plt.close(fig)

    return nome_file


def parametri_casuali_plausibili():
    """
    Restituisce (angolo, iterazioni) casuali ma sensati.

    L'angolo influenza la forma del drago:
      25-35: drago piu' allungato e sottile
      40-50: forme classiche simmetriche (45 = isoscele)
      55-65: drago piu' compatto e arricciato

    Le iterazioni controllano il dettaglio:
      10-12: dettaglio medio, generazione veloce
      13-14: dettaglio alto, ancora rapido

    Returns:
        tuple: (angolo_gradi, iterazioni)
    """
    angoli_possibili = [25, 28, 30, 33, 35, 38, 40, 43,
                        45, 48, 50, 53, 55, 58, 60]
    angolo = random.choice(angoli_possibili)
    iterazioni = random.randint(10, 14)
    return angolo, iterazioni


# === Test rapido se eseguito direttamente ===
# Se lanci "python dragon.py" dal terminale, viene generato un PNG
# di prova nella cartella corrente. Utile per verificare che il
# modulo funzioni senza dover avviare Flask.
if __name__ == "__main__":
    nome = salva_drago_png(45, 12, output_dir=".")
    print(f"Generato file di prova: {nome}")