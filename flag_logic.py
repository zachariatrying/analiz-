    def detect_flag_pattern(self, df, timeframe="Günlük"):
        """
        Detects Bull Flag / Pennant (Boğa Flaması/Bayrağı).
        Structure:
        1. Pole (Direk): Sharp Impulse Move (>15% in <15 bars).
        2. Flag (Bayrak): Consolidation in upper 30-50% of Pole. Volume drops.
        3. Breakout: Continuation.
        """
        patterns = []
        if df is None or len(df) < 20: return patterns
        
        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        vol = df['Volume'].values if 'Volume' in df.columns else None
        dates = df['Date'].values
        
        # Scan backwards for the "Pole Top"
        # We look for a local high that was the climax of an impulse
        # Look at last 30 bars
        
        # Simple scan: Find max high in last 5-20 bars
        curr_idx = len(df)-1
        lookback = 30
        
        # Find highest point in recent history (potential Pole Top)
        window = close[-lookback:]
        pole_top_idx = np.argmax(window) + (len(df) - lookback)
        pole_top_val = close[pole_top_idx]
        
        # If Pole Top is too old (more than 15 bars ago), pattern is stale
        dist_from_now = curr_idx - pole_top_idx
        if dist_from_now > 15: return patterns
        
        # 1. FIND THE POLE (Impulse)
        # Search backwards from Pole Top for the start of the move
        pole_start_idx = -1
        pole_start_val = 0
        
        # We look for a low point such that the move is fast
        # Limit pole search to 15 bars before Pole Top
        pole_limit = max(0, pole_top_idx - 15)
        
        min_val = pole_top_val
        for i in range(pole_top_idx, pole_limit, -1):
            if close[i] < min_val:
                min_val = close[i]
                pole_start_idx = i
                
        if pole_start_idx == -1: return patterns
        
        pole_start_val = min_val
        
        # Pole Validation
        pole_height = pole_top_val - pole_start_val
        pole_pct = pole_height / pole_start_val
        pole_duration = pole_top_idx - pole_start_idx
        
        # Rule: Move > 10% (relaxed slightly from 15 for sensitivity)
        if pole_pct < 0.10: return patterns
        if pole_duration < 3: return patterns # Too fast? flash crash recovery?
        
        # Momentum Check: Average candle size in Pole should be large?
        # Or simply time: < 15 bars for 10% move is strong.
        
        # 2. CHECK CONSOLIDATION (The Flag)
        # From Pole Top to Current
        # Price should strictly stay in the upper range (e.g. upper 50%)
        # Retracement Limit
        flag_lows = low[pole_top_idx:curr_idx+1]
        if len(flag_lows) < 2: return patterns # Need some consolidation
        
        min_flag_low = flag_lows.min()
        retracement = pole_top_val - min_flag_low
        
        # Elite Rule: Consolidation must stay in upper 50% (Max 0.5 Fib)
        if retracement > 0.5 * pole_height: return patterns 
        
        # 3. VOLUME CHECK (Breathing)
        vol_score = 50
        reason = ""
        if vol is not None:
            # Avg Vol during Pole
            v_pole = vol[pole_start_idx:pole_top_idx+1].mean()
            # Avg Vol during Flag
            v_flag = vol[pole_top_idx:curr_idx+1].mean()
            
            if v_flag < v_pole:
                vol_score += 25
                reason = "Hacim Daralması ✅"
            else:
                vol_score -= 10
        
        # 4. BREAKOUT & STATUS
        curr_price = close[-1]
        
        # Resistance can be simple (Pole Top) or a trendline on Highs
        # For Flag, Pole Top is horizontal resistance check, or slightly lower wedge
        resistance = df['High'].iloc[pole_top_idx:curr_idx].max()
        
        status = "unconfirmed"
        if curr_price > resistance:
            status = "confirmed"
            if vol is not None and vol[-1] > vol[-2]*1.2:
                 reason += " + Kırılım Hacimli"
                 vol_score += 10
                 
        start_price = pole_start_val
        target = start_price + pole_height # Flag Target = Pole Height added to breakout? 
        # Usually Target = Breakout + Pole Height
        target = resistance + pole_height
        stop = min_flag_low
        
        quality_score = vol_score + (pole_pct * 100) # Bonus for big poles
        if status == "unconfirmed":
            quality_score -= 10
            
        q_text = "Normal"
        if quality_score > 80: q_text = "Yıldızlı ⭐"
        
        strategy = self.get_strategy_text(status, curr_price, resistance, target, stop, "Flama/Bayrak")
        
        vade = f"{pole_duration}-{pole_duration*2} Mum"
        if "gün" in timeframe.lower() or timeframe=="G": vade = f"{pole_duration*0.5}-{pole_duration} Hafta"

        patterns.append({
            'name': f'Flama/Bayrak ({status.upper()})',
            'signal': 'Bullish',
            'desc': f"Direk: %{pole_pct*100:.1f}. {reason}",
            'points': [int(pole_start_idx), int(pole_top_idx), int(curr_idx)],
            'target': float(target),
            'stop': float(stop),
            'neckline': float(resistance),
            'status': status,
            'quality': q_text,
            'strategy': strategy,
            'type': 'flag',
            'score': quality_score,
             'date_range': f"{pd.to_datetime(dates[pole_start_idx]).strftime('%d.%m')}-{pd.to_datetime(dates[curr_idx]).strftime('%d.%m')}",
            'vade': vade
        })
        
        return patterns
