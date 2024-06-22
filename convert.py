# datasource : https://data.gov.tw/dataset/33305
# data is stored in 電力座標, 虎子山二分帶, TWD97
# 使用 PROJ 轉換成WGS84


#橫麥卡托(Transverse Mercator)系：

# TM2（TWD97，中央經線121度）(適用臺灣本島，民國87年之後施行迄今) ＝> EPSG:3826
# TM2（TWD97，中央經線119度）(適用澎湖金門馬祖，民國87年之後施行迄今) ＝> EPSG:3825
# TM2（TWD67，中央經線121度）(適用臺灣本島，民國69年之後施行) ＝> EPSG:3828（內建參數有誤，需自行修正）
# TM2（TWD67，中央經線119度）(適用澎湖金門馬祖，民國69年之後施行) ＝> EPSG:3827
# TM3（TWD67，中央經線121度）(適用臺灣本島及澎湖，民國58年之後短暫使用) ＝> 無EPSG代號，需自行定義

# 經緯度(Latitude-Longitude)系：

# WGS84經緯度（全球性資料，如：GPS） ＝> EPSG:4326
# TWD97經緯度（國土測繪中心發佈全國性資料）＝> EPSG:3824
# TWD67經緯度（部分地籍圖圖解數化成果）＝> EPSG:3821
# 虎子山經緯度（日治時期陸測地形圖） ＝> EPSG:4236

# 其他：

# Spherical Mercator（圖磚、WMTS，如：Google Map） ＝> EPSG:3857
# 虎子山UTM zone 51N（中美合作軍用地形圖） ＝> EPSG:3829


# source : https://service.taipower.com.tw/data/opendata/apply/file/d077006/all.csv

from tqdm.auto import tqdm
import time
from pyproj import Transformer
import csv



filename = 'all.csv'
filename2 = 'output.csv'
transformerph = Transformer.from_crs('epsg:3825','epsg:4326')  #澎湖金馬 TWD97 to WGS84
transformer = Transformer.from_crs('epsg:3826','epsg:4326')  #TWD97 to WGS84
start = time.time()

with open(filename, mode='r',newline = '') as file:
    reader = csv.reader(file)
    header = next(reader)
    data  = [row for row in reader]

print (f'total {len(data):,} poles')
header.extend(['WGS84_lat','WGS84_lon'])

for row in tqdm(data):
#"縣市","行政區","鄉里","圖號座標","形式","桿號","TWD_97_X","TWD_97_Y"
    if row[0] in ('澎湖縣','連江縣','金門縣'):
        lat, lon = transformerph.transform(row[-2], row[-1])
    else:
        lat, lon = transformer.transform(row[-2], row[-1])

    row.extend([lat, lon])
    
with open(filename2, mode='w',newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)
end = time.time()



print (f'done. took {(end - start)/60:,.1f} min')
