# Range Trading Strategie s Fundamentálním Filtrem

- [Roadmap](#roadmap)
- 

---
## Roadmap
- WIP - sepsat stragegii do pravidel
- TODO - jak ji vylepsit a vyladit do robo reportu
  - merit uspesnost

---

## 1. Princip strategie

### Fundamentální filtr (výběr akcií)
[Finviz - screener](https://finviz.com/screener.ashx?v=171&f=fa_debteq_u0.7%2Cfa_pe_u20%2Cfa_roe_o15%2Cfa_sales3years_o10%2Cfa_sales5years_o10%2Cfa_salesyoyttm_o10%2Cta_sma200_pb&ft=4)

- **P/E** < 20
- **Debt/Equity** < 0,7
- **Rust prodeju (Sales)** > 10 % (TTM, last 3y, 5y)
- **ROE** > 15 %
- _volitelne:_ pod 200 MA (momentálně) - muze byt i nad, pokud je v uptrendu

Výsledkem je seznam zdravých firem vhodných i k dlouhodobému držení, obchodovaných v pásmu.

### Range trading (technická část)
- Primární signály z **denních svíček**.
- **Týdenní graf** pro potvrzení trendu (uptrend nebo stagnace).
- Identifikace **support/resistance** z posledních 3–12 měsíců.
- Indikátory pro potvrzení:
    - RSI (30–70) → vstup blízko 30–40, výstup nad 65–70.
    - Bollinger Bands (20) → vstup u spodního pásma, výstup u horního.
    - Volume → potvrzuje platnost supportu/resistance.
    - 200 MA → dlouhodobý filtr zdraví akcie.

### Obchodní pravidla
- **Vstup:**
    - Cena blízko supportu.
    - RSI pod 40.
    - Dotyk spodního Bollinger pásma.
- **Výstup:**
    - Cena u resistance.
    - RSI nad 65–70.
    - Trailing stop dle ATR (např. 2× ATR).
- **Stop-loss:**
    - 5–8 % pod supportem nebo 1,5–2× ATR.
- **Take profit:**
    - Šířka range (10–25 %).
    - Možnost částečných odprodejů.

### Money management
- 20 % kapitálu na pozici.
- Max 5 paralelních pozic.
- Každý vstup potvrdit fundamentem.

### Scénář „fundamentální jackpot“
- Pokud extrémně kvalitní firma dosáhne dolní hranice range → nakoupit.
- Pokud prorazí nahoru → část držet jako long-term, zbytek obchodovat range-style.

---

## 2. Workflow (praktický postup)
- Screening (Finviz, SeekingAlpha, Yahoo Finance).
- Vybrat 20–30 tickerů dle kritérií.
- Označit **A-list** (nejlepší fundamenty).
- Každý víkend: analýza týdenního grafu a range.
- Denně: sledovat grafy, nastavovat alerty.
- Vstupy a výstupy podle pravidel.

---

## 3. Rizika a doporučení
- **Fake breakouts** → počkat na potvrzení (objem, pattern).
- **Earnings** → obchodovat menší velikostí nebo vynechat.
- **Likvidita** → držet se velkých US firem (S&P 500).
- **Pravidelná reanalýza** fundamentů a range.
- **Psychologie** → vyhnout se overtradingu, FOMO a nedočkavosti.

---

## 4. Technická vylepšení

### Kombinace indikátorů
- **BUY (nákup):**
    - Cena u supportu.
    - RSI ~30–40.
    - Dotyk spodního Bollinger pásma.
    - Byčí svíčkový pattern (hammer, bullish engulfing).
    - Objem potvrzuje obrat.
    - Cena nad 200 MA a soulad s týdenním grafem.

- **SELL (prodej):**
    - Cena u resistance.
    - RSI > 65–70.
    - Dotyk horního Bollinger pásma.
    - Medvědí pattern (shooting star, bearish engulfing).
    - Objem potvrzuje vybírání zisků.
    - Trailing stop pro případ průrazu nahoru.

### Psychologická pravidla
- Dodržet plán, vyhnout se předčasným vstupům.
- Nehonit falešné průrazy.
- Vést trading deník.
- Připravit si checklist rozhodnutí.
- Trpělivost a konzistence jsou klíčové.

### IBKR tipy
- **Skenery** – filtrovat akcie dle technických podmínek.
- **Alerty** – cenové upozornění u support/resistance.
- **Bracket orders** – automatické nastavení SL a TP.
- **Trailing stop** – chránit zisky při průrazech.
- **Paper účet** – testování bez rizika.

---

## 5. Checklist pravidel
- ✅ Fundamentálně silná firma.
- ✅ Range identifikován.
- ✅ Vstup u supportu + potvrzení indikátory.
- ✅ Výstup u resistance nebo trailing stop.
- ✅ Stop-loss pod support.
- ✅ 20 % kapitálu / pozici, max 5 pozic.
- ✅ Reanalýza range a fundamentů každý týden.
