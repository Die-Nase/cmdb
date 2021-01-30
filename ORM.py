from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import isatools.model as isa

Base = declarative_base()


class Investigation(Base):
    __tablename__ = "investigation"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    identifier = Column(String)
    title = Column(String)
    description = Column(String)
    comments = relationship('Comment', secondary = 'link', lazy='subquery')
    studies = relationship('Study', secondary = 'link2', lazy='subquery')

    # def attr2node(self):
    #     tree = {'node_id': self.identifier,
    #             'children': [{'node_id': 'studies',
    #                           'children': []},
    #                          {'node_id': 'comments',
    #                           'children': []}]}
    #     return tree


class Comment(Base):
    __tablename__ = "comment"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    # investigations = relationship('InvestigationORM', secondary = 'link')
    def __str__(self):
        return()


class Study(Base):
    __tablename__ = "study"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    identifier = Column(String)
    title = Column(String)
    description = Column(String)
    comments = relationship("Comment", secondary = 'link')


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
    isa_obj = isa.Investigation(id_= str(orm_obj.id), filename=orm_obj.filename,
                        identifier=orm_obj.identifier, title=orm_obj.title,
                        description=orm_obj.description)
    for comment in orm_obj.comments:
        isa_obj.add_comment(comment.name,comment.value)
        # c1 = Comment(comment.name,comment.value)
        # isa.comments.append(c1)
    return isa_obj


def investigation_isa2orm(isa_obj):
    orm_obj = Investigation(filename=isa_obj.filename,
                        identifier=isa_obj.identifier, title=isa_obj.title,
                        description=isa_obj.description)
    if not(isa_obj.id == 'None'):
        orm_obj = int(isa_obj.id)

    for comment in isa_obj.comments:
        C = Comment(name = comment.name,value = comment.value)
        # if not.isinstance(comment.id, None):
        # orm_obj = int(isa_obj.id)
        orm_obj.comments.append(C)
    return orm_obj