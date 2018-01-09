# -*- coding: utf-8 -*-
"""
Created on Fri Dec 01 23:17:19 2017

@author: jeand
"""
from flask import render_template
from app import app
import numpy as np

from flask import Flask, render_template, flash, request, Response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Jean-Damien'}  # fake user
    return render_template('home.html')
	




@app.route('/index_backup')
def index_backup():
    user = {'nickname': 'Jean-Damien'}  # fake user
    return render_template('index_backup.html')





def group(x):
    if np.isreal(x)==False:
        return x
    else:
        s = '%d' % x
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ','.join(reversed(groups))


    

def df_to_html(pd_df, table_class, table_style, level_1, level_2, value):
    #build pivot tables
    df_pivot_1=pd.pivot_table(pd_df, index=[level_1], values=[value], aggfunc=sum)
    df_pivot_1.reset_index(inplace=True)
    df_pivot_2=pd.pivot_table(pd_df, index=[level_1, level_2], values=[value], aggfunc=sum)    
    df_pivot_2.reset_index(inplace=True)
    total_str=""
    #start preparing html code
    #total_str="<div class=" +"'"+"col-sm-3"+"'"+">\n "
    #total_str+="<section class="+"'"+"panel "+"'"+">\n "
    #total_str+="<header class="+"'"+"panel-heading"+"'"+">\n "
    total_str+="<table class=" +"'"+table_class+"'"+" style="+"'"+table_style+"'"+">\n"
    
    #build header
    total_str+="<thead>\n <tr >\n "
    for x in [level_1+"/"+level_2, value]:
        total_str+="<th>"+str(x)+"</th>\n "
    total_str+="</tr>\n </thead>\n <tbody>\n "
    
    #build body
    for i in range(len(df_pivot_1)):
        temp_lvl_1=df_pivot_1.loc[i][0]
        #total_str+="<li class="+"'"+"toctree-l1"+"'"+">"
        #total_str+=<li class="toctree-l1"><a class="reference internal" href="quickcharts.html">Chart Views</a><ul>
        total_str+="<tr data-toggle="+"'"+"collapse"+"'"+" id="+"'"+temp_lvl_1+"'"+" data-target="+"'."+temp_lvl_1+"collapsed"+"'"+" class="+"'"+"clickable"+"'"+" style="+"'"+"cursor: pointer;font-size: 90%;"+"'"+">\n "
        #total_str+="<tr>\n "
        #total_str+="<a data-toggle="+"'"+"collapse"+"'"+" href="+"'"+"#'"+temp_lvl_1+"'"+">"+temp_lvl_1+"</a>"
        for j in range(len(df_pivot_1.columns)):
            total_str+="<td>"+str(group(df_pivot_1.loc[i][j]))+"</td>\n "
        total_str+="</tr>\n "
        #total_str+="</li>"
        #total_str+="<div id="+"'"+temp_lvl_1+"'"+">\n "
        
        #Builld hidden rows in blue colour
        for k in range(len(df_pivot_2)):
            if df_pivot_2[level_1][k]==temp_lvl_1:
                total_str+="<tr class="+"'"+"collapse out budgets "+temp_lvl_1+"collapsed"+"'"+">\n "
                for l in range(len(df_pivot_2.columns)):                    
                    if df_pivot_2.columns[l]!=level_1:
                        total_str+="<td height="+"'"+"1"+"'"+" class="+"'"+"hiddenRow"+"'"+" style="+"'"+"color:CornflowerBlue;background-color: AliceBlue;font-size: 75%;"+"'"+">"+str(group(df_pivot_2.loc[k][l]))+"</td>\n "                            
                total_str+="</tr>\n "                  
        
        
    total_str+="</tbody>\n "
    total_str+="</table>\n " 
    #total_str+="</section>"
    #total_str+="</div>"
    return total_str
       
    
        
    
    


# App config.
#DEBUG = True
#app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        print request.form.keys()
        print name
 
        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)



	
