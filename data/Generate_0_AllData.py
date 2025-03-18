import os
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
from datetime import datetime

# Binance API 클라이언트 설정 (API 키 & 시크릿 입력 필요)
client = Client(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')

# 데이터를 저장할 디렉토리 설정
base_dir = './BTC_data'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 데이터 수집 시작 날짜 및 종료 날짜 (2018년 1월1일부터 오늘까지)
start_date = datetime(2018, 1, 1)
end_date = datetime.now()

# 원하는 봉 간격 리스트 (원하는 기간을 설정할 수 있음)
# ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

# 데이터 수집 및 저장
for interval in intervals:
    save_dir = os.path.join(base_dir, interval)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Fetching {interval} data...")

    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

    # 봉 데이터 요청
    bars = client.get_historical_klines('BTCUSDT', interval, start_date_str, end_date_str)

    # 데이터프레임 변환
    btc_df = pd.DataFrame(bars, columns=[
        'Open_time', 'open', 'high', 'low', 'close', 'volume', 'Close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    # 필요한 컬럼만 선택 및 타임스탬프 변환
    btc_df = btc_df[['Open_time', 'open', 'high', 'low', 'close', 'volume']]
    btc_df['Open_time'] = pd.to_datetime(btc_df['Open_time'], unit='ms')
    btc_df.set_index('Open_time', inplace=True)
    
    # 데이터 타입 변환
    btc_df[['open', 'high', 'low', 'close', 'volume']] = btc_df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    # CSV 저장
    filename = f'{save_dir}/BTC_{interval}.csv'
    btc_df.to_csv(filename, float_format='%.2f')
    
    print(f"Data saved: {filename}")

print("모든 데이터 수집 완료!")
