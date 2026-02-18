import asyncio
from metaapi_cloud_sdk import MetaApi
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime, timedelta

# Force flush stdout
# sys.stdout.reconfigure(line_buffering=True)
print("Starting script...", flush=True)

# Configuration
TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYjllMmEwZGM1Y2M1OTM0ODUxMGZjNzNhZGJiMGE3MyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiM2I5ZTJhMGRjNWNjNTkzNDg1MTBmYzczYWRiYjBhNzMiLCJpYXQiOjE3NzEzNjA3ODJ9.LWvwBRCttxN_89L59ibidG_FfeR_Z5J6DSBBC-YKSVqHTE01vszF-2pkbby_eprH8N-A_sCjzUDLC7zj4rIYU1ZdjZQA8nTAg3ocR27j-aov1n3eiCV5MpF5JpMKocqL7SJYbMwEIEb7Rhfs_txMaLDwTqp2TJb36Gil2UnQweS6b5OYpPF1gKFXHIsPvG5_seSZ0vYUPeC5aG67VmR4VQH2W9kxKCyI0Is6bt55xNwl1jRpbuWgs2OcTJFIcN8rWZrKJNX3pZzXOJYJt2vbrzp2prf1DqeouawBO39n45crRhO7Z6m98-4WowgsSHoCtI-4ye1sZ8p3XcJRD1HMxObjIuBC57E7E16jLP90qBm5t4rXIlkSwJXoxUFu_tRo8KsQ_WPhf3MLN4npmZ2B4mc7dfSx7QaIZHx71lBztBShCw3WSD_K-A-UNaiY_9aTy51rSe6avRRSJ-PiC_6Cx8HTjQFtB8BIf_hSw5B_lQAn1WIDcN_e7XZn07Y9UIeAYtz3u8pNXcnkL4UnU64Qx17pX4WSYnsj0VAFp_w5nIy4Ls8aR3ByqqXE5-jujmAVTMSLJHey-Ad0ncIi0l4mHIttvepQyOnES7BpnNMNGUrXFzpKZrPnDUmFyzTcZSBQuh01MF65VTEJPtP2T9wrNib1klB-bSs_OVGOWAVx8aA"
ACCOUNT_ID = "91ed7198-e093-47b8-9940-f73a07ca49e4"
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY"]
TIMEFRAMES = ["5m", "15m"]
OUTPUT_DIR = "/data/trading_monitor"

async def test_connection(api):
    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        print(f"Connected to account: {account.name} ({account.id})", flush=True)
        return account
    except Exception as e:
        print(f"Connection failed: {e}", flush=True)
        return None

async def get_candles(account, symbol, timeframe, limit=100):
    try:
        minutes = 5 if timeframe == '5m' else 15
        start_time = datetime.now() - timedelta(minutes=minutes * limit * 1.5) 
        
        candles = await account.get_historical_candles(symbol, timeframe, start_time)
        
        if not candles:
             print(f"Warning: No candles returned for {symbol} {timeframe}", flush=True)
             return pd.DataFrame()
        
        df = pd.DataFrame(candles)
        df['time'] = pd.to_datetime(df['time'])
        return df
    except Exception as e:
        print(f"Error getting candles for {symbol} {timeframe}: {e}", flush=True)
        return pd.DataFrame()

