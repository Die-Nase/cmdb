from ORM import *


# I1 = InvestigationORM(title = 'first investigation')
# S1 = StudyORM(title = 'first Study')
# C1 = CommentORM(name = 'first comment',value = 'some description')
# C2 = CommentORM(name = 'second comment',value = 'some description')
# I1.comments.append(C1)
# I1.comments.append(C2)
# # S1.comments.append(C2)
# I1.studies.append(S1)
#I1 = InvestigationORM(title = 'first investigation')


engine = create_engine('sqlite:///test.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
#
#session.add(I1)
#session.commit()


# from sqlalchemy.orm import subqueryload
I_list = session.query(InvestigationORM).all()
for item in I_list:
    print(item.title)
# # I1 = session.query(InvestigationORM).options(subqueryload(InvestigationORM.comments)).filter_by(id=1).one()
# I1 = session.query(InvestigationORM).join(Link2).join(StudyORM).join(Link).join(CommentORM).one()
# print(I1)
# print(I1.comments[0].name)
# c1 = session.query(CommentORM).join(Link).join(StudyORM).join(Link2).join(InvestigationORM).all()
#T = investigation_orm2isa(I1)
# print(c1.name)
# query = session.query(User, Document, DocumentsPermissions).join(Document).join(DocumentsPermissions)
# # for x in session.query( InvestigationORM, CommentORM).filter(
# #         Link.investigation_id == InvestigationORM.id,
# #         Link.comment_id == CommentORM.id).order_by(Link.investigation_id).all():
# #     print ("Investigation: {} Comment: {}".format(x.InvestigationORM.title, x.CommentORM.name))