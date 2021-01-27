import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeView,TreeViewLabel

from ORM import *
engine = create_engine('sqlite:///test.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

#from kivy.uix.boxlayout import BoxLayout

def populate_tree_view(tree_view, parent, node):
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    for child_node in node['children']:
        populate_tree_view(tree_view, tree_node, child_node)


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


class DatabaseManager(FloatLayout):
    def __init__(self, **kwargs):
        super(DatabaseManager, self).__init__(**kwargs)

    def say_hello(self):
        #populate_tree_view(self.ids.tv, None, tree)
        print('hello')
        self.fill_screen()

    def create_tree(self, orm_list):
        for node in [i for i in self.ids.tv.iterate_all_nodes()]:
            self.ids.tv.remove_node(node)
        self.ids.tv.hide_root = False
        self.ids.tv.root_options=dict(text=orm_list[0].__tablename__)
        for item in orm_list:
            populate_tree_view(self.ids.tv, None, item.attr2node())

    def fill_screen(self):
        I_list = session.query(InvestigationORM).all()
        self.create_tree(I_list)




class MyApp(App):
    def build(self):
        return DatabaseManager()


if __name__ == "__main__":
    MyApp().run()