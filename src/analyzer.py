import pandas as pd
import numpy as np
import scipy.signal as signal
from scipy.stats import linregress
import traceback

class Analyzer:
    def __init__(self):
        # ----------------------------------------------------------------
        # ALGORITMA VE FORMASYON AYARLARI
        # ----------------------------------------------------------------
        self.config = {
            # TOBO
            'tobo_window': 5,         
            'tobo_tolerance': 0.15,   
            'tobo_min_depth': 0.015,   # NEW: Bas derinligi (Relaxed default)
            'tobo_min_bars': 3,       # NEW: Omuzlarda ve bas yapisinda minimum mum sayisi (Relaxed default)
            
            # FLAMA
            'flag_pole_min': 0.15,    
            'flag_consolidation': 0.10, 
            
            # CANAK
            'cup_min_depth': 0.10,    
            'handle_max_drop': 0.10, 
            
            # KIRILIM
            'trend_lookback_min': 30,  # NEW
            'trend_lookback_max': 180, 
            'breakout_margin': 0.02,
            
            # TOGGLES (Varsayilan Hepsi Acik)
            'enabled_patterns': {
                'tobo': True,
                'flag': True,
                'cup': True,
                'breakout': True
            }
        }

    def resample_data(self, df, timeframe):
        """
        Resamples dataframe to Hourly ('60min'), Weekly ('W') or Monthly ('M').
        Returns original if timeframe is 'G' or 'D'.
        """
        if df is None or df.empty: return df
        if timeframe in ['G', 'D', 'Günlük', 'Gunluk']: return df
        
        # Mapping
        if timeframe in ['S', 'Saatlik']:
            rule = '60min'
        elif timeframe in ['H', 'W', 'Haftalık', 'Haftalik']:
            rule = 'W'
        elif timeframe in ['A', 'M', 'Aylık', 'Aylik']:
            rule = 'M'
        else:
            return df
        
        # Ensure Date is index
        df = df.copy()
        df.set_index('Date', inplace=True)
        
        agg_dict = {
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }
        
        df_res = df.resample(rule).agg(agg_dict).dropna()
        df_res.reset_index(inplace=True)
        return df_res

    def calculate_trendlines(self, df):
        """
        Calculates Trendlines and Support/Resistance levels.
        Returns a dict with coordinates for plotting.
        """
        if df is None or len(df) < 30: return {}
        
        trends = {'uptrend': [], 'downtrend': [], 'support': [], 'resistance': []}
        close = df['Close'].values
        dates = df['Date'].values
        
        # 1. Horizontal Support/Resistance (Peaks/Troughs)
        # We look for price levels that have multiple touches
        # Simplified: Just find major Max/Min in recent history
        max_idx, min_idx = self.find_peaks(df, window=10)
        
        # Resistance (Top 2 peaks)
        if len(max_idx) > 0:
            recent_peaks = sorted([(close[i], i) for i in max_idx[-3:]], key=lambda x: x[0], reverse=True)
            for p, i in recent_peaks[:2]:
                trends['resistance'].append({'price': p, 'date': dates[i]})
                
        # Support (Bottom 2 troughs)
        if len(min_idx) > 0:
            recent_troughs = sorted([(close[i], i) for i in min_idx[-3:]], key=lambda x: x[0])
            for p, i in recent_troughs[:2]:
                trends['support'].append({'price': p, 'date': dates[i]})

        # 2. Uptrend (BLUE) - Connect Higher Lows
        # Need at least 2 lows, where low2 > low1
        if len(min_idx) >= 2:
            # Check last 2 major lows
            l1_idx = min_idx[-2]
            l2_idx = min_idx[-1]
            if close[l2_idx] > close[l1_idx]:
                 trends['uptrend'] = [
                     {'date': dates[l1_idx], 'price': close[l1_idx]},
                     {'date': dates[l2_idx], 'price': close[l2_idx]},
                     # Extend to current
                     {'date': dates[-1], 'price': close[l1_idx] + (close[l2_idx]-close[l1_idx])/(l2_idx-l1_idx) * (len(df)-1 - l1_idx)}
                 ]

        # 3. Downtrend (ORANGE) - Connect Lower Highs
        if len(max_idx) >= 2:
            h1_idx = max_idx[-2]
            h2_idx = max_idx[-1]
            if close[h2_idx] < close[h1_idx]:
                 trends['downtrend'] = [
                     {'date': dates[h1_idx], 'price': close[h1_idx]},
                     {'date': dates[h2_idx], 'price': close[h2_idx]},
                     # Extend
                     {'date': dates[-1], 'price': close[h1_idx] + (close[h2_idx]-close[h1_idx])/(h2_idx-h1_idx) * (len(df)-1 - h1_idx)}
                 ]
                 
        return trends

    def find_peaks(self, df, window=5):
        """Finds local maxima and minima."""
        if df is None: return [], []
        close = df['Close'].values
        max_idx = signal.argrelextrema(close, np.greater, order=window)[0]
        min_idx = signal.argrelextrema(close, np.less, order=window)[0]
        return max_idx, min_idx

    def calculate_zigzag(self, df, deviation=0.03):
        """
        Calculates ZigZag points based on percentage deviation.
        Returns a list of dicts: {'idx': i, 'price': p, 'type': 'high'|'low', 'date': d}
        """
        if df is None or len(df) < 10: return []
        
        # We need Highs and Lows
        highs = df['High'].values
        lows = df['Low'].values
        dates = df['Date'].values
        
        zz_points = []
        
        # Intialize
        trend = None # 1 for up, -1 for down
        last_high_idx = 0
        last_low_idx = 0
        last_high = highs[0]
        last_low = lows[0]
        
        # Simple ZigZag Logic
        for i in range(1, len(df)):
            curr_high = highs[i]
            curr_low = lows[i]
            
            if trend is None:
                if curr_high > last_high * (1 + deviation):
                    trend = 1
                    zz_points.append({'idx': last_low_idx, 'price': last_low, 'type': 'low'})
                    last_high_idx = i
                    last_high = curr_high
                elif curr_low < last_low * (1 - deviation):
                    trend = -1
                    zz_points.append({'idx': last_high_idx, 'price': last_high, 'type': 'high'})
                    last_low_idx = i
                    last_low = curr_low
            elif trend == 1: # Uptrend
                if curr_high > last_high:
                    last_high = curr_high
                    last_high_idx = i
                elif curr_low < last_high * (1 - deviation):
                    # Reversal to Down
                    zz_points.append({'idx': last_high_idx, 'price': last_high, 'type': 'high'})
                    trend = -1
                    last_low = curr_low
                    last_low_idx = i
            elif trend == -1: # Downtrend
                if curr_low < last_low:
                    last_low = curr_low
                    last_low_idx = i
                elif curr_high > last_low * (1 + deviation):
                    # Reversal to Up
                    zz_points.append({'idx': last_low_idx, 'price': last_low, 'type': 'low'})
                    trend = 1
                    last_high = curr_high
                    last_high_idx = i
                    
        # Add the last pending point (optional, but good for current state)
        if trend == 1:
             zz_points.append({'idx': last_high_idx, 'price': last_high, 'type': 'high'})
        elif trend == -1:
             zz_points.append({'idx': last_low_idx, 'price': last_low, 'type': 'low'})
             
        return zz_points

    def get_strategy_text(self, status, price, entry, target, stop, pattern_type=""):
        """
        Generates dynamic strategy advice based on current price action.
        """
        advice = ""
        
        # 0. Stop Hit?
        if price < stop:
            return f"❌ STOP PATLADI. Fiyat stop seviyesinin altında ({stop:.2f}). Formasyon geçersiz."
            
        # 1. Target Hit?
        if price >= target:
            return f"✅ HEDEF GÖRÜLDÜ. Fiyat hedef seviyesine ulaştı ({target:.2f}). Kar satışı değerlendirilebilir."

        # 2. Status Logic
        if status == "unconfirmed":
            dist = (entry - price) / price
            if 0 < dist < 0.03:
                advice = f"🚨 KIRILIM YAKIN. {entry:.2f} üzeri kapanış beklenmeli. Yakın takip."
            else:
                advice = f"⏳ OLUŞUYOR. {entry:.2f} seviyesinin kırılması bekleniyor."
                
        elif status == "confirmed":
            # Check for retest
            dist_retest = abs(price - entry) / entry
            
            if dist_retest < 0.03:
                advice = f"🛒 ALIM FIRSATI (Retest). Fiyat kırılım seviyesine ({entry:.2f}) yakın. Stop: {stop:.2f}"
            else:
                # In Profit?
                if price > entry:
                    gain = (price - entry) / entry
                    advice = f"📈 KARDA. Mevcut Getiri: %{gain*100:.1f}. Hedef: {target:.2f}. Stop yükseltilebilir."
                else:
                    return f"⚠️ RİSKLİ. Onaylanmış ama fiyat girişin altında. {entry:.2f} üzerine atamazsa stop olunmalı."
         
        return advice

    def calculate_trend_slope(self, values):
        """Calculates Linear Regression Slope of a series."""
        if len(values) < 2: return 0.0
        try:
            x = np.arange(len(values))
            slope, _, _, _, _ = linregress(x, values)
            mean_val = np.mean(values)
            if mean_val == 0: return 0.0
            return slope / mean_val
        except (ValueError, RuntimeWarning, Exception):
            return 0.0

    def calculate_linear_regression_channel(self, df, length=None):
        """
        Calculates Linear Regression Channel (Fair Value) and Standard Deviation Bands.
        Returns dictionary with arrays for upper, lower, and middle lines.
        """
        if df is None or len(df) < 2: return {}
        
        close = df['Close'].values
        n = len(close)
        if length is None: length = n
        
        # We calculate regression over the entire available data or specified length
        start_idx = max(0, n - length)
        y = close[start_idx:]
        x = np.arange(len(y))
        
        try:
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            
            # Regression Line (Fair Value)
            reg_line = slope * x + intercept
            
            # Standard Deviation
            std_dev = np.std(y - reg_line)
            
            upper_channel = reg_line + (2 * std_dev)
            lower_channel = reg_line - (2 * std_dev)
            
            # Extend to match original DF length if needed (filling start with NaNs or calc)
            # For simplicity in valid_range:
            full_reg = np.full(n, np.nan)
            full_upper = np.full(n, np.nan)
            full_lower = np.full(n, np.nan)
            
            full_reg[start_idx:] = reg_line
            full_upper[start_idx:] = upper_channel
            full_lower[start_idx:] = lower_channel
            
            return {
                'middle': full_reg,
                'upper': full_upper,
                'lower': full_lower,
                'slope': slope,
                'std': std_dev
            }
        except:
            return {}

    def detect_support_resistance(self, df, window=10):
        """
        Detects Support and Resistance levels using local extrema.
        Returns lists of prices.
        """
        if df is None or len(df) < window: return {'supports': [], 'resistances': []}
        
        # Highs for Resistance, Lows for Support
        highs = df['High'].values
        lows = df['Low'].values
        
        # Maxima
        max_idx = signal.argrelextrema(highs, np.greater, order=window)[0]
        min_idx = signal.argrelextrema(lows, np.less, order=window)[0]
        
        resistances = [highs[i] for i in max_idx]
        supports = [lows[i] for i in min_idx]
        
        # Optional: Filter close levels or just return raw significant ones
        # For visualization, we might want only the most recent/relevant ones.
        return {
            'supports': sorted(supports)[-5:],     # Return top 5 potential supports (closest to price maybe?)
            'resistances': sorted(resistances)[-5:] # Return top 5
        }

    def detect_high_tight_flag(self, df):
        """
        Detects High Tight Flag (Rocket Pattern).
        Criteria:
        1. >90% gain in <40 bars (Pole).
        2. Consolidation < 20% pullback.
        3. Tight consolidation duration.
        """
        if df is None or len(df) < 50: return []
        
        patterns = []
        close = df['Close'].values
        
        # Look for massive run-up
        # Iterate backwards to find recent formation
        curr_price = close[-1]
        
        # Check last 15-25 bars for consolidation
        lookback_consolidation = 20
        consolidation_slice = close[-lookback_consolidation:]
        max_cons = consolidation_slice.max()
        min_cons = consolidation_slice.min()
        
        # 1. Tightness Check (<20% drop from peak of consolidation)
        drop_pct = (max_cons - min_cons) / max_cons
        if drop_pct > 0.25: return [] # Too loose
        
        # 2. Pole Check (The Rocket)
        # Look back 40-60 bars from the START of consolidation
        pole_end_idx = len(close) - lookback_consolidation
        pole_start_search = max(0, pole_end_idx - 60)
        
        pole_slice = close[pole_start_search:pole_end_idx]
        if len(pole_slice) < 10: return []
        
        pole_min = pole_slice.min()
        pole_max = pole_slice.max() # Should be close to max_cons
        
        # Ensure the run-up is huge (>90% or user configurable, maybe 50% for BIST is enough?)
        # Standard HTF is 100% in 8 weeks. Let's use 50% for BIST as "Rocket".
        run_up = (pole_max - pole_min) / pole_min
        
        if run_up > 0.50:
            # Check duration of run-up (fast move)
            # Logic: If 50% gain happened in short time.
            
            # Simple Output
            target = curr_price * 1.5 # 50% more?
            patterns.append({
                'name': 'High Tight Flag (Roket 🚀)',
                'signal': 'Bullish',
                'desc': f"Güçlü Yükseliş: %{run_up*100:.0f}. Dar Konsolidasyon: %{drop_pct*100:.1f}",
                'score': 95,
                'target': max_cons + (max_cons - pole_min), # Measured move
                'stop': min_cons * 0.95,
                'status': 'unconfirmed' if curr_price < max_cons else 'confirmed',
                'prices': [],
                'points': [], # No specific points needed for simple signal
                'type': 'rocket'
            })
            
        return patterns

    def detect_classic_patterns(self, df, timeframe="Günlük"):
        """Wrapper to detect all classic patterns with config."""
        # Clean Wrapper
        if df is None or df.empty: return []
        
        zz_points = self.calculate_zigzag(df, deviation=self.config.get('zigzag_deviation', 0.04))
        
        all_patterns = []
        
        # Checks
        if self.config['enabled_patterns']['tobo']:
            all_patterns.extend(self.detect_tobo_zigzag(df, zz_points, timeframe))
            all_patterns.extend(self.detect_obo_pattern(df, timeframe))
            
        if self.config['enabled_patterns']['cup']:
             all_patterns.extend(self.detect_cup_zigzag(df, zz_points, timeframe))
             
        # Add Rocket
        all_patterns.extend(self.detect_high_tight_flag(df))
             
        return all_patterns

    def validate_volume_profile(self, df, p1_idx, p3_idx, p5_idx):
        """
        Validates Volume Profile for TOBO:
        1. High volume at Left Shoulder (Panic selling)
        2. Lower volume at Head (Absorption) - Optional but good
        3. Low volume at Right Shoulder (No supply)
        Returns: (Score 0-100, Reason)
        """
        if 'Volume' not in df.columns: return 50, "Volume data missing"
        
        try:
            # Ranges (approx +/- 2 bars around points)
            v_ls = df['Volume'].iloc[max(0, p1_idx-1):p1_idx+2].mean()
            v_head = df['Volume'].iloc[max(0, p3_idx-1):p3_idx+2].mean()
            v_rs = df['Volume'].iloc[max(0, p5_idx-1):p5_idx+2].mean()
            
            score = 50
            reasons = []
            
            # 1. Head Volume < LS Volume (Drying up)
            if v_head < v_ls:
                score += 25
                reasons.append("Hacim Başta düştü")
            else:
                score -= 10
                
            # 2. RS Volume < LS Volume (Supply exhausted)
            if v_rs < v_ls:
                score += 25
                reasons.append("Sağ Omuz hacimsiz")
                
            return score, ", ".join(reasons)
        except:
            return 50, "Volume calc error"

    def detect_tobo_zigzag(self, df, zz_points, timeframe="Günlük"):
        """
        TOBO (Inverse Head & Shoulders) - ELITE VERSION
        Includes: Pre-Trend Check, Absolute Geometry, Volume Profile, Smart Scoring.
        """
        patterns = []
        if len(zz_points) < 5: return patterns
        
        cfg = self.config
        close = df['Close'].values
        lows = df['Low'].values 
        highs = df['High'].values
        dates = df['Date'].values
        
        # Iterate backwards
        for i in range(len(zz_points)-1, 4, -1):
            p5 = zz_points[i]   # RS Low
            p4 = zz_points[i-1] # Neck 2
            p3 = zz_points[i-2] # Head Low
            p2 = zz_points[i-3] # Neck 1
            p1 = zz_points[i-4] # LS Low
            
            # 1. Basic Type Check
            if not (p5['type'] == 'low' and p4['type'] == 'high' and 
                    p3['type'] == 'low' and p2['type'] == 'high' and 
                    p1['type'] == 'low'):
                # print("Type mismatch")
                continue
            
            # --- PHASE 0.5: MATURITY (Duration) ---
            # Every leg (p1-p2, p2-p3, p3-p4, p4-p5) must have enough candles
            # Elite Requirement: Minimum bars per swing to avoid "noise"
            min_bars = cfg.get('tobo_min_bars', 3)
            leg1 = p2['idx'] - p1['idx']
            leg2 = p3['idx'] - p2['idx']
            leg3 = p4['idx'] - p3['idx']
            leg4 = p5['idx'] - p4['idx']
            
            if any(leg < min_bars for leg in [leg1, leg2, leg3, leg4]):
                continue
            
            # Levels
            ls_val, n1_val, h_val, n2_val, rs_val = p1['price'], p2['price'], p3['price'], p4['price'], p5['price']
            
            # --- PHASE 1: GEOMETRY (The Structure) ---
            
            # A. Head must be strictly and significantly lower than both shoulders
            # Elite Rule: Head should be at least X% lower than the lower of the two shoulders
            shoulder_min = min(ls_val, rs_val)
            head_depth_pct = (shoulder_min - h_val) / shoulder_min
            
            # Use Configured Depth instead of hardcoded 0.015
            min_depth_cfg = cfg.get('tobo_min_depth', 0.015)
            if head_depth_pct < min_depth_cfg: continue 
            
            # B. Absolute Minimum Check (Strict)
            # The Head must be the absolute lowest point (including wicks) in the entire range.
            start_idx = min(p1['idx'], p5['idx'])
            end_idx = max(p1['idx'], p5['idx'])
            min_in_range = lows[start_idx:end_idx+1].min()
            
            # Allow zero tolerance except for the head index itself
            if min_in_range < h_val: 
                continue 

            # C. Symmetry & Neckline
            neck_diff = abs(n1_val - n2_val) / max(n1_val, n2_val)
            if neck_diff > 0.07: continue
            
            shoulder_diff = abs(ls_val - rs_val) / max(ls_val, rs_val)
            # Use Config tolerance
            if shoulder_diff > cfg.get('tobo_tolerance', 0.20): continue
            
            # --- PHASE 2: PRE-TREND (The Setup) ---
            # TOBO is a Reversal. It MUST come after a downtrend.
            # We should check trend ending at the START of the pattern (the High before LS).
            # LS is p1 (Low). We need p0 (High).
            trend_end_idx = p1['idx']
            if i-5 >= 0:
                p0 = zz_points[i-5]
                if p0['type'] == 'high':
                     trend_end_idx = p0['idx']
            
            pattern_width = p5['idx'] - p1['idx']
            lookback = int(pattern_width * 1.5) # Look further back
            trend_start = max(0, trend_end_idx - lookback)
            
            # Edge Case: Not enough data before pattern start (p0)
            # Fallback: Check the slope of the setup leg (p0 -> p1)
            # If p0 is high and p1 is low, this will be negative (valid).
            if trend_end_idx - trend_start < 5: 
                trend_start = trend_end_idx
                trend_end_idx = p1['idx']
                
            if trend_end_idx - trend_start < 5: continue 
            
            pre_trend_prices = close[trend_start:trend_end_idx]
            slope = self.calculate_trend_slope(pre_trend_prices)
            
            # Slope must be negative (Downtrend)
            if slope > 0:
                 # Fail: Rising trend before pattern
                 continue
                 
            # --- PHASE 3: CONFIRMATION (The Trigger) ---
            # Elite Update: Use Slanted Neckline (Trendline between P2 and P4) instead of Horizontal
            # Math: Line passing through (idx2, p2) and (idx4, p4)
            # y = mx + c
            
            x1, y1 = p2['idx'], p2['price']
            x2, y2 = p4['idx'], p4['price']
            
            if x2 <= x1: continue # Safety: P4 must be after P2
            
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            
            # Calculate Neckline value at Current Price (Last Bar)
            curr_idx = len(close) - 1
            neckline_at_curr = (slope * curr_idx) + intercept
            
            # Also calculate neckline value at the breakout point (roughly)
            # For target calculation, we can use the head depth relative to the slanted line at Head Index
            neckline_at_head = (slope * p3['idx']) + intercept
            depth = abs(neckline_at_head - h_val)
            
            curr_price = close[-1]
            status = "unconfirmed"
            
            # Breakout Check: Price > Slanted Neckline
            if curr_price > neckline_at_curr:
                status = "confirmed"
            
            # Determine Quality Score
            quality_score = 50 # Start base
            
            # 1. Trend Slope of Neckline
            # Ideally slightly rising or flat is better for TOBO? 
            # Actually, standard TOBO has slightly down-sloping neckline (easier break), 
            # but up-sloping implies stronger bulls. Let's not penalize much.
            if slope < 0: quality_score += 5 # Down-sloping is traditional easier entry
            
            # 2. Volume Score
            vol_score, vol_reason = self.validate_volume_profile(df, p1['idx'], p3['idx'], p5['idx'])
            quality_score += (vol_score - 50) # Add delta
            
            # 3. Fibonacci Check (RS Depth)
            rs_depth = neckline_at_curr - rs_val # Approx depth at RS
            rs_retracement = (rs_val - h_val) / depth
            if rs_retracement > 0.236: 
                quality_score += 10
            else:
                quality_score -= 10 
                
            # 4. Breakout Quality
            if status == "confirmed":
                try:
                    # Check if volume spiked recently
                    if df['Volume'].iloc[-1] > df['Vol_SMA_20'].iloc[-1] * 1.5:
                         quality_score += 15
                         vol_reason += ", Kırılım Hacimli 💥"
                except: pass

            # Filter Weak Patterns
            if quality_score < 40: continue

            # --- OUTPUT GENERATION ---
            target = neckline_at_curr + depth
            # Stop is slightly below RS Low
            stop = rs_val * 0.99
            
            quality_text = "Normal"
            if quality_score > 75: quality_text = "Yıldızlı ⭐ (Elite)"
            elif quality_score > 60: quality_text = "Güçlü"
            elif quality_score < 45: quality_text = "Zayıf"

            # Dynamic Strategy
            strategy = self.get_strategy_text(status, curr_price, neckline_at_curr, target, stop, "TOBO")
            if status == "confirmed":
                dist_pct = (curr_price - neckline_at_curr) / neckline_at_curr
                if dist_pct > 0.15: continue # Too late
                
            # Time Estimate
            width = p5['idx'] - p1['idx']
            vade = self.calculate_smart_vade(int(width*0.8), int(width*1.5), timeframe)
            
            patterns.append({
                'name': f'TOBO ({status.upper()})',
                'signal': 'Bullish',
                'desc': f"Skor: {quality_score}/100. {vol_reason}. Boyun: {neckline_at_curr:.2f} (Eğimli)",
                'points': [int(p1['idx']), int(p2['idx']), int(p3['idx']), int(p4['idx']), int(p5['idx'])],
                'prices': [float(p1['price']), float(p2['price']), float(p3['price']), float(p4['price']), float(p5['price'])],
                'neckline': float(neckline_at_curr), # Store Current level
                'neckline_slope': float(slope),      # Store slope for drawing
                'neckline_intercept': float(intercept), # Store intercept
                'target': float(target),
                'stop': float(stop),
                'status': status,
                'quality': quality_text,
                'strategy': strategy,
                'type': 'tobo',
                'score': quality_score,
                'date_range': f"{pd.to_datetime(dates[p1['idx']]).strftime('%d.%m')}-{pd.to_datetime(dates[p5['idx']]).strftime('%d.%m')}",
                'vade': vade,
                
                # --- ÇİZİM MOTORU İÇİN KOORDİNATLAR (TOBO) ---
                "Points": {
                    "p_start_idx": int(p1['idx']),  # Sol Omuz
                    "p_start_val": float(p1['price']),
                    "p_end_idx": int(p5['idx']),    # Sağ Omuz
                    "p_end_val": float(p5['price']),
                    "f_end_idx": int(len(close)-1),
                    # Neckline & Head
                    "head_idx": int(p3['idx']),
                    "head_val": float(p3['price']),
                    "neck_slope": float(slope),
                    "neck_intercept": float(intercept),
                    # Drawing lines
                    "res_start": float((slope * p1['idx']) + intercept), # Neckline at start
                    "res_end":   float(neckline_at_curr),                # Neckline at end
                     # Dummy values to prevent errors in generic parser
                     "sup_start": float(p3['price']),
                     "sup_end": float(p3['price']) 
                },
                "Formasyon": "TOBO",
                "Symbol": "N/A"
            })
            
            break # Only most recent

        return patterns

    def detect_obo_pattern(self, df, timeframe="Günlük"):
        """
        Detects OBO (Head and Shoulders) - BEARISH Reversal.
        Structure: Peak (LS) -> Trough (N1) -> Higher Peak (Head) -> Trough (N2) -> Lower Peak (RS)
        """
        zz_points = self.calculate_zigzag(df)
        patterns = []
        if len(zz_points) < 5: return patterns
        
        cfg = self.config
        close = df['Close'].values
        highs = df['High'].values
        dates = df['Date'].values
        
        # Iterate backwards
        for i in range(len(zz_points)-1, 4, -1):
            p5 = zz_points[i]   # RS High
            p4 = zz_points[i-1] # Neck 2 (Low)
            p3 = zz_points[i-2] # Head High
            p2 = zz_points[i-3] # Neck 1 (Low)
            p1 = zz_points[i-4] # LS High
            
            # 1. Basic Type Check (Inverted vs TOBO)
            if not (p5['type'] == 'high' and p4['type'] == 'low' and 
                    p3['type'] == 'high' and p2['type'] == 'low' and 
                    p1['type'] == 'high'):
                continue
            
            # Duration Check
            min_bars = cfg.get('tobo_min_bars', 3)
            leg1 = p2['idx'] - p1['idx']
            leg2 = p3['idx'] - p2['idx']
            leg3 = p4['idx'] - p3['idx']
            leg4 = p5['idx'] - p4['idx']
            
            if any(leg < min_bars for leg in [leg1, leg2, leg3, leg4]):
                continue
            
            # Levels
            ls_val, n1_val, h_val, n2_val, rs_val = p1['price'], p2['price'], p3['price'], p4['price'], p5['price']
            
            # --- PHASE 1: GEOMETRY ---
            
            # A. Head must be HIGHER than both shoulders
            shoulder_max = max(ls_val, rs_val)
            # Head must be distinctly higher (e.g. 1%)
            if h_val <= shoulder_max * 1.01: continue 

            # B. Absolute Maximum Check
            # Head must be the highest point in the pattern range
            start_idx = min(p1['idx'], p5['idx'])
            end_idx = max(p1['idx'], p5['idx'])
            max_in_range = highs[start_idx:end_idx+1].max()
            
            if max_in_range > h_val: continue
            
            # C. Symmetry & Neckline Flatness
            # Neckline points (Lows) shouldn't be too far apart
            neck_diff = abs(n1_val - n2_val) / min(n1_val, n2_val)
            if neck_diff > 0.15: continue # Relaxed for OBO
            
            shoulder_diff = abs(ls_val - rs_val) / min(ls_val, rs_val)
            if shoulder_diff > cfg.get('tobo_tolerance', 0.20): continue
            
            # --- PHASE 2: PRE-TREND (Must be UPTREND) ---
            trend_end_idx = p1['idx']
            if i-5 >= 0:
                p0 = zz_points[i-5]
                # Look for Low before LS High
                if p0['type'] == 'low': trend_end_idx = p0['idx']
            
            lookback = int((p5['idx'] - p1['idx']) * 1.5)
            trend_start = max(0, trend_end_idx - lookback)
            
            if trend_end_idx - trend_start < 5: 
                trend_start = trend_end_idx
                trend_end_idx = p1['idx']
            
            if trend_end_idx - trend_start < 5: continue
            
            pre_trend_prices = close[trend_start:trend_end_idx]
            slope = self.calculate_trend_slope(pre_trend_prices)
            
            # Must be Uptrend (Positive Slope)
            if slope < 0.0005: continue 
            
            # --- PHASE 3: CONFIRMATION (Slanted Neckline) ---
            # Line through Neck1 (p2) and Neck2 (p4) -> Lows
            x1, y1 = p2['idx'], p2['price']
            x2, y2 = p4['idx'], p4['price']
            
            if x2 == x1: continue
            
            neck_slope = (y2 - y1) / (x2 - x1)
            neck_intercept = y1 - (neck_slope * x1)
            
            curr_idx = len(close) - 1
            neckline_at_curr = (neck_slope * curr_idx) + neck_intercept
            
            neckline_at_head = (neck_slope * p3['idx']) + neck_intercept
            depth = abs(h_val - neckline_at_head)
            
            curr_price = close[-1]
            status = "unconfirmed"
            
            # Breakout: Price < Neckline
            if curr_price < neckline_at_curr:
                status = "confirmed"
                
            # Scoring
            quality_score = 50
            
            # Downtrending shoulder (RS < LS)
            if rs_val < ls_val: quality_score += 10
            
            # Volume Logic: Should decrease on RS rally
            try:
                vol_rs = df['Volume'].iloc[p4['idx']:p5['idx']].mean()
                vol_head = df['Volume'].iloc[p2['idx']:p3['idx']].mean()
                if vol_rs < vol_head: quality_score += 10
            except: pass
            
            # Validating Neckline Slope: Rising neckline (slope > 0) is standard for topping OBO
            if neck_slope > 0: quality_score += 5

            if status == "confirmed":
                # Check breakdown volume
                 if df['Volume'].iloc[-1] > df['Vol_SMA_20'].iloc[-1]:
                     quality_score += 10
                     
            if quality_score < 40: continue
            
            # Targets (Downside)
            target = neckline_at_curr - depth
            stop = rs_val * 1.01 # Stop above RS
            
            # Strategy Text
            strategy = f"OBO (Düşüş): {neckline_at_curr:.2f} altı kapanışta hedef {target:.2f}. Stop: {stop:.2f}"
            
            width = p5['idx'] - p1['idx']
            vade = self.calculate_smart_vade(int(width*0.8), int(width*1.5), timeframe)
            
            patterns.append({
                'name': f'OBO ({status.upper()})',
                'signal': 'Bearish',
                'desc': f"Skor: {quality_score}/100. Ayı Formasyonu 🐻. Boyun: {neckline_at_curr:.2f}",
                'points': [int(p1['idx']), int(p2['idx']), int(p3['idx']), int(p4['idx']), int(p5['idx'])],
                'prices': [float(p1['price']), float(p2['price']), float(p3['price']), float(p4['price']), float(p5['price'])],
                'neckline': float(neckline_at_curr),
                'neckline_slope': float(neck_slope),
                'neckline_intercept': float(neck_intercept),
                'target': float(target),
                'stop': float(stop),
                'status': status,
                'quality': "Normal",
                'strategy': strategy,
                'type': 'obo',
                'score': quality_score,
                'date_range': f"{pd.to_datetime(dates[p1['idx']]).strftime('%d.%m')}-{pd.to_datetime(dates[p5['idx']]).strftime('%d.%m')}",
                'vade': vade,
                
                # --- ÇİZİM MOTORU İÇİN KOORDİNATLAR (OBO) ---
                "Points": {
                    "p_start_idx": int(p1['idx']),  # Sol Omuz
                    "p_start_val": float(p1['price']),
                    "p_end_idx": int(p5['idx']),    # Sağ Omuz
                    "p_end_val": float(p5['price']),
                    "head_idx": int(p3['idx']),
                    "head_val": float(p3['price']),
                    "neck_slope": float(neck_slope),
                    "neck_intercept": float(neck_intercept),
                    "f_end_idx": int(len(close)-1),
                    "res_start": float((neck_slope * p1['idx']) + neck_intercept),
                    "res_end":   float(neckline_at_curr)
                },
                "Formasyon": "OBO",
                "Symbol": "N/A"
            })
            
            break # Return best/latest 
            
        return patterns

    def detect_cup_zigzag(self, df, zz_points, timeframe="Günlük"):
        """Detects Cup and Handle using Elite standards (Rounded Bottom, Handle Slope)."""
        patterns = []
        if len(zz_points) < 5: return patterns
        cfg = self.config
        close = df['Close'].values
        dates = df['Date'].values
        
        # Iterate looking for the Handle first (P3 Low, P2 High before it)
        # P2=Right Lip, P3=Handle Low. P1=Left Lip.
        for i in range(len(zz_points)-1, 2, -1):
            p3 = zz_points[i]   # Handle Low (or Handle End)
            p2 = zz_points[i-1] # Right Lip
            
            # P3 must be a Low (Handle Pullback)
            if p3['type'] != 'low': continue
            
            # Handle Validation 1: Slope & Level
            # The Handle Low (P3) must be lower than the Right Lip (P2).
            if p3['price'] >= p2['price']: continue 
            
            handle_slice = close[p2['idx']:p3['idx']+1]
            if len(handle_slice) > 3:
                h_slope = self.calculate_trend_slope(handle_slice)
                if h_slope > 0.0: continue # Reject upward drift even if lower
                
            # Search for Left Lip (P1)
            best_p1 = None
            cup_bottom_val = float('inf')
            
            scan_limit = max(0, i-20)
            for j in range(i-2, scan_limit, -1):
                pj = zz_points[j]
                if pj['type'] == 'low':
                    cup_bottom_val = min(cup_bottom_val, pj['price'])
                    
                if pj['type'] == 'high':
                    # Check Level Difference
                    diff = abs(pj['price'] - p2['price']) / p2['price']
                    if diff < 0.10: # 10% tolerance for lip alignment
                        best_p1 = pj
                        # Width Check
                        width = p2['idx'] - pj['idx']
                        if width > 30: # Minimum cup width
                            break
            
            if not best_p1: continue
            p1 = best_p1
            
            # --- GEOMETRY & SHAPE ---
            
            # 1. Depth Check
            min_cup_depth = cfg.get('cup_min_depth', 0.10)
            cup_depth = p2['price'] - cup_bottom_val
            pct_depth = cup_depth / p2['price']
            if pct_depth < min_cup_depth: continue
            
            # 2. Handle Retracement (Fibonacci)
            # Handle depth should not exceed 50% of Cup Depth
            handle_depth = p2['price'] - p3['price']
            if handle_depth > 0.5 * cup_depth: continue
            
            # 3. U-Shape Score (Symmetry/Roundness)
            # Check the middle third of the cup. It should be relatively flat (Accumulation).
            # Indices
            idx_start = p1['idx']
            idx_end = p2['idx']
            idx_len = idx_end - idx_start
            
            mid_start = idx_start + int(idx_len * 0.33)
            mid_end = idx_start + int(idx_len * 0.66)
            bottom_slice = close[mid_start:mid_end]
            
            # The bottom slice should not have prices higher than say 50% of depth?
            # Or simpler: Variance should be low?
            # Let's check if avg price of bottom is in lower half of cup.
            avg_bottom = bottom_slice.mean()
            mid_price_level = cup_bottom_val + (cup_depth * 0.5)
            
            u_shape_score = 50
            if avg_bottom < mid_price_level:
                u_shape_score += 20 # Good, bottom is deep/wide
            
            # 4. Breakout Check
            curr_price = df['Close'].iloc[-1]
            breakout_level = p2['price']
            status = "unconfirmed"
            
            is_breakout = curr_price > breakout_level
            
            # Volume Analysis
            vol_score = 50
            vol_reason = ""
            if 'Volume' in df.columns:
                 # High Vol at Breakout?
                 try:
                     if is_breakout and df['Volume'].iloc[-1] > df['Vol_SMA_20'].iloc[-1] * 1.5:
                         vol_score += 20
                         vol_reason = "Hacimli Kırılım"
                 except: pass

            quality_score = u_shape_score + (vol_score - 50) + 10 # Base goodness
            
            if status == "unconfirmed":
                dist = (breakout_level - curr_price) / curr_price
                if 0 < dist < 0.05:
                    status = "forming" # Close to breakout
                else:
                    if curr_price < p3['price']: continue # Broken handle low
                    
            if is_breakout: status = "confirmed"

            # Skip weak patterns
            if quality_score < 60: continue

            target = breakout_level + cup_depth
            stop = p3['price']
            
            q_text = "Normal"
            if quality_score > 80: q_text = "Yıldızlı ⭐"
            elif quality_score > 70: q_text = "Güçlü"

            strategy = self.get_strategy_text(status, curr_price, breakout_level, target, stop, "Fincan Kulp")
            
            # Vade
            vade = self.calculate_smart_vade(int(idx_len*0.4), int(idx_len*0.8), timeframe)

            patterns.append({
                'name': f'Fincan Kulp ({status.upper()})',
                'signal': 'Bullish',
                'desc': f"Derinlik: %{pct_depth*100:.1f}. Kulp: %{(handle_depth/cup_depth)*100:.0f} Retracement. {vol_reason}",
                'points': [p1['idx'], p2['idx'], p3['idx']],
                'prices': [float(p1['price']), float(p2['price']), float(p3['price'])],
                'target': target,
                'stop': stop,
                'neckline': breakout_level,
                'status': status,
                'quality': q_text,
                'strategy': strategy,
                'type': 'cup',
                'score': quality_score,
                'date_range': f"{pd.to_datetime(dates[p1['idx']]).strftime('%d.%m')}-{pd.to_datetime(dates[p3['idx']]).strftime('%d.%m')}",
                'vade': vade,
                
                # --- ÇİZİM MOTORU İÇİN KOORDİNATLAR (KULP) ---
                "Points": {
                    "p_start_idx": int(p1['idx']),  # Sol Dudak
                    "p_start_val": float(p1['price']),
                    "p_end_idx": int(p2['idx']),    # Sağ Dudak
                    "p_end_val": float(p2['price']),
                    "f_end_idx": int(p3['idx']),    # Kulp Dibi
                    # Resistance (Breakout Level)
                    "res_start": float(breakout_level),
                    "res_end":   float(breakout_level),
                    # Support (Bottom)
                     "sup_start": float(cup_bottom_val),
                     "sup_end": float(cup_bottom_val) 
                },
                "Formasyon": "Fincan Kulp",
                "Symbol": "N/A"
            })
            
            break # Return most recent
        return patterns

    def detect_flag_pattern(self, df, timeframe="Günlük"):
        """
        Detects Flama (Pennant) and Flag (Bayrak) patterns with Tuned filters.
        Includes Momentum (Speed) and Duration checks.
        """
        patterns = []
        if df is None or len(df) < 20: return patterns
        
        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        vol = df['Volume'].values if 'Volume' in df.columns else None
        dates = df['Date'].values
        
        curr_idx = len(df) - 1
        lookback = 60
        start_scan = max(0, curr_idx - lookback)
        
        # 1. Candidate Detection (Local Extrema)
        bull_peaks = signal.argrelextrema(high, np.greater, order=3)[0]
        bull_candidates = [p for p in bull_peaks if p >= start_scan and p < curr_idx - 2]
        
        bear_troughs = signal.argrelextrema(low, np.less, order=3)[0]
        bear_candidates = [p for p in bear_troughs if p >= start_scan and p < curr_idx - 2]
        
        all_candidates = [{'idx': p, 'type': 'bull'} for p in bull_candidates] + \
                         [{'idx': p, 'type': 'bear'} for p in bear_candidates]
        
        best_score = -1
        
        for cand in all_candidates:
            pole_end_idx = cand['idx'] 
            direction = cand['type']
            
            # Recency Check (Relaxed to 45 bars to catch slightly older setups)
            if (curr_idx - pole_end_idx) > 45: continue
            
            # --- POLE ANALYSIS ---
            search_limit = max(0, pole_end_idx - 35) # Look further back for base
            
            if direction == 'bull':
                pole_high = high[pole_end_idx]
                pole_base_idx = pole_end_idx
                pole_base = pole_high
                for k in range(pole_end_idx, search_limit, -1):
                     if low[k] < pole_base:
                         pole_base = low[k]
                         pole_base_idx = k
                pole_height = high[pole_end_idx] - pole_base
            else:
                pole_low = low[pole_end_idx]
                pole_base_idx = pole_end_idx
                pole_base = pole_low
                for k in range(pole_end_idx, search_limit, -1):
                     if high[k] > pole_base:
                         pole_base = high[k]
                         pole_base_idx = k
                pole_height = pole_base - pole_low
                
            if pole_base == 0: continue
            pole_height_pct = pole_height / pole_base
            pole_width = pole_end_idx - pole_base_idx
            
            # Basic Constraint
            
            # --- AYARLAR (BIST İçin Optimize Edildi) ---
            # Eskisi 0.012 idi, çok sıkıydı. 0.005'e çektik (Mum başı %0.5 hareket yeterli).
            MIN_MOMENTUM = 0.005  
            # Direk boyu en az %7 olsun (Eskisi %10 idi).
            MIN_POLE_HEIGHT = 0.05 # Config overridable, defaulting to user request or slightly lower for safety
            
            min_pole = self.config.get('flag_pole_min', MIN_POLE_HEIGHT) 
            if pole_height_pct < min_pole: continue
            
            # DYNAMIC WIDTH CONSTRAINT
            min_width = 3
            if "W" in timeframe or "Haftalık" in timeframe: min_width = 1 # Allow 1-bar poles in Weekly
            
            if pole_width < min_width: continue 
            
            # --- FILTER 1: MOMENTUM (SPEED) ---
            avg_bar_return = pole_height_pct / pole_width
            
            # Relaxed Momentum Check
            if avg_bar_return < MIN_MOMENTUM: continue 
            
            # --- CONSOLIDATION ANALYSIS ---
            flag_highs = high[pole_end_idx:curr_idx+1]
            flag_lows = low[pole_end_idx:curr_idx+1]
            flag_width = len(flag_highs)
            
            # --- FILTER 2: DURATION LIMIT ---
            min_flag_width = 3
            if "W" in timeframe or "Haftalık" in timeframe: min_flag_width = 2
            
            if flag_width < min_flag_width: continue
            if flag_width > 35: continue # Relaxed from 25 to capture longer consolidations
            if flag_width > (pole_width * 4.0): continue 
            
            # Retracement Check
            if direction == 'bull':
                curr_price = close[-1]
                retracement = high[pole_end_idx] - curr_price
                if curr_price > high[pole_end_idx] * 1.05: continue 
                is_htf = (pole_height_pct > 0.90) and (retracement / pole_height < 0.20) 
            else:
                curr_price = close[-1]
                retracement = curr_price - low[pole_end_idx]
                is_htf = False
                
            retracement_pct = retracement / pole_height
            if retracement_pct > 0.60: continue # Too deep
            
            # --- GEOMETRY ---
            x = np.arange(flag_width)
            if len(x) < 2: continue
            slope_res, int_res, _, _, _ = linregress(x, flag_highs)
            slope_sup, int_sup, _, _, _ = linregress(x, flag_lows)
            
            # Classify
            # Classify Flag vs Pennant (Geometry)
            # Flag = Parallel Channel (Slopes are similar)
            # Pennant = Converging Triangle (Slopes intersect in near future)
            
            is_pennant = False
            
            # Check convergence
            slope_diff = abs(slope_res - slope_sup)
            
            # 1. Parallel Check (Flag)
            # If slopes are very close, it's a channel
            if slope_diff < 0.01: 
                is_pennant = False
            else:
                # 2. Convergence Point Check
                # m1*x + c1 = m2*x + c2  =>  x = (c2 - c1) / (m1 - m2)
                try:
                    x_int = (int_sup - int_res) / (slope_res - slope_sup)
                    
                    # If intersection is in the future (relative to start of flag)
                    # And not too far away (e.g. within 3x flag width)
                    if x_int > flag_width and x_int < (flag_width * 5):
                        is_pennant = True
                    # Also handle traditional symmetric triangle case (already formed)
                    elif slope_res < 0 and slope_sup > 0:
                        is_pennant = True
                        
                except:
                    is_pennant = False # Parallel/Error
            
            pat_name = "Flama" if is_pennant else "Bayrak"
            full_name = f"Boğa {pat_name}" if direction == 'bull' else f"Ayı {pat_name}"
            if is_htf: full_name = "High Tight Flag 🚀"
            
            # --- BREAKOUT & SCORE ---
            breakout_level = 0
            neckline = 0
            status = "unconfirmed"
            
            if direction == 'bull':
                resistance = (slope_res * (flag_width-1)) + int_res
                breakout_level = resistance
                neckline = resistance
                if curr_price > resistance: status = "confirmed"
            else:
                support = (slope_sup * (flag_width-1)) + int_sup
                breakout_level = support
                neckline = support
                if curr_price < support: status = "confirmed"
            
            # Score
            score = 70
            if vol is not None:
                v_pole_avg = np.mean(vol[pole_base_idx:pole_end_idx])
                v_flag_avg = np.mean(vol[pole_end_idx:])
                if v_flag_avg < v_pole_avg: score += 15
                else: score -= 10
                
            if status == "confirmed": score += 20
            else:
                 if breakout_level != 0:
                    dist = abs(curr_price - breakout_level) / abs(breakout_level)
                    if dist < 0.02: score += 5
            
            if score > best_score:
                best_score = score
                
                # Target/Stop
                if direction == 'bull':
                    target = breakout_level + pole_height
                    stop = (slope_sup * (flag_width-1)) + int_sup
                else:
                    target = breakout_level - pole_height
                    stop = (slope_res * (flag_width-1)) + int_res
                
                strategy = (f"Hedef: {target:.2f}, Stop: {stop:.2f}. "
                           f"{'Kırılım geldi!' if status == 'confirmed' else 'Kırılım bekleniyor.'}")

                # Vade
                vade = self.calculate_smart_vade(int(flag_width*0.5), int(flag_width*1.5), timeframe)

                # ÇIKIŞ PAKETİ (Antigravity Çizim Motoru İçin Güncellendi)
                patterns.append({
                    'name': full_name,
                    'signal': 'Bullish' if direction == 'bull' else 'Bearish',
                    'desc': f"Direk: %{pole_height_pct*100:.1f}. Derinlik: %{retracement_pct*100:.0f}. {status.upper()}",
                    'points': [int(pole_base_idx), int(pole_end_idx), int(curr_idx)],
                    'type': 'flama' if is_pennant else 'bayrak',
                    'status': status,
                    'quality': 'Yüksek' if score > 75 else 'Normal',
                    'strategy': strategy,
                    'target': float(target),
                    'stop': float(stop),
                    'score': score,
                    'neckline': float(neckline),
                    'breakout_level': float(breakout_level),
                    'date_range': f"{pd.to_datetime(dates[pole_base_idx]).strftime('%d.%m')}-{pd.to_datetime(dates[curr_idx]).strftime('%d.%m')}",
                    'vade': vade,
                    
                    # --- ÇİZİM MOTORU İÇİN KOORDİNATLAR (Yeni) ---
                    "Points": {
                        "p_start_idx": int(pole_base_idx),
                        "p_start_val": float(pole_base),
                        "p_end_idx": int(pole_end_idx),
                        "p_end_val": float(high[pole_end_idx] if direction == 'bull' else low[pole_end_idx]),
                        "f_end_idx": int(curr_idx),
                        # Regresyon formülü: y = mx + c
                        "res_start": float((slope_res * 0) + int_res),
                        "res_end":   float((slope_res * (flag_width-1)) + int_res),
                        "sup_start": float((slope_sup * 0) + int_sup),
                        "sup_end":   float((slope_sup * (flag_width-1)) + int_sup)
                    },
                    "Formasyon": full_name, # Alias for user script compatibility
                    "Symbol": "N/A" # Will be filled by app
                })
                
        return sorted(patterns, key=lambda x: x['score'], reverse=True)[:1]

    def detect_rsi_divergence(self, df, zz_points=None, timeframe="Günlük"):
        """
        Detects RSI Divergences using robust Peak Matching logic.
        Elite Version:
        1. Peak Alignment: Precision within +/- 2 bars.
        2. Reset Check: (Line of Sight) RSI must not cross the midline significantly.
        3. Zone Validation: Extremas should originate from OB/OS areas.
        4. Confirmation: Logic checks for price/RSI momentum turn.
        """
        patterns = []
        if df is None or len(df) < 20 or 'RSI' not in df.columns: return patterns
        
        # Settings
        dev = self.config.get('zigzag_deviation', 0.04)
        tolerance = 2 # Elite tolerance (tight)
        
        close = df['Close'].values
        rsi = df['RSI'].values
        dates = df['Date'].values
        
        # Extrema detection
        price_lows = []
        price_highs = []
        
        if dev > 0.05:
            if zz_points is None:
                zz_points = self.calculate_zigzag(df, deviation=dev)
            price_lows = np.array([p['idx'] for p in zz_points if p['type'] == 'low'])
            price_highs = np.array([p['idx'] for p in zz_points if p['type'] == 'high'])
        else:
            order = max(3, int(dev * 100))
            price_lows = signal.argrelextrema(close, np.less, order=order)[0]
            price_highs = signal.argrelextrema(close, np.greater, order=order)[0]
            
            # Filter recent
            idx_limit = len(df) - 100
            price_lows = price_lows[price_lows > idx_limit]
            price_highs = price_highs[price_highs > idx_limit]
        
        # RSI Extremas
        rsi_lows = signal.argrelextrema(rsi, np.less, order=3)[0]
        rsi_highs = signal.argrelextrema(rsi, np.greater, order=3)[0]
        
        def get_matching_rsi(p_idx, r_candidates):
            if len(r_candidates) == 0: return None
            diffs = np.abs(r_candidates - p_idx)
            min_idx = np.argmin(diffs)
            if diffs[min_idx] <= tolerance: return r_candidates[min_idx]
            return None

        # --- Positive Divergence (Bullish) ---
        if self.config['enabled_patterns'].get('div_pos', True) and len(price_lows) >= 2:
            for i in range(len(price_lows)-1, 0, -1):
                p2 = price_lows[i] # Recent
                p1 = price_lows[i-1] # Previous
                
                if (len(df) - p2) > 30: continue
                
                # Rule 1: Price Lower Low
                if close[p2] < close[p1]:
                    r2 = get_matching_rsi(p2, rsi_lows)
                    r1 = get_matching_rsi(p1, rsi_lows)
                    
                    if r2 is not None and r1 is not None:
                        # Rule 2: RSI Higher Low
                        if rsi[r2] > rsi[r1] + 1:
                            # Rule 3: Line of Sight (Reset Check)
                            # If RSI crossed > 55 between points, the divergence is "broken"
                            inter_rsi = rsi[p1:p2+1]
                            if np.max(inter_rsi) > 55: continue
                            
                            # Rule 4: Zone Validation
                            # First low should be near/in oversold (<40)
                            if rsi[r1] > 45: continue 
                            
                            # Scoring
                            qual_score = 60
                            if rsi[r1] < 30: qual_score += 20 # Deep OS
                            if rsi[p2] < 45: qual_score += 10 # Stayed in weakness
                            
                            target_price = float(np.max(close[p1:p2+1]))
                            width = int(p2) - int(p1)
                            
                            # User Rule: Div forms in 5-10 bars
                            if width > 15: continue 
                            
                            # User Rule: Reaction lasts max 3 bars
                            vade_est = "3-5 Mum (Tepki)"
                            
                            strategy_text = (f"🎯 Hedef: {target_price:.2f} | ⏳ Süre: {vade_est}. "
                                             "Kısa vadeli tepki yükselişi (Scalp).")
                            
                            patterns.append({
                                'name': 'RSI Pozitif Uyuşmazlık',
                                'signal': 'Bullish',
                                'desc': f"Fiyat LL, RSI HL. Alan Onaylı. Direnç: {target_price:.2f}",
                                'points': [int(p1), int(p2)],
                                'type': 'divergence_pos',
                                'status': 'confirmed',
                                'quality': 'Riskli 🔥' if qual_score >= 80 else 'Normal',
                                'strategy': strategy_text,
                                'date_range': f"{pd.to_datetime(dates[p1]).strftime('%d.%m')} - {pd.to_datetime(dates[p2]).strftime('%d.%m')}",
                                'target': target_price,
                                'score': qual_score,
                                'vade': vade_est,
                                "Points": {
                                    "p1_idx": int(p1), "p1_val": float(close[p1]),
                                    "p2_idx": int(p2), "p2_val": float(close[p2]),
                                    "rsi1": float(rsi[r1]), "rsi2": float(rsi[r2])
                                }
                            })
                            break 

        # --- Negative Divergence (Bearish) ---
        if self.config['enabled_patterns'].get('div_neg', True) and len(price_highs) >= 2:
            for i in range(len(price_highs)-1, 0, -1):
                p2 = price_highs[i]
                p1 = price_highs[i-1]
                
                if (len(df) - p2) > 30: continue
                
                # Rule 1: Price Higher High
                if close[p2] > close[p1]:
                    r2 = get_matching_rsi(p2, rsi_highs)
                    r1 = get_matching_rsi(p1, rsi_highs)
                    
                    if r2 is not None and r1 is not None:
                        # Rule 2: RSI Lower High
                        if rsi[r2] < rsi[r1] - 1:
                            # Rule 3: Line of Sight (Reset Check)
                            # If RSI crossed < 45 between points, it's reset
                            inter_rsi = rsi[p1:p2+1]
                            if np.min(inter_rsi) < 45: continue
                            
                            # Rule 4: Zone Validation
                            if rsi[r1] < 55: continue # First peak must be high
                            
                            qual_score = 60
                            if rsi[r1] > 70: qual_score += 20 # Overbought origin
                            
                            target_price = float(np.min(close[p1:p2+1]))
                            width = int(p2) - int(p1)
                            
                            # User Rule: Div forms in 5-10 bars
                            if width > 15: continue
                            
                            # User Rule: Reaction lasts max 3 bars
                            vade_est = "3-5 Mum (Düzeltme)"
                            
                            strategy_text = (f"🎯 Destek: {target_price:.2f} | ⏳ Süre: {vade_est}. "
                                             "Kısa vadeli düzeltme beklentisi.")

                            patterns.append({
                                'name': 'RSI Negatif Uyuşmazlık',
                                'signal': 'Bearish',
                                'desc': f"Fiyat HH, RSI LH. Alan Onaylı. Destek: {target_price:.2f}",
                                'points': [int(p1), int(p2)],
                                'type': 'divergence_neg',
                                'status': 'confirmed',
                                'quality': 'Riskli 🔥' if qual_score >= 80 else 'Normal',
                                'strategy': strategy_text,
                                'date_range': f"{pd.to_datetime(dates[p1]).strftime('%d.%m')} - {pd.to_datetime(dates[p2]).strftime('%d.%m')}",
                                'target': target_price,
                                'score': qual_score,
                                'vade': vade_est,
                                "Points": {
                                    "p1_idx": int(p1), "p1_val": float(close[p1]),
                                    "p2_idx": int(p2), "p2_val": float(close[p2]),
                                    "rsi1": float(rsi[r1]), "rsi2": float(rsi[r2])
                                }
                            })
                            break
                            
        return patterns



    def detect_candlestick_patterns(self, df, timeframe="Günlük"):
        """
        Detects single or dual candlestick patterns (Doji, Hammer, Engulfing).
        Checks the LAST 2-3 bars only (Live signal).
        """
        patterns = []
        if df is None or len(df) < 5: return patterns
        
        # Get last few rows
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        O, H, L, C = last['Open'], last['High'], last['Low'], last['Close']
        pO, pH, pL, pC = prev['Open'], prev['High'], prev['Low'], prev['Close']
        
        points = [len(df)-1]
        date_str = pd.to_datetime(last['Date']).strftime('%d.%m')
        
        body = abs(C - O)
        rang = H - L
        if rang == 0: return patterns
        
        # 1. DOJI (Kararsızlık)
        # Body is very small relative to range
        if body <= rang * 0.10:
            # Dragonfly vs Gravestone vs Regular
            subtype = "Doji"
            if (C - L) > rang * 0.6 and (O - L) > rang * 0.6: subtype = "Dragonfly Doji (Boğa)"
            elif (H - C) > rang * 0.6 and (H - O) > rang * 0.6: subtype = "Gravestone Doji (Ayı)"
            
            patterns.append({
                'name': subtype,
                'signal': 'Neutral',
                'desc': f"{subtype}: Kararsızlık mumu. Yön değişimi habercisi olabilir.",
                'points': points,
                'status': 'confirmed',
                'quality': 'Normal',
                'type': 'candle',
                'score': 50,
                'date_range': date_str
            })
            
        # 2. HAMMER (Çekiç) - Bullish Reversal
        # Small body, long lower wick, little/no upper wick. Occurs after downtrend (handled loosely here)
        upper_wick = H - max(O, C)
        lower_wick = min(O, C) - L
        
        is_hammer_shape = (lower_wick > 2 * body) and (upper_wick < body * 0.5)
        if is_hammer_shape:
             patterns.append({
                'name': 'Çekiç (Hammer)',
                'signal': 'Bullish',
                'desc': "Uzun alt fitil, küçük gövde. Dipten dönüş sinyali.",
                'points': points,
                'status': 'confirmed',
                'quality': 'Yüksek' if lower_wick > 3 * body else 'Normal',
                'type': 'candle',
                'score': 65,
                'date_range': date_str
            })

        # 3. SHOOTING STAR (Kayan Yıldız) - Bearish Reversal
        is_shooting_star = (upper_wick > 2 * body) and (lower_wick < body * 0.5)
        if is_shooting_star:
             patterns.append({
                'name': 'Kayan Yıldız (Shooting Star)',
                'signal': 'Bearish',
                'desc': "Uzun üst fitil, küçük gövde. Tepeden dönüş sinyali.",
                'points': points,
                'status': 'confirmed',
                'quality': 'Yüksek' if upper_wick > 3 * body else 'Normal',
                'type': 'candle',
                'score': 65,
                'date_range': date_str
            })
            
        # 4. ENGULFING (Yutan Boğa / Ayı)
        # Current body engulfs previous body
        prev_body = abs(pC - pO)
        is_engulfing = (body > prev_body) and (max(C, O) >= max(pC, pO)) and (min(C, O) <= min(pC, pO))
        
        if is_engulfing:
            # Bullish Engulfing: Prev Red, Curr Green
            if pC < pO and C > O:
                patterns.append({
                    'name': 'Yutan Boğa (Bullish Engulfing)',
                    'signal': 'Bullish',
                    'desc': "Önceki kırmızı mumu tamamen içine alan yeşil mum. Güçlü yükseliş sinyali.",
                    'points': [len(df)-2, len(df)-1],
                    'status': 'confirmed',
                    'quality': 'Güçlü',
                    'type': 'candle',
                    'score': 75,
                    'date_range': date_str
                })
            # Bearish Engulfing: Prev Green, Curr Red
            elif pC > pO and C < O:
                 patterns.append({
                    'name': 'Yutan Ayı (Bearish Engulfing)',
                    'signal': 'Bearish',
                    'desc': "Önceki yeşil mumu tamamen içine alan kırmızı mum. Güçlü düşüş sinyali.",
                    'points': [len(df)-2, len(df)-1],
                    'status': 'confirmed',
                    'quality': 'Güçlü',
                    'type': 'candle',
                    'score': 75,
                    'date_range': date_str
                })
                
        return patterns

    def calculate_smart_vade(self, bars_min, bars_max, timeframe):
        """
        Converts bar counts to human readable time estimates based on timeframe.
        """
        tf_lower = timeframe.lower()
        
        if "saat" in tf_lower or timeframe == "S" or timeframe == "60min":
            # Hourly: Bars = Hours
            # If > 8 hours (1 trading day), convert to days
            if bars_min > 9:
                d_min = round(bars_min / 9, 1)
                d_max = round(bars_max / 9, 1)
                return f"{d_min}-{d_max} İş Günü"
            return f"{bars_min}-{bars_max} Saat"
            
        elif "gün" in tf_lower or timeframe == "G" or timeframe == "D":
            # Daily: Bars = Days
            # If > 5 days, convert to weeks
            if bars_min >= 5:
                w_min = round(bars_min / 5, 1)
                w_max = round(bars_max / 5, 1)
                return f"{w_min}-{w_max} Hafta"
            return f"{bars_min}-{bars_max} İş Günü"
            
        elif "hafta" in tf_lower or timeframe == "W":
            # Weekly: Bars = Weeks
            if bars_min >= 4:
                m_min = round(bars_min / 4, 1)
                m_max = round(bars_max / 4, 1)
                return f"{m_min}-{m_max} Ay"
            return f"{bars_min}-{bars_max} Hafta"
            
        elif "ay" in tf_lower or timeframe == "M":
             return f"{bars_min}-{bars_max} Ay"
             
        return f"{bars_min}-{bars_max} Mum (Bar)"


    def detect_classic_patterns(self, df, timeframe="Günlük"):
        """
        Detects specific geometric patterns using ZigZag.
        """
        patterns = []
        if df is None or len(df) < 15: return patterns
        
        # Data Safety: Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            try:
                df.columns = df.columns.get_level_values(0)
            except: pass
            
        try:
            # 1. Calculate ZigZag
            dev = self.config.get('zigzag_deviation', 0.04)
            zz_points = self.calculate_zigzag(df, deviation=dev)
            
            # 2. TOBO Detection
            if self.config['enabled_patterns'].get('tobo', True):
                tobo_pats = self.detect_tobo_zigzag(df, zz_points, timeframe)
                patterns.extend(tobo_pats)
                
            # 2.1 OBO Detection (Inverse)
            if self.config['enabled_patterns'].get('obo', True):
                obo_pats = self.detect_obo_pattern(df, timeframe)
                patterns.extend(obo_pats)
                
            # 3. Cup & Handle
            if self.config['enabled_patterns'].get('cup', True):
                cup_pats = self.detect_cup_zigzag(df, zz_points, timeframe)
                patterns.extend(cup_pats)
                
            # 4. Flag / Pennant (Combined Detection, then Filter)
            enable_flag = self.config['enabled_patterns'].get('flag', True)
            enable_flama = self.config['enabled_patterns'].get('flama', True)
            
            if enable_flag or enable_flama:
                mixed_pats = self.detect_flag_pattern(df, timeframe)
                for p in mixed_pats:
                    if p['type'] == 'bayrak' and enable_flag:
                        patterns.append(p)
                    elif p['type'] == 'flama' and enable_flama:
                        patterns.append(p)
            
            # 5. RSI Divergence
            div_pats = self.detect_rsi_divergence(df, zz_points, timeframe)
            patterns.extend(div_pats)
            
        except Exception as e:
            print(f"Error in pattern detection: {e}")
            
        return patterns
    def add_indicators(self, df):
        """Adds technical indicators to the dataframe."""
        if df is None or df.empty:
            return df

        df = df.copy()
        # Ensure stats are calculated
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Volume SMA (For Confirmation)
        if 'Volume' in df.columns:
             df['Vol_SMA_20'] = df['Volume'].rolling(window=20).mean()
        
        # MACD
        exp12 = df['Close'].ewm(span=12, adjust=False).mean()
        exp26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp12 - exp26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        df['BB_Mid'] = df['Close'].rolling(window=20).mean()
        df['BB_Std'] = df['Close'].rolling(window=20).std()
        df['BB_High'] = df['BB_Mid'] + (2 * df['BB_Std'])
        df['BB_Low'] = df['BB_Mid'] - (2 * df['BB_Std'])
        
        # ATR (Average True Range)
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=14).mean()
        
        return df

    def detect_patterns(self, df):
        """Detects simple patterns like Golden Cross or Oversold."""
        patterns = []
        if df is None or len(df) < 50:
            return patterns

        curr = df.iloc[-1]
        prev = df.iloc[-2]

        # RSI Checks
        if curr['RSI'] < 30:
            patterns.append("RSI Oversold (Bullish)")
        elif curr['RSI'] > 70:
            patterns.append("RSI Overbought (Bearish)")

        # Golden Cross (SMA 50 crosses above SMA 200)
        # Check specific crossover in last few days
        if 'SMA_200' in df.columns and not np.isnan(curr['SMA_200']):
            if prev['SMA_50'] < prev['SMA_200'] and curr['SMA_50'] > curr['SMA_200']:
                patterns.append("Golden Cross (Bullish)")
            elif prev['SMA_50'] > prev['SMA_200'] and curr['SMA_50'] < curr['SMA_200']:
                patterns.append("Death Cross (Bearish)")
        
        # Bollinger Bands - Squeeze or Breakout
        if curr['Close'] > curr['BB_High']:
            patterns.append("Bollinger Breakout (Upper)")
        elif curr['Close'] < curr['BB_Low']:
            patterns.append("Bollinger Breakout (Lower)")
            
        # -------------------
        # CLASSIC PATTERNS
        # -------------------
        classic_patterns = self.detect_classic_patterns(df)
        patterns.extend(classic_patterns)
        
        # -------------------

        return patterns

    def get_detailed_signals(self, df):
        """
        Generates explicit BUY/SELL/NEUTRAL signals with reasons.
        Returns a list of dicts: {'indicator': 'RSI', 'signal': 'AL', 'color': 'green', 'reason': '...'}
        """
        signals = []
        if df is None or len(df) < 50: return signals
        
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 1. RSI
        rsi_val = curr['RSI']
        if rsi_val < 30:
            signals.append({
                'indicator': 'RSI', 'signal': 'AL', 'color': 'green',
                'reason': f"RSI {rsi_val:.0f} < 30. Aşırı satım bölgesinde (Ucuz). Tepki yükselişi beklenebilir."
            })
        elif rsi_val > 70:
            signals.append({
                'indicator': 'RSI', 'signal': 'SAT', 'color': 'red',
                'reason': f"RSI {rsi_val:.0f} > 70. Aşırı alım bölgesinde (Pahalı). Kâr satışı gelebilir."
            })
        else:
             signals.append({
                'indicator': 'RSI', 'signal': 'NÖTR', 'color': 'grey',
                'reason': f"RSI {rsi_val:.0f} seviyesinde makul bölgede. Yön belirsiz."
            })
            
        # 2. MACD
        # Buy: MACD crosses above Signal
        if curr['MACD'] > curr['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
             signals.append({
                'indicator': 'MACD', 'signal': 'AL', 'color': 'green',
                'reason': "MACD çizgisi sinyal çizgisini YUKARI kesti (Pozitif Kesişim)."
            })
        elif curr['MACD'] < curr['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
             signals.append({
                'indicator': 'MACD', 'signal': 'SAT', 'color': 'red',
                'reason': "MACD çizgisi sinyal çizgisini AŞAĞI kesti (Negatif Kesişim)."
            })
        else:
            trend = "Pozitif" if curr['MACD'] > curr['MACD_Signal'] else "Negatif"
            color = "green" if trend == "Pozitif" else "red"
            signals.append({
                'indicator': 'MACD', 'signal': trend.upper(), 'color': color,
                'reason': f"MACD, Sinyal çizgisinin {'üzerinde' if trend=='Pozitif' else 'altında'} seyrediyor."
            })
            
        # 3. Bollinger Bands
        if curr['Close'] < curr['BB_Low']:
             signals.append({
                'indicator': 'Bollinger', 'signal': 'AL', 'color': 'green',
                'reason': "Fiyat alt bandın altında/hizasında. 'Ucuzluk' algısı oluşabilir."
            })
        elif curr['Close'] > curr['BB_High']:
             signals.append({
                'indicator': 'Bollinger', 'signal': 'SAT', 'color': 'red',
                'reason': "Fiyat üst bandı zorluyor. Düzeltme riski yüksek."
            })
        else:
             signals.append({
                'indicator': 'Bollinger', 'signal': 'NÖTR', 'color': 'grey',
                'reason': "Fiyat bantların içerisinde hareket ediyor."
            })
            
        # 4. Golden/Death Cross
        if 'SMA_50' in df.columns:
            if curr['SMA_50'] > curr['SMA_200']:
                signals.append({'indicator': 'Trend (SMA)', 'signal': 'POZİTİF', 'color': 'green', 'reason': "Golden Cross aktif (50 > 200). Uzun vadeli trend yukarı."})
            else:
                signals.append({'indicator': 'Trend (SMA)', 'signal': 'NEGATİF', 'color': 'red', 'reason': "Death Cross aktif (50 < 200). Uzun vadeli trend aşağı."})
                
        return signals

    def get_explanations(self):
        """Returns dictionary of explanations for indicators."""
        return {
            "RSI (Relative Strength Index)": "Hissenin aşırı alım veya aşırı satım bölgelerini gösterir. 30 altı 'ucuz/aşırı satım' (alım fırsatı olabilir), 70 üstü 'pahalı/aşırı alım' (düşüş gelebilir) olarak yorumlanır.",
            "SMA (Simple Moving Average)": "Belirli bir periyottaki ortalama fiyattır. 50 günlük ortalama 200 günlüğü yukarı keserse 'Golden Cross' (Yükseliş), aşağı keserse 'Death Cross' (Düşüş) sinyalidir.",
            "MACD": "Trendin gücünü ve yönünü gösterir. Sinyal çizgisini yukarı kesmesi al, aşağı kesmesi sat sinyali olabilir.",
            "Bollinger Bands": "Fiyatın standart sapmasına göre çizilen bantlardır. Bantların daralması fiyatta sert bir hareketin habercisi olabilir. Fiyatın üst bandı delmesi güçlü yükseliş, altı delmesi güçlü düşüş eğilimi gösterebilir.",
            "ATR (Average True Range)": "Piyasadaki volatiliteyi (oynaklığı) ölçer. Yüksek ATR, fiyatın gün içinde çok hareketli olduğunu gösterir."
        }
        
    def analyze_trend(self, df, macro_events=[]):
        """
        Generates a text summary of the current trend with Macro Context.
        
        Args:
            df: Stock dataframe
            macro_events: List of macro events that happened recently (e.g. last 10 days relative to end of data)
        """
        if df is None or len(df) < 20:
            return "Yeterli veri yok.", []
            
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        trend_score = 0
        factors = [] # List of tuples: (Factor Name, Description, Impact 'Positive'/'Negative'/'Neutral')
        
        # 1. Price vs SMA Trend
        if curr['Close'] > curr['SMA_50']:
            trend_score += 1
            factors.append(("Trend (SMA 50)", "Fiyat 50 günlük ortalamanın üzerinde, kısa-orta vade yükseliş trendi.", "Pozitif"))
        else:
            trend_score -= 1
            factors.append(("Trend (SMA 50)", "Fiyat 50 günlük ortalamanın altında, düşüş baskısı var.", "Negatif"))
            
        # 2. Momentum (RSI)
        if 40 < curr['RSI'] < 60:
            factors.append(("Momentum (RSI)", f"RSI {curr['RSI']:.0f} seviyesinde nötr.", "Nötr"))
        elif curr['RSI'] <= 40:
             trend_score += 0.5 
             factors.append(("Momentum (RSI)", f"RSI {curr['RSI']:.0f} ile aşırı satım/ucuz bölgesine yakın.", "Pozitif (Tepki Beklentisi)"))
        elif curr['RSI'] >= 70:
             trend_score -= 0.5
             factors.append(("Momentum (RSI)", f"RSI {curr['RSI']:.0f} ile aşırı alım bölgesinde, düzeltme gelebilir.", "Negatif (Riskli)"))
        elif curr['RSI'] >= 60:
             trend_score += 0.5
             factors.append(("Momentum (RSI)", f"RSI {curr['RSI']:.0f} güçlü bölgede.", "Pozitif"))

        # 3. Volatility (ATR & Bollinger)
        bb_width = (curr['BB_High'] - curr['BB_Low']) / curr['BB_Mid']
        if curr['Close'] > curr['BB_High']:
             factors.append(("Volatilite (Bollinger)", "Fiyat üst bandı deldi, güçlü yükseliş (ancak sert düzeltme riski).", "Dikkat"))
        elif curr['Close'] < curr['BB_Low']:
             factors.append(("Volatilite (Bollinger)", "Fiyat alt bandı deldi, güçlü düşüş.", "Negatif"))
             
        # 4. Macro Context
        recent_macro = [e for e in macro_events if (pd.to_datetime(curr['Date']) - pd.to_datetime(e['date'])).days <= 7]
        
        if recent_macro:
            for event in recent_macro:
                event_name = event['event']
                if "Faiz İndirimi" in event_name:
                    trend_score += 0.5
                    factors.append(("Makro Gündem", f"{event_name} gerçekleşti. Faiz indirimleri genellikle borsayı destekler.", "Pozitif"))
                elif "Faiz Artışı" in event_name:
                    trend_score -= 0.5
                    factors.append(("Makro Gündem", f"{event_name} gerçekleşti. Faiz artışları borçlanma maliyetini artırır, satış baskısı yaratabilir.", "Negatif"))
                else:
                    factors.append(("Makro Gündem", f"Yakın zamanda {event_name} açıklandı, piyasa bunu fiyatlıyor olabilir.", "Nötr/Belirsiz"))
        else:
             factors.append(("Makro Gündem", "Yakın tarihte kritik bir FED/TCMB kararı bulunmuyor.", "Nötr"))

        # Conclusion Score Logic
        if trend_score >= 1.5:
            sentiment = "GÜÇLÜ POZİTİF"
        elif trend_score >= 0.5:
            sentiment = "POZİTİF"
        elif trend_score <= -1.5:
            sentiment = "GÜÇLÜ NEGATİF"
        elif trend_score <= -0.5:
            sentiment = "NEGATİF"
        else:
            sentiment = "NÖTR / BELİRSİZ"
            
        return sentiment, factors

    def analyze_ownership(self, holders_df):
        # Analyzes ownership dataframe to determine if 'Takas' is concentrated or dispersed.
        # Returns: (Score change, Factor Tuple)
        if holders_df is None or holders_df.empty:
            return 0, ("Takas Analizi", "Veri çekilemedi.", "Nötr")
            
        try:
            insider_pct = 0.0
            search_col = 1 if len(holders_df.columns) > 1 else 0
            val_col = 0
            
            for idx, row in holders_df.iterrows():
                desc = str(row[search_col]).lower()
                val_str = str(row[val_col]).replace('%', '').strip()
                try:
                    val = float(val_str)
                except:
                    continue
                    
                if "insider" in desc:
                    insider_pct = val
                    break
            
            impact = "Nötr"
            score = 0
            desc = f"Insider (İçeriden) Sahiplik: %{insider_pct:.2f}"
            
            if insider_pct > 60:
                impact = "Pozitif (Toplu)"
                score = 0.5
                desc += ". Takasın toplu olduğu görülüyor (Patron/Büyük ortak hakimiyeti). Satış baskısı daha kontrollü olabilir."
            elif insider_pct < 30:
                impact = "Nötr/Negatif (Dağınık)"
                score = -0.25
                desc += ". Takas nispeten dağınık, küçük yatırımcı etkisi yüksek olabilir (Volatilite riski)."
            else:
                desc += ". Takas dengeli görünüyor."
                
            return score, ("Takas Analizi (Toplu/Dağınık)", desc, impact)
            
        except Exception as e:
            return 0, ("Takas Analizi", f"Veri işlenirken hata: {str(e)}", "Nötr")

    def normalize_series(self, series):
        # Normalizes a series to start at 0 and be percentage change, or min-max scale.
        if len(series) == 0:
            return series
        return (series - series.min()) / (series.max() - series.min())

    def find_similar_patterns(self, target_df, comparison_dict, window_size=60, top_n=3):
        '''
        Finds IPOs that had a similar price action to the recent history of the target dataframe.
        '''
        if len(target_df) < window_size:
            return []

        target_seq = target_df['Close'].iloc[-window_size:].values
        target_seq_norm = self.normalize_series(target_seq)

        scores = []

        for ticker, comp_df in comparison_dict.items():
            if len(comp_df) < window_size:
                continue
            
            comp_seq = comp_df['Close'].iloc[:window_size].values 
            if len(comp_seq) < window_size:
                continue
                
            comp_seq_norm = self.normalize_series(comp_seq)
            dist = np.linalg.norm(target_seq_norm - comp_seq_norm)
            
            scores.append({
                'ticker': ticker,
                'score': dist, 
                'dates_compared': 'First 60 Days'
            })

        scores.sort(key=lambda x: x['score'])
        return scores[:top_n]
