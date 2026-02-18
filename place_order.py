import asyncio
from metaapi_cloud_sdk import MetaApi
import sys

# Configuration
TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYjllMmEwZGM1Y2M1OTM0ODUxMGZjNzNhZGJiMGE3MyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiM2I5ZTJhMGRjNWNjNTkzNDg1MTBmYzczYWRiYjBhNzMiLCJpYXQiOjE3NzEzNjA3ODJ9.LWvwBRCttxN_89L59ibidG_FfeR_Z5J6DSBBC-YKSVqHTE01vszF-2pkbby_eprH8N-A_sCjzUDLC7zj4rIYU1ZdjZQA8nTAg3ocR27j-aov1n3eiCV5MpF5JpMKocqL7SJYbMwEIEb7Rhfs_txMaLDwTqp2TJb36Gil2UnQweS6b5OYpPF1gKFXHIsPvG5_seSZ0vYUPeC5aG67VmR4VQH2W9kxKCyI0Is6bt55xNwl1jRpbuWgs2OcTJFIcN8rWZrKJNX3pZzXOJYJt2vbrzp2prf1DqeouawBO39n45crRhO7Z6m98-4WowgsSHoCtI-4ye1sZ8p3XcJRD1HMxObjIuBC57E7E16jLP90qBm5t4rXIlkSwJXoxUFu_tRo8KsQ_WPhf3MLN4npmZ2B4mc7dfSx7QaIZHx71lBztBShCw3WSD_K-A-UNaiY_9aTy51rSe6avRRSJ-PiC_6Cx8HTjQFtB8BIf_hSw5B_lQAn1WIDcN_e7XZn07Y9UIeAYtz3u8pNXcnkL4UnU64Qx17pX4WSYnsj0VAFp_w5nIy4Ls8aR3ByqqXE5-jujmAVTMSLJHey-Ad0ncIi0l4mHIttvepQyOnES7BpnNMNGUrXFzpKZrPnDUmFyzTcZSBQuh01MF65VTEJPtP2T9wrNib1klB-bSs_OVGOWAVx8aA"
ACCOUNT_ID = "91ed7198-e093-47b8-9940-f73a07ca49e4"
SYMBOL = "EURUSD"
VOLUME = 0.05
TARGET_PRICE = 1.18567

async def main():
    print("Connecting...", flush=True)
    api = MetaApi(TOKEN)
    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        price = await connection.get_symbol_price(SYMBOL)
        current_bid = price['bid']
        current_ask = price['ask']
        print(f"Current {SYMBOL} Price: Bid={current_bid}, Ask={current_ask}", flush=True)
        
        if current_ask < TARGET_PRICE:
            print(f"Placing BUY STOP order at {TARGET_PRICE}...", flush=True)
            result = await connection.create_stop_buy_order(SYMBOL, VOLUME, TARGET_PRICE, 0.0, 0.0)
            print(f"Order Placed: {result['orderId']}", flush=True)
        else:
            print(f"Price ({current_ask}) is already above {TARGET_PRICE}. Using BUY LIMIT instead?", flush=True)
            # Strategy: if price is above, maybe we shouldn't place a stop? 
            # The user said "crosses to the upside", implying it hasn't happened yet.
            # If it's already above, the condition "crosses" might have passed.
            # I'll just report it and not place the order to be safe.
            print("Action required: Verify order type.", flush=True)

    except Exception as e:
        print(f"Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())