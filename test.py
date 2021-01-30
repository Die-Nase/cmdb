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
    comments = relationship('CommentORM', lazy='joined')



class CommentORM(Base):
    __tablename__ = "comment"
    
    id = Column(Integer, primary_key=True)
    investigation_id = Column(Integer, ForeignKey('investigation.id'))
    name = Column(String)
    value = Column(String)

# I1 = InvestigationORM(identifier = 'ident 3')
# C1 = CommentORM(name = 'first comment',value = 'some description')
# C2 = CommentORM(name = 'second comment',value = 'some description')
# I1.comments.append(C1)
# I1.comments.append(C2)


engine = create_engine('sqlite:///test2.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

I3 = session.query(InvestigationORM).one()

# d = I.__dict__

# for key in d.keys():
#     #print(type(d[key]))
#     print(str(key))

# # session.add(I1)
# # session.commit()
import sqlalchemy

def attr2node(obj):
    if hasattr(obj, 'identifier'):
        desc = obj.identifier
    elif hasattr(obj, 'name'):
        desc = obj.name
    node_id = str(desc) + " id:"+ str(obj.id)
    tree = {'node_id': node_id, 'children':[]}
    obj_dict = obj.__dict__
    children_list = []
    for key in obj_dict.keys():
        if isinstance(obj_dict[key],sqlalchemy.orm.collections.InstrumentedList):
                tree['children'].append({'node_id': str(key),'children': []})

    return tree


# I = InvestigationORM()
t = attr2node(I3)

