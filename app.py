# import necessary Bookraries
import os
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import requests

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://kcgroityanbzbh:9628ada64f272d28fa11b1fffc6c23120e669ef39ffa0e094156605e0ad7c256@ec2-18-206-84-251.compute-1.amazonaws.com:5432/d4mqhu1hofe8vr"

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@localhost:5432/BookShare"
db = SQLAlchemy(app)
db.create_all()

from models import *

""" #session connection to database
    ## sqlalchemy.ORM is not working so using sessions instead.
connection_string = 'postgres:postgres@localhost:5432/BookShare'
engine = create_engine(f'postgresql://{connection_string}')
Base=automap_base()
Base.prepare(engine, reflect=True)

Book= Base.classes.library
owner_details=Base.classes.owner
book_details= Base.classes.book

session=Session(engine) """

# global variables used in the code
bookTitle=""
books=[]
books_owner=[]

# create route that renders index.html template
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

#navigation route
@app.route("/bookSearch", methods=["GET", "POST"])
def Find_Books():
    
    return render_template("Find.html")

# Query the database and send the jsonified results
@app.route("/getBook", methods=["GET", "POST"])
def getBook():

    global books
    books=[]
    """ global Book
    global session """

    if request.method == "POST":
        
        bookTitle = request.form["title"].lower()
        
        #query database and filter book results
        books_db = db.session.query(Book.image_url, Book.title, Book.authors, Book.average_rating, Book.sub_category, Book.num_pages,Book.isbn).\
                filter(func.lower(Book.title).like(f'%{bookTitle}%')).limit(10).all()
        
        for book in books_db:
            dict_book = {
                "title" : book.title,
                "author":book.authors,
                "average_rating":book.average_rating,
                "image_url": book.image_url,
                "sub_category":book.sub_category,
                "num_pages":book.num_pages,
                "isbn":book.isbn   
            }
            books.append(dict_book)
        
        db.session.close()

        return redirect("/bookSearch")

    if request.method== "GET":

        #query database for book results
        books_db = db.session.query(Book.image_url, Book.title, Book.authors, Book.average_rating, Book.sub_category, 
                                    Book.num_pages,Book.isbn).limit(20).all()
 
        for book in books_db:
            dict_book = {
                "title" : book.title,
                "author":book.authors,
                "average_rating":book.average_rating,
                "image_url": book.image_url,
                "sub_category":book.sub_category,
                "num_pages":book.num_pages,
                "isbn":book.isbn      
            }
            books.append(dict_book)
        
        db.session.close()

        return render_template("Library.html")

#################################################################################################################
# ###################         bookshare page and Owner Details    #################################################
###################################################################################################################

#navigation route
@app.route("/bookShare", methods=["GET", "POST"])
def Share_Books():
    
    return render_template("Share.html")

