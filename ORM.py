from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from isatools.model import *

Base = declarative_base()


class InvestigationORM(Base):
    __tablename__ = "investigation"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    identifier = Column(String)
    title = Column(String)
    description = Column(String)
    comments = relationship('CommentORM', secondary = 'link')
    studies = relationship('StudyORM', secondary = 'link2')


class CommentORM(Base):
    __tablename__ = "comment"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    # investigations = relationship('InvestigationORM', secondary = 'link')
    def __str__(self):
        return()


class StudyORM(Base):
    __tablename__ = "study"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    identifier = Column(String)
    title = Column(String)
    description = Column(String)
    comments = relationship("CommentORM", secondary = 'link')


class Link(Base):
    __tablename__ = "link"
    
    comment_id = Column(Integer,ForeignKey('comment.id'), primary_key=True)
    investigation_id = Column(Integer, ForeignKey('investigation.id'))
    study_id = Column(Integer, ForeignKey('study.id'))


class Link2(Base):
    __tablename__ = "link2"
    
    investigation_id = Column(Integer, ForeignKey('investigation.id'), primary_key=True)
    study_id = Column(Integer, ForeignKey('study.id'), primary_key=True)


def investigation_orm2isa(orm_obj):
    isa_obj = Investigation(id_= str(orm_obj.id), filename=orm_obj.filename,
                        identifier=orm_obj.identifier, title=orm_obj.title,
                        description=orm_obj.description)
    for comment in orm_obj.comments:
        isa_obj.add_comment(comment.name,comment.value)
        # c1 = Comment(comment.name,comment.value)
        # isa.comments.append(c1)
    return isa_obj


def investigation_isa2orm(isa_obj):
    orm_obj = InvestigationORM(filename=isa_obj.filename,
                        identifier=isa_obj.identifier, title=isa_obj.title,
                        description=isa_obj.description)
    if not(isa_obj.id == 'None'):
        orm_obj = int(isa_obj.id)

    for comment in isa_obj.comments:
        C = CommentORM(name = comment.name,value = comment.value)
        # if not.isinstance(comment.id, None):
        # orm_obj = int(isa_obj.id)
        orm_obj.comments.append(C)
    return orm_obj