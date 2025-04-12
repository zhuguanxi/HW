#static

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.nationalgeographic.com/photography/photo-of-the-day/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

#抓取標題
title_meta = soup.find("meta", property="og:title")
title = title_meta["content"].strip() if title_meta else "無標題"

#抓取說明
desc_meta = soup.find("meta", attrs={"name": "description"})
description = desc_meta["content"].strip() if desc_meta else "無內文"

#抓取圖片連結
img_meta = soup.find("meta", property="og:image")
img_url = img_meta["content"] if img_meta else "無圖片"

#輸出成CSV
df = pd.DataFrame([{
    "標題": title,
    "說明": description,
    "圖片連結": img_url
}])
df.to_csv("static.csv", index=False, encoding="utf-8-sig")

print("已成功抓取資料")
