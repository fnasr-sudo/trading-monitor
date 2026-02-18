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
    Strategy A: Price Origins / Rejection
    """
    df['strategy_a'] = False
    df['strategy_a_type'] = None
    if len(df) < 5: return df
    
    df['body'] = abs(df['open'] - df['close'])
    df['avg_body'] = df['body'].rolling(window=20).mean()
    
    for i in range(2, len(df)):
        current = df.iloc[i]
        prev = df.iloc[i-1]
        
        is_impulse = current['body'] > (df.iloc[i]['avg_body'] * 2.5)
        
        if is_impulse:
            is_base = prev['body'] < (df.iloc[i]['avg_body'] * 0.8)
            upper_wick = prev['high'] - max(prev['open'], prev['close'])
            lower_wick = min(prev['open'], prev['close']) - prev['low']
            is_rejection = (upper_wick > prev['body'] * 1.5) or (lower_wick > prev['body'] * 1.5)

            if is_base or is_rejection:
                df.at[df.index[i], 'strategy_a'] = True
                df.at[df.index[i], 'strategy_a_type'] = 'Origin/Base' if is_base else 'Rejection'
                
    return df

def detect_strategy_b(df):
    """
    Strategy B: Sharp Spikes / Snapback
    """
    df['strategy_b'] = False
    if len(df) < 20: return df
    
    df['range'] = df['high'] - df['low']
    df['avg_range'] = df['range'].rolling(window=20).mean()
    
    for i in range(1, len(df)):
        current = df.iloc[i]
        is_spike = current['range'] > (df.iloc[i]['avg_range'] * 3.0)
        
        if is_spike:
            df.at[df.index[i], 'strategy_b'] = True
            
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