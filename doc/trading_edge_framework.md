# Trading Edge Framework

## 1. MVP + Backtest
- **Datová základna**
  - Kvalitní historická data (OHLCV, fundamentální metriky)
  - Kontrola survivorship bias (i zaniklé tituly)
- **Signálová logika**
  - Z-score reziduí, Hurst, OU half-life, filtry na ATR a události
  - Definice vstupu, výstupu, stopů, time-stopů
- **Backtestovací engine**
  - Validace na in-sample a out-of-sample
  - Započítání komisí a slippage
- **Základní metriky**
  - Win-rate, profit factor, max drawdown, Sharpe ratio

## 2. Robustnost
- **Walk-forward testy** (rolling rekalibrace parametrů)
- **Monte Carlo permutace** (zamíchání pořadí obchodů)
- **Stres testy parametrů** (změna prahů Z, half-life, ATR)
- **Cross-validation na jiných tickerech / sektorech**
- **Outlier analýza** (reakce na krizové roky – 2008, 2020)

## 3. Risk management
- **Position sizing**
  - Max 0.25–1 % účtu risk na obchod (hlavní MR může jít víc, ale s tvrdým stopem)
- **Stop-lossy a time-stopy**
  - Definované na základě Z-score nebo OU half-life
- **Diverzifikace**
  - Více tickerů, více párů, více sektorů
- **Kill-switch**
  - Pravidla, kdy systém pozastavit (drawdown > X %, Hurst > 0.5)
- **Maximální portfolio risk**
  - Součet expozic, korelace mezi obchody

## 4. Adaptace
- **Rekalibrace parametrů** (čtvrtletně)
- **Update universa** (ročně → přidat/odebrat firmy podle fundamentu)
- **Monitoring režimu trhu**
  - Hurst, volatilita, half-life drift → adaptace frekvence a sizingu
- **Automatizovaná diagnostika**
  - Dashboard: rolling win-rate, PF, MFE/MAE, slippage trend

## 5. Governance
- **Obchodní deník** (log signálů, fundamentální poznámky)
- **Reporting**
  - Měsíční a čtvrtletní vyhodnocení výkonu vs. očekávání
- **Audit**
  - Kontrola přeoptimalizace
  - Peer review (druhý pár očí, i simulovaný)
- **Limity na zásahy**
  - Jasně dané, kdy smíš ručně vypnout / zasáhnout

## 6. Psychologie a obchodovatelnost
- **Tolerance k drawdownům** – testuj schopnost unést typické série ztrát
- **Obchodovatelný win-rate** – systém musí sedět psychice
- **Disciplína** – dodržování filtrů i při pokušení

## 7. Infrastructure & Automatizace
- **Nightly screening** (automatická detekce kandidátů)
- **Alerty** (signály → mail/telegram)
- **Rychlá exekuce** (poluautomat nebo ruční schválení)
- **Archiv dat** (rezidua, Z, Hurst, fundamenty)
- **Backtest re-run** po updatech

## 8. Portfolio konstrukce
- **Main strategie**: high-conviction MR (10–20 obchodů/rok, +15 % ročně)
- **Overlay**: akciové páry long-only (30–60 obchodů/rok, +5–10 % ročně)
- **Celkové cílení**: 20–25 % ročně při rozumné volatilitě
