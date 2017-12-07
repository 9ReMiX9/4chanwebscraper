import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=Graphics%20Card'

#Opening connection and grabbing page
uClient = uReq(my_url)

#Content to variable
page_html = uClient.read()

#Closes connection
uClient.close()

#Finds all containers
page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("div", {"class":"item-container"})

filename = "products.csv"
f = open(filename, "w")

headers = "brand, product_name, shipping\n"

f.write(headers)


for container in containers:
    brand = container.div.div.a.img["title"] #Brand

    title_container = container.findAll("a", {"class":"item-title"}) #Getting Title
    title = title_container[0].text

    shipping_container = container.findAll("li", {"class":"price-ship"}) #Shipping
    shipping = shipping_container[0].text.strip()

    print("brand: "     + brand)
    print("title: "     + title)
    print("shipping: "  + shipping)

    f.write(brand + "," + title.replace(",","|") + "," + shipping + "\n")

f.close()