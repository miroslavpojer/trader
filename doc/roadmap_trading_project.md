# 📌 Roadmapa – Mean Reversion Trading Project

---

## ✅ v1 – MVP (Minimum Viable Product)
**Cíl:** Spustit základní mean reversion systém s backtestem.  

### 1. Data
- Python skript na stažení historických dat z **Yahoo Finance** (`yfinance` knihovna).  
- Výběr akcií (např. z **S&P 500**).  
- Ukládat do složky `data/` → CSV nebo Parquet.  
- Metadata: seznam tickerů + informace o sektoru/industry.  

### 2. Indikátory
- Spočítat:  
  - SMA (20, 50, 200).  
  - Bollinger Bands (20, 2σ).  
  - RSI(2), RSI(14).  
  - ATR(14).  
- Výpočet pomocí `pandas_ta` nebo `ta` knihovny.  

### 3. Backtest
- Vstup: složka s daty + seznam tickerů.  
- Načíst data, spustit mean reversion logiku:  
  - Vstupy: Close < dolní BB + RSI(2)<5.  
  - Výstupy: návrat k SMA20 nebo RSI(2)>70, SL = 0.7×ATR.  
- Výstup:  
  - Per-ticker report (winrate, průměrný výnos, Sharpe, max DD).  
  - Sumarizace podle **industry** (průměrné výsledky).  

---

## 🚀 v2 – Optimalizace a univerzalizace
**Cíl:** Najít robustní nastavení fungující na více akciích.  

### 1. Optimalizace parametrů
- Použít **DEAP (genetický algoritmus)**.  
- Hledané parametry:  
  - délka SMA,  
  - Bollinger σ,  
  - RSI prahy,  
  - ATR násobky (SL/PT),  
  - holding period.  

### 2. Strategie univerzalizace
- Testovat 3 úrovně nastavení:  
  1. **Generic (univerzální)** – stejné pro všechny akcie.  
  2. **Per industry** – parametry podle sektoru (např. tech vs. utility).  
  3. **Adaptive** – parametry relativní k volatilitě (ATR, stdev).  

### 3. Validace
- Walk-forward testy (např. 2015–2020 trénink, 2021–2023 test).  
- Cross-industry validace (musí fungovat na více sektorech).  

---

## 🤖 v3 – AI rozhodovací systém
**Cíl:** Nejen ladit parametry, ale **učit AI rozhodovat BUY/SELL/HOLD**.  

### 1. Vstupy
- Časové řady indikátorů (SMA, RSI, BB, ATR, objem).  
- Fundamentální filtry (volitelně).  

### 2. Modely
- **Klasická ML**: RandomForest, XGBoost – jako baseline.  
- **NEAT (neuro-evoluce)**: neuronové sítě, které se evolučně naučí generovat signály.  
- Fitness funkce: kombinace (výnos, Sharpe, drawdown, winrate).  

### 3. Cíl
- Minimalizovat počet **loss trades**.  
- Najít **signálové vzory** mimo jednoduché prahy (nelineární kombinace indikátorů).  

---

# 📊 Shrnutí
- **v1:** backtest framework s indikátory, výsledky za tickery a industries.  
- **v2:** optimalizace parametrů pomocí DEAP, hledání univerzálního/per-industry setupu.  
- **v3:** AI řešení (NEAT nebo ML), které samo rozhoduje vstupy/výstupy s cílem zvýšit winrate a omezit ztrátové obchody.  
