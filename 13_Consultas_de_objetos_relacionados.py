from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists


engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, Sequence('author_id_seq'), primary_key = True)
    firstname = Column(String)
    lastname = Column(String)

    books = relationship("Book", order_by = "Book.id", back_populates = "author")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, Sequence('book_id_seq'), primary_key = True)
    isbn = Column(String)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship("Author", back_populates = "books")

    def __repr__(self):
        return "{}".format(self.title)

Base.metadata.create_all(engine)

author = Author(firstname = 'Joanne', lastname = 'Rowling')

Session = sessionmaker(bind=engine)

session = Session()

j_rowling = Author(firstname = 'Joanne', lastname = 'Rowling')

j_rowling.books=[
    Book(isbn = '9788498387087', title = 'Harry Potter y la Piedra Filosofal', description = 'La vida de Harry Potter cambia para siempre el...'),
    Book(isbn = '9788498382679', title = 'Harry Potter y la cámara secreta', description = 'Tras derrotar una vez más a Lord Voldemort...')
]

session.add(j_rowling)
session.commit()

print("Query # 1")
for an_author, a_book in session.query(Author,Book).\
        filter(Author.id == Book.author_id).\
        filter(Book.isbn == '9788498387087').\
        all():
    print(an_author)
    print(a_book)

print("Query # 2")
print(session.query(Author).join(Book).\
        filter(Book.isbn == '9788498387087').\
        all())

print("Query # 3")
print(session.query(Author).join(Book, Author.id == Book.author_id).all()) #Explicit condition

print("Query # 4")
print(session.query(Author).join(Author.books).all()) #Specify relationship from left to right

print("Query # 5")
print(session.query(Author).join(Book, Author.books).all())

print("Query # 6")
print(session.query(Author).join('books').all())

print("Query # 7")
stmt = exists().where(Book.author_id == Author.id)
for name, in session.query(Author.firstname).filter(stmt):
    print(name)

print("Query # 8")
for name, in session.query(Author.firstname).filter(Author.books.any()):
    print(name)

print("Query # 9")
for name, in session.query(Author.firstname).\
            filter(Author.books.any(Author.lastname.like('%Row%'))):
    print(name)

print("Query # 10")
print(session.query(Book).filter(~Book.author.has(Author.firstname == 'Joanne')).all())

