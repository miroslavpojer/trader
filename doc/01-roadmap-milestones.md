# Trading Edge Roadmap (EPICs & Tasks)

## 🟢 Epic 1: MVP + Backtest
**Popis:** Postavit první funkční prototyp systému mean reversion a otestovat, zda má edge na historických datech.  
**Tasks:**
- [ ] Import historických dat (OHLCV, fundamenty)
- [ ] Vyřešit survivorship bias (zahrnout i zaniklé tituly)
- [ ] Implementovat výpočet Z-score reziduí, Hurst exponentu, OU half-life
- [ ] Definovat vstupní a výstupní logiku (entry, exit, stop, time-stop)
- [ ] Napsat základní backtestovací engine (vectorized nebo event-driven)
- [ ] Vyhodnocení metrik (win-rate, PF, max DD, Sharpe)

---

## 🎯 Milestone 2: Robustnost & Risk Layer

### 🟡 Epic 2: Robustnost
**Popis:** Zajistit, aby systém nebyl přeoptimalizovaný a obstál i mimo sample.  
**Tasks:**
- [ ] Přidat walk-forward testy (rolling rekalibrace parametrů)
- [ ] Implementovat Monte Carlo permutace (shuffle pořadí obchodů)
- [ ] Přidat stres testy parametrů (Z-threshold, half-life, ATR)
- [ ] Otestovat cross-validation na různých tickerech/sektorech
- [ ] Prohnat systém krizovými obdobími (2008, 2020)

### 🔵 Epic 3: Risk Management
**Popis:** Implementovat systém ochrany účtu a řízení rizika.  
**Tasks:**
- [ ] Přidat position sizing fixní (např. max 1 % účtu / obchod)
- [ ] Implementovat **volatility targeting** (ATR-based sizing)
- [ ] Přidat stop-loss a time-stop logiku (na základě Z a half-life)
- [ ] Přidat diverzifikaci přes tickery, páry, sektory
- [ ] Kill-switch (pozastavit systém při DD > X % nebo Hurst > 0.5)
- [ ] Výpočet celkového portfolio risku (součet expozic, korelace)

---

## ⚙️ Milestone 3: Adaptace & Governance

### 🟠 Epic 4: Adaptace
**Popis:** Udržet edge dlouhodobě průběžnou adaptací.  
**Tasks:**
- [ ] Přidat čtvrtletní rekalibraci parametrů (automatizace)
- [ ] Přidat roční update universa podle fundamentů
- [ ] Monitoring trhu: rolling Hurst, volatilita, half-life drift
- [ ] Dashboard diagnostiky (rolling WR, PF, MFE/MAE, slippage trend)
- [ ] Přidat **více timeframe filtrů** (daily + weekly potvrzení signálu)
- [ ] Implementovat **meta-systém adaptivní vypínač** (pauza při degradaci)

### 🟣 Epic 5: Governance
**Popis:** Řídit systém jako „firmu“ s reportingem a auditem.  
**Tasks:**
- [ ] Vést obchodní deník (log signálů + fundament poznámky)
- [ ] Generovat měsíční a čtvrtletní report výkonu vs. očekávání
- [ ] Implementovat kontrolu přeoptimalizace (srovnání parametrů)
- [ ] Peer review (2. pohled nebo alespoň simulovaný audit)
- [ ] Definovat pravidla pro manuální zásahy (kdy je smíš udělat)

---

## 🛠️ Milestone 4: Infrastructure & Automatizace

### 🟤 Epic 6: Infrastructure & Automatizace
**Popis:** Automatizovat screening, alerty a workflow.  
**Tasks:**
- [ ] Implementovat nightly screening kandidátů
- [ ] Posílat alerty (mail/telegram)
- [ ] Přidat poluautomatickou exekuci (rychlé potvrzení)
- [ ] Archivovat data (rezidua, Z, Hurst, fundamenty)
- [ ] Nastavit periodický backtest re-run po updatech
- [ ] Přidat **cash booster** (automatický parking do T-Bill ETF)
- [ ] CI/CD pipeline (automatické testy při update kódu)
- [ ] Docker/venv orchestrace (přenositelnost)
- [ ] Scheduler (Airflow/Prefect nebo cron DAG)

---

## 📈 Milestone 5: Portfolio Construction & Strategy Suite

### 🔴 Epic 7: Portfolio konstrukce & Performance Enhancers
**Popis:** Vytvořit finální portfolio s hlavní strategií a overlayi pro zvýšení výkonu.  
**Tasks:**
- [ ] Definovat hlavní strategii (high-conviction MR, 10–20 obchodů/rok)
- [ ] Přidat párový overlay long-only (30–60 obchodů/rok)
- [ ] Rozšířit overlay o víc diverzifikovaných párů (ETF, cross-sektory)
- [ ] Přidat sezónní/kalendářní edge (např. turn-of-month)
- [ ] Otestovat různé kombinace main + overlay
- [ ] Optimalizovat cílení: 25–30 % roční výnos při rozumné volatilitě
- [ ] Přidat další pipelines (trend following, ETF rotation, panic rebound, breakout retest)
- [ ] Meta-allokátor kapitálu (priority a kill-switch per pipeline)
- [ ] Correlation matrix & hedging logika

---

## 🌐 Milestone 6: Monitoring & Meta-Layer

### 🟣 Epic 8: Monitoring & Analytics (nový)
**Popis:** Centralizovaný monitoring a meta-řízení.  
**Tasks:**
- [ ] Centralizovaný dashboard (strategies performance, risk, corr)
- [ ] Rolling diagnózy (WR, PF, DD)
- [ ] Alerty na degradaci edge
- [ ] Meta-allocator kapitálu podle režimu trhu
