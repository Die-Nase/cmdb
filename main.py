import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.core.window import Window

from screeninfo import get_monitors

from ORM import *
engine = create_engine('sqlite:///test.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

#from kivy.uix.boxlayout import BoxLayout
print(Window.get_parent_layout)

def populate_tree_view(tree_view, parent, node):
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    for child_node in node['children']:
        populate_tree_view(tree_view, tree_node, child_node)


class DatabaseManager(FloatLayout):
    def __init__(self, **kwargs):
        super(DatabaseManager, self).__init__(**kwargs)

    def say_hello(self):
        #populate_tree_view(self.ids.tv, None, tree)
        print('button pressed')
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

    def display_metadata(self, tree, selected_node):
        for model in Base.__subclasses__():
            # print(model.__tablename__)
            if model.__tablename__ == selected_node.parent_node.text:
                orm_model = model
        selected_object = session.query(orm_model).filter(orm_model.identifier == selected_node.text).one()
        
        clms = dict(selected_object.__table__.columns)
        desc = list(clms.keys())
        value = 0
        count = 0
        for clm in clms:
            label = Label(text = desc[count], pos = (0, value))
            self.ids.right.add_widget(label)
            value = value + 50
            count = count +1



class MyApp(App):
    def build(self):
        monitors = get_monitors()
        Window.size = (.7 * monitors[0].width, .7 * monitors[0].height)
        Window.left = 0.15 * monitors[0].width
        Window.top = 0.15 * monitors[0].height
        return DatabaseManager()


if __name__ == "__main__":
    MyApp().run()