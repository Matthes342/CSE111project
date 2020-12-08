#!/usr/bin/python3
import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State

import proj

app = dash.Dash()

conn = proj.openConnection(r"proj.sqlite")
allAddresses = "SELECT n_address FROM network ORDER BY n_address"
c = conn.cursor()
c.execute(allAddresses)
allAddresses= []
addrOptions= []
for i in c.fetchall():
    allAddresses.append(i[0])
for i in allAddresses:
    addrOptions.append({'label': i, 'value': i})

speeds = "SELECT DISTINCT s_speed FROM speed ORDER BY s_speed"
c.execute(speeds)
speeds = []
speedOptions = []
for i in c.fetchall():
    speeds.append(i[0])
for i in speeds:
    speedOptions.append({'label': str(i) + " mbps", 'value': i})

proj.closeConnection(conn, r"proj.sqlite")

app.layout = html.Div(children =[ 
    html.H1("Input a new house"),
    html.Div(id = 'space'),
    dcc.Dropdown(
        id = 'Loc', 
        options=[
            {'label': 'San Diego', 'value': 'San Diego'},
            {'label': 'Los Angeles',  'value': 'Los Angeles'},
            {'label': 'Merced',  'value': 'Merced'},
            {'label': 'Tokyo',  'value': 'Tokyo'},
            {'label': 'Moscow',  'value': 'Moscow'}
        ],
        value='Merced'
    ),
    dcc.Input(id = 'addr', type = 'number'),
    dcc.Input(id = 'num', type = 'number'),
    html.Button('Submit', id = 'button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),
    html.Div(id = 'div'),
    'Find the address of the contract you would like to delete',
    dcc.Dropdown(
        id = 'addies', 
        options=addrOptions,
        value=allAddresses[0]
    ),
    html.Button('Submit', id = 'button1'),
    html.Div(id='deleteContract-output',
             children='Enter a value and press submit'),

    dcc.Input(id = 'newIsp', type = 'text', placeholder="Insert new ISP"),
    html.Button('Submit', id = 'button2'),
    html.Div(id='addIsp-output',
             children='Enter a value and press submit'),

    dcc.Dropdown(
        id = 'speeds', 
        options=speedOptions,
        value=str(speeds[0]) + " mbps"
    ),
    dcc.Input(id = 'newSpeed', type = 'number'),
    html.Button('Submit', id = 'button3'),
    html.Div(id='updateSpeed-output',
             children='Enter a value and press submit'),
    dcc.Interval(
        id='interval-update',
        interval=2*1000,
        n_intervals=0
    ),
    html.Div(id='updateDropDown-output')
]) 

# insertHouse()
@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks'),
     State("Loc", "value")],
    [State('num', 'value'),
     State('addr', 'value')]
)
def insertInfo(n_clicks, loc, num, addr):
    if n_clicks != None:
        conn = proj.openConnection(r"proj.sqlite")
        nclicks = None
        print("Inserted")
        with conn:
            proj.inserthouse(conn, "Address___#" + str(addr), num, loc)
        proj.closeConnection(conn, r"proj.sqlite")

# endContract()
@app.callback(
    Output('deleteContract-output', 'children'),
    [Input('button1', 'n_clicks'), 
     State("addies", "value")],
)
def deleteContractInfo(n_clicks, addr):
    if n_clicks != None:
        conn = proj.openConnection(r"proj.sqlite")
        nclicks = None
        print("Deleted Contract")
        with conn:
            proj.endcontract(conn, addr)
        proj.closeConnection(conn, r"proj.sqlite")

# insertIsp()
@app.callback(
    Output('addIsp-output', 'children'),
    [Input('button2', 'n_clicks'), 
     State("newIsp", "value")],
)
def addIspInfo(n_clicks, isp):
    if n_clicks != None:
        conn = proj.openConnection(r"proj.sqlite")
        nclicks = None
        print("ISP Added")
        with conn:
            proj.insertisp(conn, isp)
        proj.closeConnection(conn, r"proj.sqlite")

#updateSpeed()
@app.callback(
    Output('updateSpeed-output', 'children'),
    [Input('button3', 'n_clicks'), 
     State("speeds", "value"),
     State('newSpeed', 'value')
     ],
)
def updateSpeedInfo(n_clicks, oldSpeed, newSpeed):
    if n_clicks != None:
        conn = proj.openConnection(r"proj.sqlite")
        nclicks = None
        print("Speeds Updated")
        with conn:
            proj.updatespeed(conn, oldSpeed, newSpeed)
        proj.closeConnection(conn, r"proj.sqlite")
        # return [speedOptions]

@app.callback(
    [Output('updateDropDown-output', 'children')], 
    [Input('interval-update', 'n_intervals')]
)
def updateSpeedDropDown(n_intervals):
    conn = proj.openConnection(r"proj.sqlite")
    c = conn.cursor()
    speeds = "SELECT DISTINCT s_speed FROM speed ORDER BY s_speed"
    c.execute(speeds)
    speeds = [{'label': str(i[0]) + " mbps", 'value': i[0]} for i in c.fetchall()]
    proj.closeConnection(conn, r"proj.sqlite")
    return [speeds]

if __name__ == '__main__':
    app.run_server(debug=True)
