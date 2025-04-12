import requests
import pandas as pd

# 設定API金鑰
API_KEY = 'A0V288MZ5ODXY44J'
BASE_URL = 'https://www.alphavantage.co/query'

# 取得歷史股價資料並儲存為 CSV
def get_historical_stock_data(stock_symbol, start_date, end_date, output_file='api.csv'):
    url = BASE_URL
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': stock_symbol,
        'outputsize': 'full',  # 取得完整資料
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        historical_data = data["Time Series (Daily)"]
        dates = list(historical_data.keys())
        dates.sort(reverse=True)

        # 過濾日期範圍的資料
        filtered_data = {
            date: historical_data[date] for date in dates if start_date <= date <= end_date
        }

        # 將資料轉為 DataFrame
        df = pd.DataFrame.from_dict(filtered_data, orient='index')
        df.index.name = 'Date'
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

        # 轉換資料型態
        df = df.astype({
            'Open': float,
            'High': float,
            'Low': float,
            'Close': float,
            'Volume': int
        })

        # 儲存為 CSV
        df.to_csv(output_file)
        print(f"已成功儲存資料")
    else:
        print("錯誤，無法取得資料")

# 主程式
def main():
    stock_symbol = input("請輸入股票代號：")
    start_date = input("請輸入開始日期（格式：YYYY-MM-DD）：")
    end_date = input("請輸入結束日期（格式：YYYY-MM-DD）：")

    get_historical_stock_data(stock_symbol, start_date, end_date)

if __name__ == "__main__":
    main()