# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 23:17:41 2017

@author: jeand
"""

#!flask/bin/python
from app import app
print "launching app"
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.run(debug=True, host='0.0.0.0', port=9000)