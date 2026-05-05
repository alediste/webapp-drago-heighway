# Relazione Tecnica - Web App Drago di Heighway

**Progetto multidisciplinare di Informatica e Matematica**
IIS Europa Unita - Anno scolastico 2025/2026

## Componenti del gruppo e ruoli

- **Diste**: Capogruppo + Backend 1 (server Flask, integrazione, manifest)
- **Inter**: Backend 2 (algoritmo Drago, parametri, relazione)
- **Cuse**: Frontend (HTML, CSS, design, esperienza utente)

## 1. Obiettivo del progetto

Realizzare una web app dedicata al frattale **Drago di Heighway** che permetta di:
- conoscere il concetto generale di frattale
- approfondire la matematica del Drago di Heighway
- generare immagini scegliendo i parametri (angolo, iterazioni)
- consultare un archivio dei frattali generati e scaricarli

## 2. Architettura tecnica

L'applicazione è una web app Flask con questa architettura:

- **Server Flask** (Python): gestisce le route, riceve i parametri dal form,
  invoca l'algoritmo, serve le pagine.
- **Modulo `dragon.py`**: contiene tutta la logica matematica del Drago,
  basata su numpy e matplotlib.
- **Frontend**: template HTML con Jinja per le 4 pagine, CSS per lo stile.
- **Manifest**: file JSON che rende la web app installabile come PWA.

## 3. Matematica del Drago di Heighway

Il Drago di Heighway è un frattale auto-simile costruito con il metodo
delle **trasformazioni iterate**. Si parte da un segmento di lunghezza L
(due punti). Ad ogni iterazione si applicano due trasformazioni:

- **T1**: rotazione di angolo α + scala di cos(α)
- **T2**: rotazione di (90°+α) + scala di sin(α) + traslazione di L

Le due figure ottenute vengono unite (la seconda lista letta al contrario,
escluso l'ultimo punto) e il procedimento si ripete.
Il numero di punti raddoppia ad ogni iterazione: 2^N + 1 punti dopo N passi.

Il caso classico (α = 45°) produce il triangolo rettangolo isoscele e genera
la forma più nota del Drago.

## 4. Implementazione con numpy

Per gestire il numero crescente di punti si usa numpy:
- I punti sono rappresentati come matrice 2 × N
- Le rotazioni sono moltiplicazioni con matrici 2x2 (operatore `@`)
- Le combinazioni avvengono con `np.hstack`

## 5. Struttura delle route Flask

| Route | Metodo | Descrizione |
|-------|--------|-------------|
| `/`           | GET       | Home: introduzione ai frattali |
| `/frattale`   | GET       | Approfondimento sul Drago |
| `/generatore` | GET, POST | Form parametri + generazione |
| `/casuale`    | GET       | Genera parametri casuali plausibili |
| `/archivio`   | GET       | Galleria dinamica dei PNG |

## 6. (DA COMPLETARE MERCOLEDÌ)

- Decisioni progettuali su palette, font, layout
- Problemi incontrati e soluzioni
- Test eseguiti
- Possibili miglioramenti