# Web App - Drago di Heighway

Progetto multidisciplinare di Informatica e Matematica, IIS Europa Unita.
Web app Flask per spiegare, generare e archiviare immagini del frattale
**Drago di Heighway** con il metodo delle trasformazioni iterate.

## Componenti del gruppo

| Ruolo | Persona |
|---|---|
| Capogruppo + Backend 1 | Diste |
| Backend 2 | Inter |
| Frontend | Cuse |

## Funzionalità

- Pagina Home con introduzione ai frattali
- Pagina dedicata alla matematica del Drago di Heighway
- Generatore interattivo con parametri (angolo α, iterazioni)
- Pulsante per parametri casuali plausibili
- Archivio dinamico delle immagini generate
- Download dei PNG
- Manifest JSON: installabile come web app
- Layout responsive

## Matematica

Il Drago di Heighway è costruito con il metodo delle trasformazioni iterate.
Ad ogni iterazione si applicano due trasformazioni a una lista di punti:

- **T1**: rotazione di angolo α + scala di cos(α)
- **T2**: rotazione di (90°+α) + scala di sin(α) + traslazione di L

Le due liste vengono combinate (la seconda letta al contrario) e la procedura
si ripete. Implementato con numpy per efficienza.

## Come avviare in locale

```bash
git clone https://github.com/TUOUSER/webapp-drago-heighway.git
cd webapp-drago-heighway
pip install -r requirements.txt
python app.py
```

Apri http://127.0.0.1:5000

## Come avviare su Codespaces

Click sul pulsante verde **Code** del repo → tab **Codespaces** →
**Create codespace on main**. Nel terminale del Codespace:

```bash
pip install -r requirements.txt
python app.py
```

Click sul popup "Open in Browser" che appare in basso a destra.

## Struttura del progetto

```
webapp-drago-heighway/
├── app.py              # Server Flask
├── dragon.py           # Algoritmo Drago di Heighway
├── requirements.txt
├── README.md
├── RELAZIONE.md        # Relazione tecnica
├── docs/
│   └── screenshots/    # Screenshot del sito
├── templates/          # Template Jinja
└── static/
    ├── css/
    ├── icons/          # Icone manifest
    ├── generated/      # PNG generati
    └── manifest.json
```