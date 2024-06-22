# 
# For large amount poles, draw on PNG to prevent file too large
#
# use basemap to draw Taiwan

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from tqdm.auto import tqdm
import time
from PIL import Image, ImageDraw
import pandas as pd

filename = 'taiwan_mini.png'
filename2 = 'taiwan_mini_poles.png'
locFilename = 'output.csv'
home = [24.78903, 120.99645]   # NCTU

fig, ax = plt.subplots(figsize = (10,7))


# draw background basemap.png, based on poles covered area.
def taiwanBasemap(llcrnrlat, llcrnrlon, urcrnrlat, urcrnrlon):
    m = Basemap(projection='cyl', llcrnrlat=llcrnrlat, llcrnrlon=llcrnrlon, urcrnrlat= urcrnrlat, urcrnrlon=urcrnrlon, resolution= 'f')
    m.drawcoastlines()
    m.drawrivers()
    plt.savefig(filename, format='png', dpi=300,  bbox_inches = 'tight', pad_inches = 0)


# convert lat, log (TWD97) to X,Y of background map.
def wgsToXY(lat, lon, imgW, imgH,llcrnrlat, llcrnrlon, urcrnrlat, urcrnrlon):
    latRange = urcrnrlat - llcrnrlat
    lonRange = urcrnrlon - llcrnrlon
    x = (lon - lllon) * imgW / lonRange
    y = (urcrnrlat - lat) * imgH / latRange
    return int(x), int(y)


print (f'Reading poles locations :{locFilename}')
df = pd.read_csv(locFilename)

lllat,lllon,urlat,urlon = df['WGS84_lat'].min()-0.1,df['WGS84_lon'].min()-0.1,df['WGS84_lat'].max()+0.1,df['WGS84_lon'].max()+0.1
print (f'poles distributes from [{lllat},{lllon}]~[{urlat},{urlon}]')
print (f'total {len(df):,} poles')

# draw background png.
print (f'\ncreating basemap :{filename}')
taiwanBasemap(llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat= urlat, urcrnrlon=urlon)

bkg = Image.open(filename)
draw = ImageDraw.Draw(bkg)
imgW = bkg.width
imgH = bkg.height
print (f'\nimage = {imgW}x{imgH} pixels')

print (f'\nmarking poles to image')
#投縣,中寮鄉,和興村,K7694GD36,水泥桿,草殼分#7分21,232267.50498,2647157.5026,23.92887769458353,120.82580625652776
for row in tqdm(df.itertuples(), total = len(df)):
    lat,lon = float(row.WGS84_lat),float(row.WGS84_lon)
    x, y = wgsToXY(lat, lon, imgH=imgH, imgW = imgW,llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon)
    draw.ellipse((x-1,y-1,x,y), fill='blue', outline= 'blue')

# mark NCTU
x, y = wgsToXY(home[0] , home[1], imgH=imgH, imgW = imgW, llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon)
draw.ellipse((x-2,y-2,x+2,y+2), fill='red', outline= 'red')
print ('done')
bkg.save(filename2)
bkg.show()
