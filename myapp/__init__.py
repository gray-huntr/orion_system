from flask import Flask

myapp = Flask(__name__)

from myapp import admin
from myapp import client
from myapp import staff
