from app import db


class Book(db.Model):
    __tablename__ = 'Book'

    id_book = db.Column(db.String(20), primary_key=True) 
    title = db.Column(db.String(300))
    authors = db.Column(db.String(500))
    category=db.Column(db.String(50))
    language = db.Column(db.String(5))
    isbn = db.Column(db.String(13))
    published_date = db.Column(db.String(5))
    publisher = db.Column(db.String(100))
    image_url = db.Column(db.String(1000))
    description = db.Column(db.String(20000))
    sub_category= db.Column(db.String(50))
    num_pages=db.Column(db.Integer)
    average_rating=db.Column(db.Float(3))
    ratings_count=db.Column(db.Integer)
    reviews_count=db.Column(db.Integer)
    text_reviews_count=db.Column(db.Integer)

    def __repr__(self):
        return '<Book %r>' % (self.title)


class Owner(db.Model):
    __tablename__ = 'Owner'

    id_book = db.Column(db.String(20))
    isbn = db.Column(db.String(13),  primary_key=True)
    owner_name=db.Column(db.String(60), primary_key=True)
    owner_email = db.Column(db.String(60))
    location = db.Column(db.String(150))
    contact_details = db.Column(db.String(1000))
    rating = db.Column(db.Integer)
    review = db.Column(db.String(1000))
    lat= db.Column(db.Float(10))
    lon= db.Column(db.Float(10))
    available = db.Column(db.Integer)

    def __repr__(self):
        return '<Owner %r>' % (self.owner_email)