def detect_strategy_a(df):
    """
    Strategy A: Price Origins / Zone Rejection (Scalping)
    - Concept: "Zone Recovery" or "Origin of Move"
    - Logic: 
        1. Identify a strong directional move (Impulse).
        2. Mark the "Origin" (Base) of that move as a Key Level.
        3. If price returns to this Origin level, it's an entry zone.
        4. User ladders multiple entries around this level.
        5. Target: Small scalps (7-10 pips).
    """
    df['strategy_a'] = False
    df['strategy_a_type'] = None
    if len(df) < 50: return df

    # 1. Identify "Origin" Levels from history
    # An origin is a candle that started a strong trend (series of same-color candles or large body)
    
    # Calculate body and direction
    df['body'] = df['close'] - df['open']
    df['abs_body'] = abs(df['body'])
    df['direction'] = df['body'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    df['atr'] = df['high'] - df['low'] # Simple range for volatility context

    # Look back to find "Origins"
    # We simulate this by checking if CURRENT price is inside a historical Origin Zone
    
    # We need to store active zones. For a simple scanner, we look for:
    # - Did price just touch a level that was the start of a big move previously?
    
    # Let's simplify for the scanner:
    # Find significant previous impulses (e.g., > 2x ATR)
    # If current price retraces to the OPEN of that impulse candle, trigger signal.
    
    # Define "Big Move" threshold (e.g., body > 2 * 20-period average body)
    avg_body = df['abs_body'].rolling(window=20).mean()
    
    # Iterate backwards to find zones? No, iterate forward to simulate real-time
    # We maintain a list of "Active Zones" [price, direction, creation_time]
    
    # For the chart generation, we just mark the current bar if it triggers.
    
    current_idx = df.index[-1]
    current_price = df.iloc[-1]['close'] # Checking close or low/high? Touch is better.
    current_low = df.iloc[-1]['low']
    current_high = df.iloc[-1]['high']
    
    # Naive implementation for visual check:
    # Check last 50 candles for a "Big Impulse"
    for i in range(len(df)-50, len(df)-5): # Look at history, excluding immediate recent
        if i < 0: continue
        
        candle = df.iloc[i]
        limit_body = avg_body.iloc[i] * 2.5 # Threshold for "Big Move"
        
        if candle['abs_body'] > limit_body:
            # It's an impulse.
            origin_level = candle['open']
            direction = candle['direction'] # 1 (Bullish), -1 (Bearish)
            
            # Check if CURRENT price is testing this origin
            # Bullish Impulse Origin (Support) -> We want to Buy if price drops to it
            if direction == 1: 
                # Check if current low touched the origin level (within tolerance, e.g., 3 pips)
                # 3 pips approx 0.0003 for EURUSD
                dist = abs(current_low - origin_level)
                if dist < 0.0005 and current_price >= origin_level: # Touching support
                     df.at[current_idx, 'strategy_a'] = True
                     df.at[current_idx, 'strategy_a_type'] = f"Test Buy Origin @ {origin_level}"

            # Bearish Impulse Origin (Resistance) -> We want to Sell if price rises to it
            elif direction == -1:
                dist = abs(current_high - origin_level)
                if dist < 0.0005 and current_price <= origin_level: # Touching resistance
                     df.at[current_idx, 'strategy_a'] = True
                     df.at[current_idx, 'strategy_a_type'] = f"Test Sell Origin @ {origin_level}"
                     
    return df

def detect_strategy_b(df):
    """
    Strategy B: Trend Snapback / Bear Market Rally
    - Concept: "Unrealistic Sharp Counter-Move"
    - Logic:
        1. Identify clear trend (e.g., MA slope or price action).
        2. Wait for a SHARP, FAST move against the trend ("Unrealistic").
        3. Entry: Fade the move (Join the original trend).
        4. Target: Break the previous extreme (Higher High for uptrend, Lower Low for downtrend).
    """
    df['strategy_b'] = False
    df['strategy_b_type'] = None
    if len(df) < 50: return df
    
    # 1. Trend Filter (e.g., 50 SMA)
    df['sma50'] = df['close'].rolling(window=50).mean()
    
    # 2. Volatility (ATR-like)
    df['range'] = df['high'] - df['low']
    df['avg_range'] = df['range'].rolling(window=20).mean()
    
    current_idx = df.index[-1]
    current = df.iloc[-1]
    trend = 1 if current['close'] > current['sma50'] else -1
    
    # Check for "Unrealistic" Counter-Move (Large Range Candle against trend)
    # e.g., Range > 3x Avg Range AND Candle Direction is Against Trend
    
    is_large_candle = current['range'] > (df.iloc[-2]['avg_range'] * 3.0)
    candle_direction = 1 if current['close'] > current['open'] else -1
    
    if is_large_candle and candle_direction != trend:
        # It's a sharp counter-move!
        signal_type = "Bullish Snapback" if trend == 1 else "Bearish Snapback"
        df.at[current_idx, 'strategy_b'] = True
        df.at[current_idx, 'strategy_b_type'] = signal_type

    return df

def generate_chart(df, symbol, timeframe, filename):
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price')])

    a_signals = df[df['strategy_a']]
    if not a_signals.empty:
        fig.add_trace(go.Scatter(
            x=a_signals['time'], 
            y=a_signals['low'] - (a_signals['high'] - a_signals['low'])*0.1,
            mode='markers+text', 
            marker=dict(symbol='triangle-up', size=12, color='blue'),
            text=a_signals['strategy_a_type'],
            textposition="bottom center",
            name='Strat A (Origin)'
        ))

    b_signals = df[df['strategy_b']]
    if not b_signals.empty:
        fig.add_trace(go.Scatter(
            x=b_signals['time'], 
            y=b_signals['high'] + (b_signals['high'] - b_signals['low'])*0.1,
            mode='markers', 
            marker=dict(symbol='star', size=12, color='orange'),
            name='Strat B (Spike)'
        ))

    fig.update_layout(
        title=f'{symbol} ({timeframe}) - {datetime.now().strftime("%H:%M UTC")}',
        xaxis_rangeslider_visible=False,
        height=600,
        template="plotly_dark"
    )
    
    path = os.path.join(OUTPUT_DIR, filename)
    fig.write_image(path)
    return path

async def main():
    print("Starting Autonomous Monitor...", flush=True)
    try:
        api = MetaApi(TOKEN)
        account = await test_connection(api)
        if not account:
            print("Failed to get account.", flush=True)
            return

        iterations = (5 * 60) // 15 # Run for 5 hours
        
        for i in range(iterations):
            print(f"\n--- Scan Cycle {i+1}/{iterations} at {datetime.now()} ---", flush=True)
            
            scan_results = []
            
            for symbol in SYMBOLS:
                for tf in TIMEFRAMES:
                    try:
                        df = await get_candles(account, symbol, tf)
                        if df.empty: continue
                        
                        df = detect_strategy_a(df)
                        df = detect_strategy_b(df)
                        
                        last_candles = df.iloc[-3:]
                        if last_candles['strategy_a'].any() or last_candles['strategy_b'].any():
                            print(f"Signal detected on {symbol} {tf}!", flush=True)
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            filename = f"chart_{symbol}_{tf}_{timestamp}.png"
                            path = generate_chart(df, symbol, tf, filename)
                            scan_results.append(path)
                            
                    except Exception as e:
                        print(f"Error scanning {symbol} {tf}: {e}", flush=True)

            if i == 0 and not scan_results:
                 print("First run: Generating baseline chart for EURUSD 15m...", flush=True)
                 df = await get_candles(account, "EURUSD", "15m")
                 if not df.empty:
                     df = detect_strategy_a(df)
                     df = detect_strategy_b(df)
                     path = generate_chart(df, "EURUSD", "15m", "chart_baseline_EURUSD.png")
                     with open(os.path.join(OUTPUT_DIR, "first_run_complete.txt"), "w") as f:
                        f.write(path)

            if scan_results:
                with open(os.path.join(OUTPUT_DIR, "latest_signals.txt"), "w") as f:
                    for res in scan_results:
                        f.write(f"{res}\n")

            await asyncio.sleep(15 * 60) # Sleep 15 mins
            
    except Exception as e:
        print(f"CRITICAL ERROR in main: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())