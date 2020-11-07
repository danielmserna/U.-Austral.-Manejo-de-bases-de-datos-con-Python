from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, Sequence('author_id_seq'), primary_key = True)
    firstname = Column(String)
    lastname = Column(String)

    books = relationship("Book", order_by = "Book.id", back_populates = "author",
                            cascade = "all, delete, delete-orphan")

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

Session = sessionmaker(bind=engine)

session = Session()

#Commit changes
session.commit()

j_rowling = Author(firstname = 'Joanne', lastname = 'Rowling')

j_rowling.books=[
    Book(isbn = '9788498387087', title = 'Harry Potter y la Piedra Filosofal', description = 'La vida de Harry Potter cambia para siempre el...'),
    Book(isbn = '9788498382679', title = 'Harry Potter y la cámara secreta', description = 'Tras derrotar una vez más a Lord Voldemort...')
]

session.add(j_rowling)
session.commit()

#Deleting
session.delete(j_rowling)

print(session.query(Author).filter_by(firstname = 'Joanne').count())

print(session.query(Book).filter(Book.isbn.in_(['9788498387087','9788498382679'])).count())

