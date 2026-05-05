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

## 6. Decisioni progettuali

### Scelta della palette colori
Abbiamo scelto navy (#0f172a) + arancione (#f97316). Il navy trasmette
serietà tecnica, l'arancione richiama il fuoco del drago.

### Scelta dei font
Manrope per il body (leggibilità su schermo) e Space Grotesk per i titoli
(geometrico, in linea con l'estetica matematica).

### Limiti dei parametri
- Angolo: limitato a 10°-80° per evitare casi degeneri
- Iterazioni: massimo 18 per evitare tempi di generazione eccessivi
  (con N=18 si hanno oltre 262.000 punti)

## 7. Problemi incontrati e soluzioni

### Numero di punti che raddoppia
Con iterazioni > 16 il server rallenta. Soluzione: limite a 18 nel form
e linee più sottili nel PNG per immagini molto dettagliate.

### Combinazione delle due liste
Bisognava ricordare che la seconda lista va letta al contrario, e che
l'ultimo punto coincide col primo della prima lista. Risolto con
`np.hstack([punti1, punti2[:, -2::-1]])`.

### Lavoro distribuito su Codespaces
Tutti e tre abbiamo lavorato su GitHub Codespaces, accessibili da
browser. Questo ci ha permesso di evitare differenze di ambiente tra
i nostri PC e di collaborare anche dai computer della scuola.

## 8. Test eseguiti

- Generazione con angoli 25°, 30°, 35°, 40°, 45°, 50°, 55°, 60°: tutti OK
- Iterazioni da 8 a 16: PNG generati correttamente
- Pulsante valori casuali cliccato 20 volte: parametri sempre nei range
- Archivio con 30+ immagini: caricamento veloce, ordinamento per data
- Responsive testato su mobile (Chrome DevTools): layout adattato
- Manifest verificato in DevTools → Application: app installabile

## 9. Possibili miglioramenti

- Animazione costruzione del frattale iterazione per iterazione
- Scelta del colore del drago dal form
- Service Worker per funzionamento offline (PWA completa)
- Filtri nell'archivio (per angolo, iterazioni)
- Export anche in SVG (vettoriale)

## 10. Conclusioni

Il progetto ha unito Informatica (Flask, Python, numpy, HTML/CSS, Git,
GitHub) e Matematica (trigonometria, matrici di rotazione, frattali,
iterazione). L'organizzazione in branch e Pull Request ci ha permesso
di lavorare in parallelo, e Codespaces ci ha permesso di lavorare sia
da casa che dai PC della scuola con un ambiente identico.