@app.route("/getbooks_share", methods=["GET", "POST"])
def OwnerBooks():
    if request.method == "POST":
        bookTitle = request.form["title"]

        #Googlebooks API connection
        from config import google_api_key

        params={'key':google_api_key,
            'maxResults':5}

        url= f'https://www.googleapis.com/books/v1/volumes?q={bookTitle}'
        response = requests.get(url, params).json()

        global books_owner
        books_owner=[]
        
        #Extracting required information from Google books API
        results=response['items']
        for item in results:
            try:
                book={
                    'image_url':item['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else " ",
                    'id_book': item['id'],
                    'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else " ",
                    'category/genre':item['volumeInfo']['categories'] if 'categories' in item['volumeInfo'].keys() else " ",
                    'authors':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else " ",
                    'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else " ",
                    'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else " ",
                    'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else " ",
                    'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else " ",
                    'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else " "     
                }
                
            except:
                book = {'id_book': 'not found'}
        #add conditional if book not in Books table, add the new book

            books_owner.append(book)


    return render_template("Share.html")

@app.route("/api/sharebook_results")
def sharebook_results():

    global books_owner
    dict_books=[]
    
    for book in books_owner:

            dict_book = {
                "image_url": book['image_url'],
                 "title" : book['title'],
                 "author":book['authors'],
                "id" : book['id_book']
                 }
            dict_books.append(dict_book)
    
    data= jsonify(dict_books)
    books_owner=[]

    return data

@app.route("/getuserinputs/<isbn>", methods=["GET", "POST"])
def ShareForm(isbn):
    title=""
    book=""
    items= db.session.query(Book.title, Book.image_url,Book.authors, Book.average_rating, Book.reviews_count).filter(Book.isbn==isbn).all()

    for item in items:
        title=item.title
        author=item.authors
        rating=item.average_rating
        reviews=item.reviews_count
        image=item.image_url

    book={"title":title,
            "isbn":isbn,
            "image":image,
            "author":author,
            "rating":rating,
            "reviews":reviews}
       
    return render_template("Share_Form.html",data=book)

@app.route("/getownerdetails/<isbn>", methods=["GET", "POST"])
def OwnerDetails(isbn):
    title=""
    #query database to get the book details
    book= db.session.query(Book.title, Book.image_url,Book.authors, Book.average_rating, Book.reviews_count).filter(Book.isbn==isbn).all()
    
    #query database to get all the owners for the above book
    owners=db.session.query(Owner.owner_name, Owner.owner_email, Owner.contact_details, Owner.location,Owner.lat, Owner.lon).\
            filter(Owner.isbn==isbn).all()
    
    listOwners = []
    for owner in owners:
        dict_owner = {
            "name":owner.owner_name,
            "email" : owner.owner_email,
            "contact_details" : owner.contact_details,
            "location": owner.location,
            "lat" : owner.lat,
            "lon" : owner.lon  
        }
        listOwners.append(dict_owner)
    
    for item in book:
        title=item.title
        author=item.authors
        rating=item.average_rating
        reviews=item.reviews_count
        image=item.image_url

    global books
    books={"title":title,
            "isbn":isbn,
            "image":image,
            "author":author,
            "rating":rating,
            "reviews":reviews,
            "owners":listOwners,
            "similar_books":similar_books}
        
    return render_template("Owner_Details.html",data=books)


# Query the database to store owner details
@app.route("/send", methods=["GET", "POST"])
def send():

    if request.method == "POST":
        title = request.form["title"]
        isbn=request.form['isbn']
        owner_name= request.form["name"]
        owner_email = request.form["email"]
        location= request.form["location"]
        rating = request.form["rating"]
        review= request.form["review"]
        contact_details= request.form["contactdetails"]
        available= request.form["available"]

        items= db.session.query(Book.id_book).filter(Book.isbn==isbn).all()
        for item in items:
            id_book= item.id_book

        from config import google_api_key
        params={'address':location,
                "key":google_api_key}

        url= 'https://maps.googleapis.com/maps/api/geocode/json?'
        response=requests.get(url, params).json()

        # getting lat/lng for the given address
        lat =response['results'][0]['geometry']['location']['lat']
        lon =response['results'][0]['geometry']['location']['lng']

        #create owner object to store the book owners data
        owner=Owner(id_book=id_book, isbn=isbn,owner_name=owner_name, owner_email=owner_email,location=location, contact_details=contact_details,
                     rating=rating,review=review, lat=lat, lon=lon,available=available)
        
        #Add object to the database
        db.session.add(owner)
        db.session.commit()
        db.session.close()

    return redirect("/",code=302)


#################################################################################################################
# ###################         Books List and Books Stats    #################################################
###################################################################################################################

#route to jasonify results--- common route
@app.route("/api/bookList")
def Library():

    global books
    data= jsonify(books)
    books=[]
    return data
    
#navigation route
@app.route("/visualisations", methods=["GET", "POST"])
def visualisations():
    
    return render_template("Stats.html")

# route to add recommendation model 


if __name__ == "__main__":
    app.run()
    