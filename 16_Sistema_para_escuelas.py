# -*- coding: utf-8 -*-
import csv
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

Base = declarative_base()

class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    name = Column(String)

    ninos = relationship('Nino', order_by='Nino.id', back_populates='curso')
    curso_schedules = relationship('Calendario', order_by='Calendario.time_from', back_populates='curso')

    def __repr__(self):
        return "{} {}".format(self.name)


class Nino(Base):
    __tablename__ = 'nino'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))

    curso = relationship('Curso', back_populates='ninos')

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Maestro(Base):
    __tablename__ = 'maestro'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    maestro_calendarios = relationship('Calendario', order_by='Calendario.time_from', back_populates='maestro')

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Calendario(Base):
    __tablename__ = 'schedule'
    
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)    
    weekday = Column(Integer)
    time_from = Column(Time)
    time_to = Column(Time)
    curso_id = Column(Integer, ForeignKey('curso.id'))
    maestro_id = Column(Integer, ForeignKey('maestro.id'))

    curso = relationship('Curso', back_populates='curso_schedules')
    maestro = relationship('Maestro', back_populates='maestro_calendarios')

    def __repr__(self):
        return "{} {}".format(self.name)


class ReporteCurso(object):

    def __init__(self, path):
        self.path = path

    def export(self, curso):
        ninos = curso.ninos
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for nino in ninos:
                writer.writerow([str(nino)])


class CalendarioReporteCurso(object):

    def __init__(self, path):
        self.path = path

    def export(self, curso):
        schedules = curso.curso_schedules
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for schedule in schedules:
                writer.writerow([schedule.weekday, schedule.time_from, schedule.time_to, schedule.maestro])


class CalendarioReporteMaestro(object):
    
    def __init__(self, path):
        self.path = path

    def export(self, maestro):
        schedules = maestro.maestro_calendarios
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for schedule in schedules:
                writer.writerow([schedule.weekday, schedule.time_from, schedule.time_to, schedule.curso.name])


def main(*args, **kwargs):
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    un_curso = Curso(name='1A')
    otro_curso = Curso(name='1B')

    un_nino = Nino(firstname='Lucas', lastname='Renx', curso=un_curso)
    otro_nino = Nino(firstname='Pedro', lastname='Gray', curso=otro_curso)
    tercer_nino = Nino(firstname='Maria', lastname='Ferry', curso=un_curso)

    un_maestro = Maestro(firstname='Jorge', lastname='Manzano')

    un_tiempo = datetime.time(8, 0, 0)
    otro_tiempo = datetime.time(10, 0, 0)
    tercer_tiempo = datetime.time(12, 0, 0)

    un_calendario = Calendario(weekday=1, time_from=un_tiempo, time_to=otro_tiempo, curso=un_curso, maestro=un_maestro)
    otro_calendario = Calendario(weekday=1, time_from=otro_tiempo, time_to=tercer_tiempo,
                                curso=otro_curso, maestro=un_maestro)
    
    session.add(un_curso)
    session.add(otro_curso)

    session.add(un_nino)
    session.add(otro_nino)
    session.add(tercer_nino)

    session.add(un_maestro)

    session.add(un_calendario)
    session.add(otro_calendario)

    session.commit()

    ReporteCurso('curso_{}.csv'.format(un_curso.name)).export(un_curso)
    ReporteCurso('curso_{}.csv'.format(otro_curso.name)).export(otro_curso)

    CalendarioReporteCurso('curso_schedule_{}.csv'.format(un_curso.name)).export(un_curso)
    CalendarioReporteCurso('curso_schedule_{}.csv'.format(otro_curso.name)).export(otro_curso)

    CalendarioReporteMaestro('maestro_calendario_{}.csv'.format(un_maestro)).export(un_maestro)


if __name__ == "__main__":
    main()