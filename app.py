import streamlit as st
from metaapi_cloud_sdk import MetaApi
import asyncio
import os

# --- BOT CONFIGURATION ---
TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1NzMxMWZkMWIyZDBiYWRiZTU2Nzc4OTBhODhiZjBkZCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiNTczMTFmZDFiMmQwYmFkYmU1Njc3ODkwYTg4YmYwZGQiLCJpYXQiOjE3NzcyMTQ3MzZ9.UZt1kc1dhpHlO5tJqJ1DjLb65aP61lxsAd7tLkbKTyaki4ssJUe5anN75SfbKAWdxM_urQQGEiuaesChwAWxn9a-T3lvNHzg5hykrx04VAgtYTcA4sHBLe_2Jyxp4I4RvgkV59_Z7vgF00yFT_ZK0VzIoAgGCqKGyEZ-yGAJNWclrN58qjiEAdv6aE1Km3giohH_5DkUIkrNEjLPSMQYgQSl-fqv0HitWBvQMCZ6o2m0tGb-rawQtnIUEyvztwLUglYbxLMCYeOSBvNsbB44nM39xdDUIFe8OBnzDix4YepwH-4s2cAW2PBnBVpOVP6ChIf0GNsWjpUR2sk_QCoGmLica6BiRKj-_doUClQwZ29jZJgFlPyRY0qZn-62jJZh0a6FheAkKtXe0SKPQo6OmDX9F7KbPgvqDwxG7-EES5QtZW8V4mMr7zRe2LHGZTfER_LLFyBS7KDxPkIIjmpVwSH1kKAKyfjBqbrF8M85PiRjyGdHJS6mpK0DwlcF2ikmHx_kbKx-5MkN60e9B0dm_v5RxwX-RdlLyHrOYmtoA4_2VMDPxk6f-VwWO8k-PM5-EPmJ3_wwf-Ig_wZGvogWPwKp-TZdQzm-bmsLCEARE27X1tHz4Xx7HKUKqsZLRadJLskWRxcBT0HvIM-a12b62aeN3LkLSWVoGi8Bx1NMZb0"
ACCOUNT_ID = "5592431c-6c0d-4e7d-8c72-fc8705f3116a"
LOT_SIZE = 0.01
PROFIT_TARGET = 0.20  # $0.20 Profit Exit

st.title("🚀 Christine's $10 Scalper Bot")
st.write("Status: Connecting to MetaAPI...")

async def run_bot():
    api = MetaApi(TOKEN)
    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        await account.wait_connected()
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        st.success("✅ Connected to FBS/Deriv Live!")
        
        while True:
            # Check current open positions
            positions = await connection.get_positions()
            
            for pos in positions:
                # Emergency Profit Guard: Close if profit > $0.20
                if pos['profit'] >= PROFIT_TARGET:
                    st.warning(f"Closing trade {pos['id']} for ${pos['profit']} profit!")
                    await connection.close_position(pos['id'])
            
            # Simple Scalper Logic: Buy if no trades open (Placeholder for your strategy)
            if len(positions) == 0:
                st.write("Scanning for Liquidity Sweep...")
                # Here we would add the logic for your 15m sweep
                # For now, it stays ready to execute.
            
            await asyncio.sleep(5) # Watch every 5 seconds
            
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Start Robot"):
    asyncio.run(run_bot())
