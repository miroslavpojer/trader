# 📑 Trading Summary – Mean Reversion & Trend Following

---

## 🔹 Strategie 1: Mean Reversion (návrat k průměru)
**Princip:** cena se krátkodobě odchýlí od průměru → očekávám návrat zpět.  
- Funguje, když trh **netrenduje** (boční pásmo, ADX < 20–22, Hurst < 0.5).  
- Typický holding: **2–5 dní**.  
- Riziko: místo návratu k průměru se průměr posune k ceně (trend se rozjede).

### ✅ Quant setup (vyžaduje výpočty)
**BUY:**
- Hurst < 0.45  
- Close pod dolní Bollinger (20, 2σ)  
- Z-score < –2.0  
- RSI(2) < 5  
- Stop-loss: swing low –0.7×ATR(14)  
- Exit: SMA20 nebo RSI(2) > 70  

**SELL:**
- Hurst < 0.45  
- Close nad horní Bollinger (20, 2σ)  
- Z-score > +2.0  
- RSI(2) > 95  
- Stop-loss: swing high +0.7×ATR  
- Exit: SMA20 nebo RSI(2) < 30  

### ✅ Yahoo setup (co jde vidět rovnou na Yahoo Finance)
**BUY:**
- Close pod dolní Bollinger (20,2)  
- RSI(14) < 30  
- SMA200 stoupá (firma v uptrendu dlouhodobě)  
- Exit: SMA20 nebo SMA50  

**SELL:**
- Close nad horní Bollinger (20,2)  
- RSI(14) > 70  
- SMA200 klesá  
- Exit: SMA20 nebo SMA50  

---

## 🔹 Strategie 2: Trend Following
**Princip:** *„trend má tendenci pokračovat déle, než si lidé myslí“*.  
- Funguje, když trh **trenduje** (ADX > 25, Hurst > 0.5).  
- Typický holding: **dny až týdny**.  

### ✅ Setup
**BUY:**
- Proražení rezistence nebo nové high  
- Cena nad SMA50 a SMA200  
- Stop-loss: pod swing low / pod SMA50 / trailing ATR  
- Exit: trailing stop (2×ATR, 50denní MA)  

**SELL:**
- Proražení supportu nebo nové low  
- Cena pod SMA50 a SMA200  
- Stop-loss: nad swing high / trailing ATR  
- Exit: trailing stop  

---

## 🔹 Fundamentální filtry (pro výběr stabilních akcií)
Cílem je omezit obchodování na **kvalitní a likvidní tickery**, kde mean reversion i trend-follow fungují spolehlivěji.  

- **Velikost & likvidita:**  
  - Market cap > 10 mld USD  
  - Denní objem > 1M akcií  
  - Úzký spread  

- **Ziskovost a růst:**  
  - P/E < 30  
  - EPS růst > 5–10 % ročně (3–5 let)  
  - ROE > 10 %  

- **Finanční zdraví:**  
  - Debt/Equity < 0.5–0.7  
  - Pozitivní free cash flow  

- **Sektorová diverzifikace:**  
  - Mix sektorů (tech, healthcare, consumer staples, industrials)  

---

## 🔹 Důležité doplnění
- **Krátkodobý výkyv** = cena se rychle odchýlí od průměru (např. –2σ pod SMA20).  
- **Slippage** = rozdíl mezi očekávanou a skutečnou cenou exekuce → důležité u nelikvidních tickerů.  
- **Likvidní ticker** = akcie s velkým objemem a úzkým spreadem (např. AAPL, MSFT).  
- **Stop-loss** a **risk management** jsou klíčové → doporučeno riskovat max. 0.5–1 % účtu na obchod.  
- **Diversifikace signálů:** Pro 5 paralelních obchodů je třeba sledovat alespoň 50–100 likvidních tickerů (např. z S&P 100/500).  
- **Overfitting (přeladění):** Pozor na ladění parametrů (např. RSI < 27.5 místo 30 jen proto, že to vyšlo líp v backtestu). Důležité je testovat robustnost (±20 % parametrů, walk-forward test).  
- **Časový limit pro mean reversion:** pokud se cena nevrátí k průměru do 5 dní → exit, i se ztrátou.  

---

📌 **Shrnutí:**
- Máš teď dva typy setupů: **Quant (s výpočty)** a **Yahoo (vizuální)**.  
- Mean reversion funguje při **Hurst < 0.5** a bočním trhu.  
- Trend following funguje při **Hurst > 0.5** a rozjetém trendu.  
- Pro stabilitu používej **likvidní tickery s kvalitním fundamentem**.  
- Na 5 paralelních obchodů musíš mít **větší watchlist (50–100 akcií)**.  
