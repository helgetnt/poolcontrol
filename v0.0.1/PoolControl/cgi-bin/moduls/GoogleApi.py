#!/usr/bin/env python
global dat
global plog
global vlog
from moduls.config import *

def graph_script_1(table):
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Uhrzeit', 'Pool - Temp.', 'Solar - Temp.', 'Luft - Temp.'],
%s
        ]);

        var options = {
          title: '%s',
          backgroundColor: 'lightgrey',
          curveType: 'function',
          focusTarget: 'category',
          // hAxis: {baselineColor: 'red', logScale: true},
          vAxis: {title: 'Temperatur', titleTextStyle: {color: 'blue'}, baseline: 0, ticks: [5,10,15,20,25,30,35,40,45], minorGridlines: {count: '5'}},
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""
    print chart_code % (table, settings['datum'])

def graph_script_2(table):
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Uhrzeit', 'Pool - Temp.', 'Solar - Temp.', 'Luft - Temp.', 'Pumpe - Zustand'],
%s
        ]);

        var options = {
          title: '%s',
          backgroundColor: 'lightgrey',
          curveType: 'function',
          focusTarget: 'category',
          // hAxis: {baselineColor: 'red', logScale: true},
          vAxis: {title: 'Temperatur', titleTextStyle: {color: 'blue'}, baseline: 0, ticks: [5,10,15,20,25,30,35,40,45], minorGridlines: {count: '5'}},
          seriesType: "line",
          series: {3: {type: "steppedArea"}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""
    print chart_code % (table, settings['datum'])

def graph_script_3(table):
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Uhrzeit', 'Pool - Temp.', 'Solar - Temp.', 'Luft - Temp.', 'Pumpe - Zustand', 'Ventil - Zustand'],
%s
        ]);

        var options = {
          title: '%s',
          backgroundColor: 'lightgrey',
          curveType: 'function',
          focusTarget: 'category',
          // hAxis: {baselineColor: 'red', logScale: true},
          vAxis: {title: 'Temperatur', titleTextStyle: {color: 'blue'}, baseline: 0, ticks: [5,10,15,20,25,30,35,40,45], minorGridlines: {count: '5'}},
          seriesType: "line",
          series: {3: {type: "steppedArea"},
                   4: {type: "steppedArea"}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""
    print chart_code % (table, settings['datum'])

def graph_script_4(table):
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Uhrzeit', 'Pool - Temp.', 'Solar - Temp.', 'Luft - Temp.', 'Pumpe - Zustand', 'Ventil - Zustand', 'Refill'],
%s
        ]);

        var options = {
          title: '%s',
          backgroundColor: 'lightgrey',
          curveType: 'function',
          focusTarget: 'category',
          // hAxis: {baselineColor: 'red', logScale: true},
          vAxis: {title: 'Temperatur', titleTextStyle: {color: 'blue'}, baseline: 0, ticks: [5,10,15,20,25,30,35,40,45], minorGridlines: {count: '5'}},
          seriesType: "line",
          series: {3: {type: "steppedArea"},
                   4: {type: "steppedArea"},
                   5: {type: "steppedArea"}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""
    print chart_code % (table, settings['datum'])
