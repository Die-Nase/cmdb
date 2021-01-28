from ORM import *
engine = create_engine('sqlite:///test.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

for c in Base.__subclasses__():
    print(c.__tablename__)

    
# tree = {'node_id': '1',
#         'children': [{'node_id': '1.1',
#                       'children': [{'node_id': '1.1.1',
#                                     'children': [{'node_id': '1.1.1.1',
#                                                   'children': []}]},
#                                    {'node_id': '1.1.2',
#                                     'children': []},
#                                    {'node_id': '1.1.3',
#                                     'children': []}]},
#                       {'node_id': '1.2',
#                        'children': []}]}