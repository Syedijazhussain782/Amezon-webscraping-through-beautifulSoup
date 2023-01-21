from bs4 import BeautifulSoup as bs       # use to prettify data
import requests   #use to get data from webpage
import pandas as pd

link= "https://www.amazon.in/OnePlus-Mirror-Black-128GB-Storage/product-reviews/B07DJHV6VZ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
url=requests.get(link)
soup=bs(url.content,'html.parser')       # change the  dataa to html parser.
soup.prettify()                         # clean the dataa and prettify it.
# print(soup)


####################    NAMES  #################################
names=soup.findAll('span',class_="a-profile-name")        #will find all  the name in a class
#print(names)
cust_name=[]
for name in range(0,len(names)):
  cust_name.append(names[name].getText())      #it will append it to a list
#print(cust_name)     #print all the names in a list

cust_name.pop(0)
cust_name.pop(0)
#print(cust_name)



#####################   REVIEWSSSSS   #########################

reviews=soup.findAll('a',class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")
#print(reviews)
revi=[]
for i in range(0,len(reviews)):
  revi.append(reviews[i].getText())  #it will append it to a list
#print(revi)

revi[:]=[i.lstrip('\n')for i in revi ]      #will remmove "\n" from left side
revi[:]=[i.rstrip('\n')for i in revi ]      ##will remmove "\n" from left side
#print(revi)

##################### STAR REVIEWS   #########################

star=soup.findAll('i',class_="review-rating")
#print(star)
starlist=[]
for i in range(0,len(star)):
    starlist.append(star[i].getText())
#print(starlist)
starlist.pop(0)
starlist.pop(5)
#print(starlist)


df=pd.DataFrame()
df['customername']=cust_name
df['reviews']=revi
df['stars']=starlist

print(df)

df.to_csv(r'E:\reviews.csv' ,index=True )
