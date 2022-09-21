import sqlite3
import requests
import bs4
# import numpy as np
import math
import os.path
BASE_DIR = os.path.dirname(os.path.abspath('/Users/davidpayne/Desktop/books.db'))
db_path = os.path.join(BASE_DIR, "books.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# formats the book list
def makeBookString(string):
    list = str(string).split(">")
    book = list[2]
    book = book[:-4]
    if "&amp;" not in book:
        return book 
    else:
        splitList = book.split()
        x = int(splitList.index('&amp;'))
        splitList[x] = "&"
        str1 = " "
        return str1.join(splitList)
    
    
def bookTypeString(string):
    list = str(string).split(">")
    x = list.index('\n<li class="format"')
    type = list[x+1]
    type = type[:-4]
    return type

# formats the author list
def makeAuthorString(string):
    list = str(string).split(">")
    check = list[4]
    if check == "by <span":
        author = list[5]
        author = author[:-6]
    else:
        author = "n/a"
    return author

def makeCopyString(string):
    list = str(string).split(">")
    copy = list[12]
    copy = copy[:-6]
    return copy

def publisherString(string):
    list = str(string).split(">")
    x = list.index('\n<li class="format"')
    publisher = list[x+3]
    publisher = publisher[:-4]
    if "&amp;" not in publisher:
        return publisher # & turns into &amp; when printed fix that later
    else:
        splitList = publisher.split()
        x = int(splitList.index('&amp;'))
        splitList[x] = "&"
        str1 = " "
        return str1.join(splitList)
        
        

def ISBNString(string):
    list = str(string).split(">")
    x = list.index('\n<li class="format"')
    isbn = list[x+9]
    isbn = isbn[:-4]
    return isbn

def dateString(string):
    list = str(string).split(">")
    x = list.index('\n<li class="format"')
    date = list[x+13]
    date = date[:-4]
    date = date[4:]
    return date

def priceString(string):
    list = str(string).split(">")
    price = list[5]
    price = price[:-6]
    return price
        


numberOfBooks = int(input("enter number of books present on website: "))
numberOfPages = numberOfBooks/100
books, pages = math.modf(numberOfPages)
books = books*100
books = int(round(books))
pages = int(pages)

a = 0

for i in range(pages):
    a+=1
    link = "https://www.gardners.com/Search/KeywordAnonymous/Books?Keyword=+&fq=14120&searchPreferences=0&pg=" + str(a)
    ##sets up beautiful soup
    res = requests.get(link)
    type(res)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    type(soup)
    # calls page details loops
    if i != pages:
        x = 100
    else:
        x = books

    for i in range(x):
        x = 5*i + 44
        booksString = soup.find_all("div")[x] #44 gets the title, author, number in stock, format, publisher, isbn and date published price in 47
        book = makeBookString(booksString)
        author = makeAuthorString(booksString)
        copy = makeCopyString(booksString)
        type = bookTypeString(booksString)
        publisher = publisherString(booksString)
        isbn = ISBNString(booksString)
        date = dateString(booksString)
        booksString = soup.find_all("div")[x+4]
        price = priceString(booksString)
        list = [book, author, price, isbn, copy, type, publisher, date]
        cursor.execute("insert into book values(?,?,?,?,?,?,?,?)",list)
    connection.commit() 

connection.close()




# divisions = (soup.find_all("div"))
# print(divisions.contents)
# print(soup.get_text())


# first data number 44 and 48
# second data number 49 and 53
# last case for this do an if not present loop on title 