@app.route("/base1", methods=['GET', 'POST'])	    
def base1():
  df_results=pd.read_csv(r"C:\Users\jeand\Desktop\flask - risk quant\app\content"+"\\"+"Book1.csv")
  level1="Book"
  level2="Product"
  my_values="Delta"
  df_html=df_to_html(pd_df=df_results, table_class="table table-hover", 
                     table_style="border-collapse:collapse;v", 
                     level_1=level1, level_2=level2,  value=my_values)
  #df_html_bis=df_results.to_html(float_format=lambda x: ':20,.2f' % x)
  if request.method == 'POST':
    print "coucou"
    print request.method
    print request.form.keys()   
    print request.form["level1"]
    print "the end"    

    level1 = request.form["level1"]
    level2 = request.form["level2"]
    print level1
    print level2
    df_html=df_to_html(pd_df=df_results, table_class="table table-hover", 
                     table_style="border-collapse:collapse;v", 
                     level_1=level1, level_2=level2,  value=my_values)
    
    print "df_HTML ok"
  return render_template("base1.html",
						  title='Home',
						  table=df_html, 
                          default_level_1=level1,
                          default_level_2=level2)


@app.route("/model_perf/<model_perf_id>", methods=['GET', 'POST'])	    
def model_perf(model_perf_id):
    #model_perf_id="perf_001"
    df_data=pd.read_csv(r"C:\Users\jeand\Desktop\flask - risk quant\app\content"+"\\"+"model_perf.csv")
    list_model_perf=list(set(df_data["model_perf_id"]))
    #list_model_perf=["perf_001",  "perf_002"]
    df_data=df_data[df_data["model_perf_id"]==model_perf_id]
    
    x_values=list(df_data["Date"])  
    y_values=list(df_data["value"])
    y_values_threshold=list(df_data["Threshold"])
    
    
    y_values=[float(x) for x in y_values]
    y_values_threshold=[float(x) for x in y_values_threshold]   

    return render_template("model_perf.html",  mylist=x_values, mydata_1=y_values, mydata_2=y_values_threshold,  m_perf_id=model_perf_id, list_model_perf=list_model_perf)    



@app.route("/reassessment_discounting_model", methods=['GET', 'POST'])	    
def reassessment_discounting_model():
  df_results=pd.read_csv(r"C:\Users\jeand\Desktop\flask - risk quant\app\content"+"\\"+"Book1.csv")
  level1="Book"
  level2="Product"
  my_values="Delta"
  df_html=df_to_html(pd_df=df_results, table_class="table table-hover", 
                     table_style="border-collapse:collapse;v", 
                     level_1=level1, level_2=level2,  value=my_values)
  #df_html_bis=df_results.to_html(float_format=lambda x: ':20,.2f' % x)
  if request.method == 'POST': 

    level1 = request.form["level1"]
    level2 = request.form["level2"]
    print level1
    print level2
    df_html=df_to_html(pd_df=df_results, table_class="table table-hover", 
                     table_style="border-collapse:collapse;v", 
                     level_1=level1, level_2=level2,  value=my_values)
    
    print "df_HTML ok"
  return render_template("discounting_model.html",
						  title='Home',
						  table=df_html, 
                          default_level_1=level1,
                          default_level_2=level2)


@app.route("/under_construction", methods=['GET', 'POST'])	    
def under_construction():
  return render_template("under_construction.html")


@app.route("/parse_pdl", methods=['GET', 'POST'])	    
def parse_pdl():   
  return render_template("parse_pdl.html")    

@app.route("/vol_surface", methods=['GET', 'POST'])	    
def vol_surface():   
  return render_template("vol_surface.html")  


@app.route("/vol_surface_csv")
def vol_surface_csv():
    with open(r"C:\Users\jeand\Desktop\flask - risk quant\app\templates"+"\\"+"vol_surface.csv") as fp:
         csv = fp.read()
    #csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=vol_surface.csv"})