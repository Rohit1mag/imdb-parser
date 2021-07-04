import requests
import re 
from bs4 import BeautifulSoup
import pandas as pd


pd.set_option('display.max_columns', None)


def getNamesAndRatings(linkList):
    nameList = []
    ratingList = []
    yearList = []
    mpaRatings = []
    
    for link in linkList:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = 0
        h3s = soup.find_all("h3", "lister-item-header")
        for instance in h3s:
            instance = instance.find("a")
            if not instance.text == "See full summary" and not instance.text == " \n":
                nameList.append(instance.text)
                movies +=1
            else:
                pass
    
        count = 0
        numRatings = 0       
        for instance in soup.find_all('span', class_= re.compile("ipl-rating-star__rating")):
            if not instance.text == "Rate":
                count += 1
                if count % 12 == 1:
                    ratingList.append(float(instance.text))
                    numRatings +=1
        
                    
        for instance in soup.find_all('span', class_ = re.compile("lister-item-year text-muted unbold")):
            if "(20" in instance.text:
                start = instance.text.find("(20", 0, len(instance.text) - 1)
                year = int(instance.text[start+1:start+5])
                yearList.append(year)
        
                 
        for instance in soup.find_all("p", class_=re.compile("text-muted text-small")):
            if instance.find("span", class_ = re.compile("runtime")):
                if instance.find("span", class_ = re.compile("certificate")):
                    instance = instance.find("span", class_= re.compile("certificate"))
                    mpaRatings.append(instance.text)
                else:
                    mpaRatings.append("Not Rated") 
            else:
                pass 
    
    return nameList, ratingList, yearList, mpaRatings

def sortAndMakeIntoDframe(list1, list2, list3, list4):
    zipped = list(zip(list1, list2, list3, list4))
    zipped.sort()
    zipped.reverse()
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    
    for bunch in zipped:
        list1.append(bunch[0])
        list2.append(bunch[1])
        list3.append(bunch[2])
        list4.append(bunch[3])
    
    finalDict = {"Names": list2, "Ratings": list1, "Years": list3, "MPA Rating": list4}
    finalDf = pd.DataFrame(finalDict, columns = ["Names", "Ratings", "Years", "MPA Rating"])
        
    return finalDf

#Main
#2019-13, 2013, 2019, 2018, 2017
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.display.width = 0
imdbLinks = ["https://www.imdb.com/list/ls057563436/", "https://www.imdb.com/list/ls041125816/", "https://www.imdb.com/list/ls047677021/", "https://www.imdb.com/list/ls062009325/", "https://www.imdb.com/list/ls033133511/", "https://www.imdb.com/list/ls071776440/", "https://www.imdb.com/list/ls059824992/", "https://www.imdb.com/list/ls050944621/"]
names, ratings, years, mpa = getNamesAndRatings(imdbLinks)
file5 = open("", "w") #The location where you want to store the table
file5.write(str(sortAndMakeIntoDframe(ratings, names, years, mpa)))







