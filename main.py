import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


from screeninfo import get_monitors

from ORM import *
engine = create_engine('sqlite:///test.db', echo = True)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
import sqlalchemy
Session = sessionmaker(bind = engine)
session = Session()


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
            populate_tree_view(self.ids.tv, None, self.attr2node(item))

    def fill_screen(self):
        I_list = session.query(Investigation).all()
        self.create_tree(I_list)

    def display_metadata(self, tree, selected_node):
        self.ids.right.clear_widgets(self.ids.right.children)
        obj_id = int(selected_node.text.split('id:')[1])
        for model in Base.__subclasses__():
            # print(model.__tablename__)
            if model.__tablename__ == selected_node.parent_node.text:
                orm_model = model
        selected_object = session.query(orm_model).filter(orm_model.id == obj_id).one()
        
        clms = dict(selected_object.__table__.columns)
        clms_keys = list(clms.keys())
        count = 0
        for clm in clms:
            label = Label(text = clms_keys[count])
            textinput = TextInput(text = str(selected_object.__dict__[clms_keys[count]]))
            self.ids.right.add_widget(label)
            self.ids.right.add_widget(textinput)
            count = count + 1

    def attr2node(self, obj):
        if hasattr(obj, 'identifier'):
            desc = obj.identifier
        elif hasattr(obj, 'name'):
            desc = obj.name
        node_id = str(desc) + " id:"+ str(obj.id)
        tree = {'node_id': node_id, 'children':[]}
        obj_dict = obj.__dict__
        for key in obj_dict.keys():
            if isinstance(obj_dict[key],sqlalchemy.orm.collections.InstrumentedList):
                tree['children'].append({'node_id': str(key),'children': []})
        return tree


class MyApp(App):
    def build(self):
        monitors = get_monitors()
        Window.size = (.7 * monitors[0].width, .7 * monitors[0].height)
        Window.left = 0.15 * monitors[0].width
        Window.top = 0.15 * monitors[0].height
        return DatabaseManager()


if __name__ == "__main__":
    MyApp().run()