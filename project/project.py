#remember to get your oauth token before starting the program
#obtain your oauth token here: https://developer.spotify.com/console/get-new-releases/?country=AX&limit=10&offset=5
import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#crawl for the countries spotify are available in
url_spotify = 'https://support.spotify.com/us/using_spotify/getting_started/full-list-of-territories-where-spotify-is-available/'
r = requests.get(url_spotify)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text,'html.parser')
#path example
#body > div > div > div.container > div.row > div.col-sm-9.col-md-7.col-md-offset-1.article-elements.content > div.article-content > table > tbody > tr:nth-child(1) > td:nth-child(2)
crawl_spotify = soup.find_all("td")
spotify_available = list()
count1 =0
#store the countries obtained in spotify_available
for item in crawl_spotify:
#item example
#<td colspan="1" rowspan="1">Algeria, Egypt, Morocco, South Africa, Tunisia.</td>
  if count1%2!=0:
    #according to the format, remove '.'
    temp = item.text[:-1]
    #exist countries like South Africa-->split() is not feasible
    #store the content before ','
    #find(',')+2 since we are removing ', '
    while ',' in temp:
      spotify_available.append(temp[:temp.find(',')].lower())
      temp = temp[temp.find(',')+2:]
    spotify_available.append(temp.lower())
  count1+=1
#print(spotify_available)

#crawl for country code and country name
url_code = 'https://countrycode.org/'
code = requests.get(url_code)
code.encoding = 'utf-8'
soup = BeautifulSoup(code.text,'html.parser')
#path example
#body > div.container > div.visible-sm.visible-xs > div.bootstrap-table > div.fixed-table-container > div.fixed-table-body > table > tbody > tr:nth-child(1) > td.country-col > a
crawl_country = soup.find_all("td")
country_code = list()
country_name = list()
count2 =0
#print(crawl_country[6])#0,6,2,8...
for item in crawl_country:
#item example
#<a href="/afghanistan">Afghanistan</a>
  if count2%6==0:
    country_name.append(item.text.lower())
  elif (count2-2)%6==0:
    country_code.append(item.text.split()[0])
  count2+=1
#combine to list together interactively
name_to_code = dict(zip(country_name,country_code))
code_to_name = dict(zip(country_code,country_name))
#store input as country
country1 = input("Enter the first country code(alpha-2) or country name of the country which you want to compare : ")
country2 = input("Enter the second country code(alpha-2) or country name of the country which you want to compare : ")
#first API: request for the new releases of spotify
#***remember to change oauth token before starting
auth_token = 'BQDPE7c5AqYleBknO6j-N77bm9snuXI1aiDlGzusQgTLeIwsTEMEq_ufh1D4ynh2JQ5RIaYWF0WhYAHgDtaBB4NSEoi0NhzTAULmI2K4nqOT-thCcPfUX5DqVB6_UrC5PDoJclZlm1849YcuOfWW3Rjv4QOjE6ze8bl5hAY'
hed = {'Authorization': 'Bearer ' + auth_token}

#import for later drawing pie chart
import matplotlib
import matplotlib.pyplot as plt

#check if country is a country_name
#if yes, change it to the corresponding country code
#if no, convert it to upper case for later determine of country code
if country1.lower() in country_name:
  country1 = name_to_code[country1.lower()]
else:
  country1 = country1.upper()

if country2.lower() in country_name:
  country2 = name_to_code[country2.lower()]
else:
  country2 = country2.upper()

#import for later output table
from prettytable import PrettyTable

#after adjustment above, if country is proper it will exist in country_code
#if country is still improper, follow else
if (country1 and country2) in country_code:
  #change country code to country name and check if spotify is available in the country
  #if no, follow else
  if (code_to_name[country1] and code_to_name[country2]) in spotify_available:
    #request for the new release by API
    response1 = requests.get('https://api.spotify.com/v1/browse/new-releases?country='+country1+'&limit=10&offset=5', headers=hed)
    response2 = requests.get('https://api.spotify.com/v1/browse/new-releases?country='+country2+'&limit=10&offset=5', headers=hed)
    #response in json
    info1 = response1.json()
    info2 = response2.json()
    release1 = info1['albums']['items']
    release2 = info2['albums']['items']
    album_type1 = list()
    album_type2 = list()
    artist_name1 = list()
    artist_name2 = list()
    album_name1 = list()
    album_name2 = list()
    category1 = dict()
    category2 = dict()
    #store album type, album name, and artist respectively
    for a in release1:
      album_type1.append(a['album_type'])
      #store type and amount of album type in category
      if a['album_type'] not in category1:
        category1.update({a['album_type']:1})
      else:
        category1[a['album_type']]+=1
      album_name1.append(a['name'])
      artist1 = a['artists']
      for b in artist1:
        artist_name1.append(b['name'])
    for c in release2:
      album_type2.append(c['album_type'])
      #store type and amount of album type in category
      if c['album_type'] not in category2:
        category2.update({c['album_type']:1})
      else:
        category2[c['album_type']]+=1
      album_name2.append(c['name'])
      artist2 = c['artists']
      for d in artist2:
        artist_name2.append(d['name'])
    #print(album_type)
    #print(album_name)
    #print(artist_name)
    #print(category2)

    #second API: requests for the information of country(capital,name)
    capital1 = requests.get("https://restcountries.eu/rest/v2/alpha/"+country1)
    capital2 = requests.get("https://restcountries.eu/rest/v2/alpha/"+country2)
    data1 = capital1.json()
    data2 = capital2.json()

    #pie chart drawing
    fig = plt.figure()
    #category.values() decide proption of each category.keys()
    #Equal aspect ratio ensures that pie is drawn as a circle.
    ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
    ax1.pie(category1.values(), labels=category1.keys(), autopct='%1.1f%%',shadow=False, startangle=90)
    ax1.axis('equal')
    ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
    ax2.pie(category2.values(), labels=category2.keys(), autopct='%1.1f%%',shadow=False, startangle=90)
    ax2.axis('equal')
    #set the title for the chart
    #if the title is too long, break it into two lines
    title1 = "Album type of "+data1["name"]
    title2 = "Album type of "+data2["name"]
    if len(title1)>30:
      title1 = "Album type of "+'\n'+data1["name"]
    if len(title2)>30:
      title2 = "Album type of "+'\n'+data2["name"]
    ax1.set_title(title1)
    ax2.set_title(title2)

    #output the information from new release in table
    tb1 = PrettyTable()
    #set the title for the table, title require installing PTable
    tb1.title = 'top 10 latest released albums of '+data1["name"]+'(capital : '+data1["capital"]+')'
    tb1.field_names = ["", "Artist", "Album Name","Album Type"]
    #add row to the table corresponding to each field
    for n in range(10):
        tb1.add_row([(n+1), artist_name1[n], album_name1[n],album_type1[n]])

    tb2 = PrettyTable()
    tb2.title = 'top 10 latest released albums of '+data2["name"]+'(capital : '+data2["capital"]+')'
    tb2.field_names = ["", "Artist", "Album Name","Album Type"]
    #add row to the table corresponding to each field
    for m in range(10):
        tb2.add_row([(m+1), artist_name2[m], album_name2[m],album_type2[m]])

    #print the table
    print(tb1)
    print('\n')
    print(tb2)
    #show the pie chart
    plt.show()
  else:
    print('Spotify is not available in the country you entered.')
else:
  print('The country code or name you entered is incorrect.')