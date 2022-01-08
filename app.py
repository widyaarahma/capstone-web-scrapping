from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here 
table1 = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
row = table1.find_all('td')

row_length = len(row)

#insert the scrapping process here
tanggal_temp = []
hari_temp = []
harga_temp = []

for i in range(0, row_length):
    
    #get tanggal
    for i in range(0, row_length, 4):
        tanggal = tanggal_temp.append(row[i].get_text())
    
    #get hari
    for i in range(1, row_length, 4):
        hari = hari_temp.append(row[i].get_text())
    
    #get harga
    for i in range(2, row_length, 4):
        harga = harga_temp.append(row[i].get_text())

#change into dataframe

#insert data wrangling here
df = pd.DataFrame()
df['Tanggal'] = tanggal_temp
df['Hari'] = hari_temp
df['Harga'] = harga_temp
df['Harga'] = df['Harga'].apply(lambda x: x.replace('IDR', ''))
df['Harga'] = df['Harga'].apply(lambda x: x.replace(',', ''))
df['Harga'] = df['Harga'].astype('float')
df['Tanggal'] = df['Tanggal'].astype('datetime64')
df =df.set_index('Tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Harga"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (9,3)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)