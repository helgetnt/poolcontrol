#!/usr/bin/env python

import os
import sys
import cgi
import cgitb
import csv 
import time
import datetime

from time import *
from datetime import datetime
from datetime import timedelta

from moduls.config import *
from moduls.GoogleApi import *
from moduls.reader import * 
from moduls.tables import *

lt = localtime()
datecheck = strftime("%Y-%m-%d.dat")

Zeitformat = "%Y-%m-%d %H:%M:%S"
Zeit = datetime.now()

global dat
global plog
global vlog

# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"

# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table, option):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print_Head_Mobile()
    print_graph_script(table)
    func()
    if datecheck == option:
        print '<meta http-equiv="refresh" content="150"/>'
    emstyle = """
<style type="text/css">
         <!--
         em { color:blue;
             margin-left:1em;
             margin-right:1em;
             font-size:1.5em; }
         em1 { color:darkred;
             margin-left:1em;
             margin-right:1em;
             font-size:1.5em; }
         em2 { color:black;
             margin-left:1em;
             margin-right:1em;
             font-size:1.0em; }
         err { color:darkred;
             margin-left:0.5em;
             margin-right:0.5em;
             font:bold 1.2em times;
             font-style:italic; 
             font-size:2em; }
         td { text-align:center;
            background-color:lightgray; }
         th { text-align:center;
            background-color:darkgray; }
         table#temp em { color:red;
                       margin-left:0.5em;
                       margin-right:0.5em;
                       font-size:1.0em; }
         table#temp em1 { color:black;
                        margin-left:0.5em;
                        margin-right:0.5em;
                       font-size:1.0em; }
         table#temp em2 { color:blue;
                        margin-left:0.5em;
                        margin-right:0.5em;
                       font-size:1.0em; }
         #t_div table, tr, th, td { border:3px outset black; }

         -->
</style>"""
    #"""
    print emstyle
    print "</head>"

def func():
    print """<script type="text/javascript">function DOsubmit(){document.forms["form1"].submit();}</script> """

def print_Head_Mobile():
    #print '<meta name="viewport" content="initial-scale=1,maximum-scale=1.0,minimum-scale=0.2,height=device-height">'
    #print '<meta name="viewport" content="width=device-width, initial-scale=1">'
    #print '<meta name="apple-mobile-web-app-capable" content="yes" />'
    #print '<meta name="apple-mobile-web-app-status-bar-style" content="black" />'
    print '<link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.css" />'
    print '<script src="http://code.jquery.com/jquery-1.8.3.js"></script>'
    print '<script src="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.js"></script>'
    
def print_graph_script(table):
    p = []
    q = [p[:-4] for p in plog]
    r = [p[:-4] for p in vlog]
    if option[:-4] not in q:
        a = graph_script_1(table)

    if option[:-4] in q:
        file1 = str(settings['data_dir']+option)
        file2 = file1[:-4]+'.plf'
        file3 = file1[:-4]+'.vlf'
        with open(file1, "r") as f1:
            line_count1 = len(f1.readlines())
        with open(file2, "r") as f2:
            line_count2 = len(f2.readlines())
        if line_count1 == line_count2:
            if option[:-4] in r:
                #if file3:
                    with open(file3, "r") as f3:
                        line_count3 = len(f3.readlines())
                    if line_count1 == line_count3:
                        a = graph_script_3(table)
                    else:
                        a = graph_script_2(table)
            else:
                    a = graph_script_2(table)
        elif line_count1 != line_count2:
            a = graph_script_1(table)
    return a

# print the div that contains the graph
def show_graph():
    #print "<h2>Temperatur Verlauf vom : "+settings['datum']+"</h2>"
    #print '<ul data-theme="a">'
    #print ' <div id="chart_div" style="width: 1200px; height: 300px;"></div>'
    print ' <div id="chart_div" style="height: 490px;"></div>'
    #print '</ul>'


def print_time_selector(option):
    print """<form id="form1" action="" style="width: 280px;" method="POST">
        <select data-theme="a" name="timeinterval" onchange="DOsubmit();">"""

    for f in dat:
          if datecheck != f:
              a = f[:-4]
          else:
              a = "Heute"
          b = "<option value="+f+">"+a+"</option>"
          c = "<option value="+f+""" selected="selected">"""+a+"</option>"""
          
          if option is not None:
            if option != f:
                print b
            else:
                print c
          else:
             print "<h1>No Datafile found !!!</h1>"

    print """        </select>
    </form>"""

#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option_str = form["timeinterval"].value
        return option_str
    else:
        return None

def copyright():
    a=str(chr(169))
    cr="All Rights resevered by "+a+"2014 TNT Inc."
    print cr

def main():
    global option
    cgitb.enable()
    # get options that may have been passed to this script
    option = get_option()

    if option is None:
        option = max(dat)

    # print the HTTP header
    printHTTPheader()

    if len(option) != 0:
        # convert the data into a table
         table=check(option)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("RPi Temp-Logger", table, option)

    # print the page body
    print "<body>"
    print_time_selector(option)
    show_graph()
    show_log(option)
    copyright()
    print "</body>"
    print "</html>"
    sys.stdout.flush()

if __name__=="__main__":
    main()

