#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from intro_to_flask import app

CGIHandler().run(app)
