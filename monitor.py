import asyncio
from metaapi_cloud_sdk import MetaApi
import pandas as pd
import plotly.graph_objects as go
import os
import sys
from datetime import datetime

# Force flush stdout
sys.stdout.reconfigure(line_buffering=True)

# Configuration
TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYjllMmEwZGM1Y2M1OTM0ODUxMGZjNzNhZGJiMGE3MyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiM2I5ZTJhMGRjNWNjNTkzNDg1MTBmYzczYWRiYjBhNzMiLCJpYXQiOjE3NzEzNjA3ODJ9.LWvwBRCttxN_89L59ibidG_FfeR_Z5J6DSBBC-YKSVqHTE01vszF-2pkbby_eprH8N-A_sCjzUDLC7zj4rIYU1ZdjZQA8nTAg3ocR27j-aov1n3eiCV5MpF5JpMKocqL7SJYbMwEIEb7Rhfs_txMaLDwTqp2TJb36Gil2UnQweS6b5OYpPF1gKFXHIsPvG5_seSZ0vYUPeC5aG67VmR4VQH2W9kxKCyI0Is6bt55xNwl1jRpbuWgs2OcTJFIcN8rWZrKJNX3pZzXOJYJt2vbrzp2prf1DqeouawBO39n45crRhO7Z6m98-4WowgsSHoCtI-4ye1sZ8p3XcJRD1HMxObjIuBC57E7E16jLP90qBm5t4rXIlkSwJXoxUFu_tRo8KsQ_WPhf3MLN4npmZ2B4mc7dfSx7QaIZHx71lBztBShCw3WSD_K-A-UNaiY_9aTy51rSe6avRRSJ-PiC_6Cx8HTjQFtB8BIf_hSw5B_lQAn1WIDcN_e7XZn07Y9UIeAYtz3u8pNXcnkL4UnU64Qx17pX4WSYnsj0VAFp_w5nIy4Ls8aR3ByqqXE5-jujmAVTMSLJHey-Ad0ncIi0l4mHIttvepQyOnES7BpnNMNGUrXFzpKZrPnDUmFyzTcZSBQuh01MF65VTEJPtP2T9wrNib1klB-bSs_OVGOWAVx8aA"
ACCOUNT_ID = "91ed7198-e093-47b8-9940-f73a07ca49e4"
SYMBOL = "XAUUSD"
TIMEFRAME = "15m"
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
    connection = account.get_rpc_connection()
    await connection.connect()
    await connection.wait_synchronized()
    
    # Introspection
    print(f"Connection type: {type(connection)}", flush=True)
    print(f"Connection dir: {[m for m in dir(connection) if not m.startswith('_')]}", flush=True)

    # Documentation suggests get_candle for the last candle, but we want history.
    # The RPC connection should have get_historical_candles in newer SDK versions.
    if hasattr(connection, 'get_historical_candles'):
        return pd.DataFrame(await connection.get_historical_candles(symbol, timeframe, limit=limit))
    
    # If not, let's try the candle method again with a fallback
    try:
        candle = await connection.get_candle(symbol, timeframe)
        return pd.DataFrame([candle])
    except Exception as e:
        print(f"Retrying get_candle failed: {e}", flush=True)
        raise e

def detect_strategy_a(df):
    df['strategy_a'] = False
    if len(df) < 2: return df
    for i in range(1, len(df)):
        body = abs(df.iloc[i]['open'] - df.iloc[i]['close'])
        prev_body = abs(df.iloc[i-1]['open'] - df.iloc[i-1]['close'])
        if body > prev_body * 3:
            df.at[df.index[i], 'strategy_a'] = True
    return df

def detect_strategy_b(df):
    df['strategy_b'] = False
    if len(df) < 20: return df
    avg_range = (df['high'] - df['low']).rolling(window=20).mean()
    for i in range(len(df)):
        current_range = df.iloc[i]['high'] - df.iloc[i]['low']
        if current_range > avg_range.iloc[i] * 2.5:
            df.at[df.index[i], 'strategy_b'] = True
    return df

def generate_chart(df, filename):
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price')])
    a_signals = df[df['strategy_a']]
    if not a_signals.empty:
        fig.add_trace(go.Scatter(x=a_signals['time'], y=a_signals['low'],
                                 mode='markers', marker=dict(symbol='triangle-up', size=10, color='blue'),
                                 name='Strategy A (Origin)'))
    b_signals = df[df['strategy_b']]
    if not b_signals.empty:
        fig.add_trace(go.Scatter(x=b_signals['time'], y=b_signals['high'],
                                 mode='markers', marker=dict(symbol='star', size=10, color='orange'),
                                 name='Strategy B (Spike)'))
    fig.update_layout(title=f'{SYMBOL} Monitor - {datetime.now()}', xaxis_rangeslider_visible=False)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.write_image(path)
    return path

async def main():
    print("Starting main...", flush=True)
    api = MetaApi(TOKEN)
    account = await test_connection(api)
    if not account:
        print("Failed to get account.", flush=True)
        return

    iterations = (5 * 60) // 15
    for i in range(iterations):
        try:
            print(f"Iteration {i+1}/{iterations} at {datetime.now()}", flush=True)
            df = await get_candles(account, SYMBOL, TIMEFRAME)
            df = detect_strategy_a(df)
            df = detect_strategy_b(df)
            
            filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = generate_chart(df, filename)
            print(f"Chart generated: {path}", flush=True)
            
            if i == 0:
                with open(os.path.join(OUTPUT_DIR, "first_run_complete.txt"), "w") as f:
                    f.write(path)
                    
        except Exception as e:
            print(f"Error in iteration {i+1}: {e}", flush=True)
            import traceback
            traceback.print_exc()
            
        await asyncio.sleep(15 * 60)

if __name__ == "__main__":
    asyncio.run(main())
