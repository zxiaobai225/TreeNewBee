import sys
from os.path import abspath
from os.path import dirname

sys.path.insert(0, abspath(dirname(__file__)))

from app import configure_app

application = configure_app()
