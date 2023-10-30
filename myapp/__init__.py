from flask import Flask

myapp = Flask(__name__)
myapp.config.from_object("config.Config")

from myapp import admin
from myapp import patient
from myapp import staff