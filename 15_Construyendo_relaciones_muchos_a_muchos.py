from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Text

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

#Association table
book_categories = Table('book_categories', Base.metadata,
    Column('book:id', ForeignKey('book.id'), primary_key = True),
    Column('category_id', ForeignKey('book_category.id'), primary_key = True)
)

class BookCategory(Base):
    __tablename__ = 'book_category'

    id = Column(Integer, Sequence('book_category_id_seq'), primary_key = True)
    name = Column(String)

    books = relationship("Book", 
                        secondary = book_categories,
                        back_populates = "categories")

    def __repr__(self):
        return "{}".format(self.name)


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

    categories = relationship(
        'BookCategory',
        secondary = book_categories,
        back_populates = 'books'
    )

    def __repr__(self):
        return "{}".format(self.title)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

j_rowling = Author(firstname = 'Joanne', lastname = 'Rowling')

session.add(j_rowling)

j_rowling = session.query(Author).filter_by(firstname = 'Joanne').one()

book = Book(isbn = '9788498387087', title = 'Harry Potter y la Piedra Filosofal', description = 'La vida de Harry Potter cambia para siempre el...')
    
book.categories.append(BookCategory(name = 'Aventura'))
book.categories.append(BookCategory(name = 'Accion'))

book.author = j_rowling

print(session.query(Book).filter(Book.categories.any(name = 'Aventura')).all())

print(session.query(Book).\
    filter(Book.author == j_rowling).\
    filter(Book.categories.any(name = 'Aventura')).\
    all())

