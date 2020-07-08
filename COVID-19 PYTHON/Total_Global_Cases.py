import geopandas as gpd
import pandas as pd
import mapclassify
import PIL
import io

data=pd.read_csv("/Users/vineetkargeti/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
data.head(10)

#grouping the data for country
data=data.groupby('Country/Region').sum()
data.head(20)

#Drop lat and lon columns
data=data.drop(columns=['Lat','Long'])
data.tail(20)
data_transposed.plot(y=['Russia','India','Brazil'],use_index=True,figsize=(5,5))

#Reading the world map shape file
world=gpd.read_file(r'/Users/vineetkargeti/Downloads/drive-download-20200707T122128Z-001/World_Map.shp')
world.plot(figsize=(14,14))

world.replace('Viet Nam','Vietnam',inplace=True)
world.replace('Brunei Darussalam','Brunei',inplace=True)
world.replace('Cape Verde','Cabo Verde',inplace=True)
world.replace('Czech Republic','Czechia',inplace=True)
world.replace('Swaziland','Eswatini',inplace=True)
world.replace('Iran (Islamic Republic of)','Iran',inplace=True)
world.replace('Korea, Republic of','Korea, South',inplace=True)
world.replace("Lao People's Democratic Republic",'Laos',inplace=True)
world.replace('Libyan Arab Jamahiriya','Libya',inplace=True)
world.replace('Republic of Moldova','Moldova',inplace=True)
world.replace('The former Yugoslav Republic of Macedonia','North Macedonia',inplace=True)
world.replace('Syrian Arab Republic','Syria',inplace=True)
world.replace('Taiwan','Taiwan*',inplace=True)
world.replace('United Republic of Tanzania','Tanzania',inplace=True)
world.replace('United States','US',inplace=True)
world.replace('Democratic Republic of the Congo','Congo (Kinshasa)',inplace=True)
world.replace('Congo','Congo (Brazzaville)',inplace=True)
world.replace('Palestine','West Bank and Gaza',inplace=True)


#Checking the names of the countries in Shape file from John Hopkins File
for index,row in data.iterrows():
    if index not in world['NAME'].tolist():
        print(index+' :is not in the list')
    else:
        pass


#merging data with world
merge=world.join(data,on='NAME',how='right')
merge
image_frames=[]


image_frames=[]

#converting columns to list
for dates in merge.columns.tolist()[2:]: #the range is column
    ax=merge.plot(column=dates,
              cmap='OrRd',
              figsize=(10,10),
              legend=True,
              scheme='user_defined',
              classification_kwds={'bins':[10,20,50,100,500,1000,5000,10000,500000]},
              edgecolor='black',
              linewidth=0.4)
#cmap=colormap #scheme to define the color intervals
#map title
    ax.set_title('Total Confirmed Corona Virus Cases '+dates,fontdict={'fontsize':20},pad=12.5)
#Move the axes
    ax.set_axis_off()
#Move the legend
    ax.get_legend().set_bbox_to_anchor((0.18,0.16))
    img=ax.get_figure()
    f=io.BytesIO()
    img.savefig(f,format='png',bbox_inches='tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))

#Creating a GIF file
image_frames[0].save('Dynamic Covid 19 Trial.gif',
                     format='GIF',
                     append_images=image_frames[1:],
                     save_all=True,
                     duration=600,
                     loop=1)
f.close()
