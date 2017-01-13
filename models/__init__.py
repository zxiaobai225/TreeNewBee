from flask_sqlalchemy import SQLAlchemy
import time
import random

db = SQLAlchemy()


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def date_time():
    format = '%Y/%m/%d %H:%M:%S'
    v = int(time.time()) + 3600 * 8
    valuegmt = time.gmtime(v)
    dt = time.strftime(format, valuegmt)
    return dt

