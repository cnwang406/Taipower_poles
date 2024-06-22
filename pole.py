#
# draw poles, with folium
#
# all Taiwan's poles > 1M. will hang. so draw only at small area.
#


import folium
import pandas as pd
from pyproj import Transformer
from tqdm import tqdm
import time

#hcc = https://service.taipower.com.tw/data/opendata/apply/file/d077010/Hsinchu_City.csv
# 
file = r'hcc.csv'
outputHTML = 'hcc.html'
df = pd.read_csv(file)
print (f'total {len(df):,} poles')
transformer = Transformer.from_crs('epsg:3826','epsg:4326')  #TWD97 to WGS84
transformerph = Transformer.from_crs('epsg:3825','epsg:4326')  #澎湖金馬 TWD97 to WGS84

#"縣市","行政區","鄉里","圖號座標","形式","桿號","TWD_97_X","TWD_97_Y"
home = [24.78903, 120.99645]   # NCTU
m = folium.Map(location = home)
cnt = 0  # draw only ? poles. 0 == all
start = time.time()

for row in tqdm(df.itertuples(), total = len(df)):
    if row.縣市 in ('澎湖縣','連江縣','金門縣'):
        lat, lon = transformerph.transform(row.TWD_97_X, row.TWD_97_Y)
    else:
        lat, lon = transformer.transform(row.TWD_97_X, row.TWD_97_Y)

    name = row.桿號

    folium.CircleMarker(location=[lat, lon],radius=0.5,
                        color="cornflowerblue",stroke=False,
                        fill=True,fill_opacity=1.0,opacity=0.7).add_to(m)
    cnt -= 1
    if cnt == 0:
        break

# draw NCTU
folium.CircleMarker(
    location=home,
    radius=3,
    color="red",
    stroke=False,
    fill=True,
    fill_opacity=1.0,
    opacity=0.7).add_to(m)
m.save(outputHTML)

print (f'total {len(df):,} poles transferred, took {(time.time() - start) / 60:,.1} min')

print ('done, saved at ',outputHTML)
m.show_in_browser()