# Trader Skeleton (Epic 1 — MVP + Backtest)

Kompletní skeleton pro mean‑reversion pipeline: **raw → clean → features → signals → risk → backtest → eval**.

## Rychlý start
```bash
python -m venv .venv && source .venv/bin/activate  # Win: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m trader.cli --config config/config.example.yml run
```

## Struktura
- `trader/` — zdrojový kód (utils, core, cli)
- `config/` — příklad konfigurace + schéma pro raw vstup
- `tests/` — pytest unit testy (syntetická data)
- `reports/` — CSV výstupy backtestu
- `docs/` + `mkdocs.yml` — volitelná dokumentace

> Pozn.: Fundamenty řeš mimo tuto pipeline (výběr universa).
