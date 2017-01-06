from . import db
from . import ModelMixin


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    content = db.Column(db.String(225))
    keywords = db.Column(db.String(225))
    master = db.Column(db.String(225))
    parent_id = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.name = form.get('name', '')
        self.content = form.get("content", '')
        self.keywords = form.get("keywords", '板块')
        self.master = form.get('master', '')
        self.parent_id = form.get("parent_id", '')

    def update(self, form):
        print('board.update, ', form)
