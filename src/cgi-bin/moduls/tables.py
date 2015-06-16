#!/usr/bin/env python
# convert rows from database into a javascript table
global dat
global plog
global vlog
from moduls.config import *

def create_table_1(filename):
    chart_table=""
    data_lines=[]
    table=""
    file_name = str(settings['data_dir']+filename)
    with open(file_name, "r") as data_file:
        data_lines=data_file.readlines()
        for line in data_lines:
            w = line.strip('\n').split(' ')
            x = w[0].split('-')
            y = x[1][:-3]
            z = w[1:8]
            table += "['"+y+"', "+z[0]+", "+z[1]+", "+z[2]+"],\n"
        else:
            w = data_lines[-1].strip('\n').split(' ')
            x = w[0].split('-')
            settings['datum'] += x[0]

    return table


def create_table_2(filename):
    file1 = str(settings['data_dir']+filename)
    file2 = file1[:-4]+'.plf'
    fobj1 = open(file1, "r")
    fobj2 = open(file2, "r")
    p_table=""    
    with open(file1) as f1:
        line_count1 = len(f1.readlines())
    with open(file2) as f2:
        line_count2 = len(f2.readlines())

    if line_count1 == line_count2:
      while True:
        line1 = fobj1.readline()
        line2 = fobj2.readline()
        if not line1:
            break
        if not line2:
            break
        y=line1.strip('\n').split(' ')
        x=y[0].split('-')
        z=line2.strip('\n').split(' ')
        w=plf_check(z[1])
        table_line = "['"+x[1][:-3]+"', "+y[1]+", "+y[2]+", "+y[3]+", "+w+"],\n"
        p_table += table_line
    return p_table

def create_table_3(filename):
    file1 = str(settings['data_dir']+filename)
    file2 = file1[:-4]+'.plf'
    file3 = file1[:-4]+'.vlf'
    fobj1 = open(file1, "r")
    fobj2 = open(file2, "r")
    fobj3 = open(file3, "r")
    v_table=""
    with open(file1) as f1:
        line_count1 = len(f1.readlines())
    with open(file2) as f2:
        line_count2 = len(f2.readlines())
    with open(file3) as f3:
        line_count3 = len(f3.readlines())

    if line_count1 == line_count2:
      if line_count1 == line_count3:
        while True:
            line1 = fobj1.readline()
            line2 = fobj2.readline()
            line3 = fobj3.readline()
            if not line1:
                break
            if not line2:
                break
            if not line3:
                break
            y=line1.strip('\n').split(' ')
            x=y[0].split('-')
            z1=line2.strip('\n').split(' ')
            w1=plf_check(z1[1])
            z2=line3.strip('\n').split(' ')
            w2=vlf_check(z2[1])
            table_line = "['"+x[1][:-3]+"', "+y[1]+", "+y[2]+", "+y[3]+", "+w1+", "+w2+"],\n"
            v_table += table_line
    return v_table

def check(option):
    p = []
    q = [p[:-4] for p in plog]
    r = [p[:-4] for p in vlog]
    if option[:-4] not in q:
        b = create_table_1(option)

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
                    with open(file3,"r") as f3:
                        line_count3 = len(f3.readlines())
                    if line_count1 == line_count3:
                        b = create_table_3(option)
                    else:
                        b = create_table_2(option)
            else:
                    b = create_table_2(option)
        elif line_count1 != line_count2:
            b = create_table_1(option)
    return b
