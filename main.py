#!/usr/bin/python3
#label x and y axis
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_table
import plotly.graph_objs as go
import dash
import pandas as pd
import sqlite3

#helper libraries
import proj
import builddb

def updatecon(price, speed, conname, house):
    con = sqlite3.connect('proj.sqlite')
    cursor = con.cursor()
    cursor.execute("""update network set n_conname = ?, n_price = ?, n_speed = ? where n_address = ?""", (conname, price, speed, house))
    
    con.commit()
    cursor.close()
    con.close()

def getdb():
    new_db_data = {}
    con = sqlite3.connect('proj.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for name in tables:
        name = name[0]
        sql = """select * from {}""".format(name)
        table = pd.read_sql_query(sql, con)

        new_db_data[name] = table 
    cursor.close()
    con.close()
    return new_db_data

def getdbq(sqls, param):
    test = {}
    con = sqlite3.connect('proj.sqlite')
    cursor = con.cursor()

    test = pd.read_sql_query(sqls, con, params=[param])
    cursor.close()
    con.close()
    return test

app = dash.Dash()

app.layout = html.Div([
    html.H2("ISP Price and Speed Comparison"),
    html.Div(
        [
            dcc.Dropdown(id="Addresses"),
             html.Div(id='drout-text',
             children='Current Contract: '),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
    dash_table.DataTable(
        id = 'table',
        style_data={ 'border': '1px solid grey' },
        virtualization=True,
        ),
    html.H2("Select a new plan to update your contact"),
    dcc.Dropdown(id="updcont",
            style={'width': '50%',
               'display': 'inline-block'}),
    html.Div(id='drupd-text',
             children='Updated contract to: '),
    
    html.H2("Input a new house"),
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
    ),
    dcc.Input(id = 'addr', type = 'number'),
    dcc.Input(id = 'num', type = 'number'),
    html.Button('Submit', id = 'button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),

    html.H2("Delete a House and End Contract"),
    html.Div(id = 'div'),
    'Find the address of the contract you would like to delete',

    dcc.Dropdown(id = 'addies'),
    html.Button('Submit', id = 'button1'),
    html.Div(id='deleteContract-output',
             children='Enter a value and press submit'),

    html.H2("Insert new ISP"),
    dcc.Input(id = 'newIsp', type = 'text', placeholder="Insert new ISP"),
    html.Button('Submit', id = 'button2'),
    html.Div(id='addIsp-output',
             children='Enter a value and press submit'),

    html.H2("Update Speeds"),

    dcc.Dropdown(id = 'speeds'),
    dcc.Input(id = 'newSpeed', type = 'number'),
    html.Button('Submit', id = 'button3'),
    html.Div(id='updateSpeed-output',
             children='Enter a value and press submit'),
    #interval update component
    dcc.Interval(
            id='interval-update',
            interval=2*1000, # in milliseconds
            n_intervals=0
        ),
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
    [Output('speeds', 'options')], 
    [Input('interval-update', 'n_intervals')]
)
def updateSpeedDropDown(n_intervals):
    db_data = getdb()
    speed = db_data["speed"]["s_speed"]
    speeds = [{'label': i, 'value': i} for i in speed.unique()]
    return [speeds]

    #conn = proj.openConnection(r"proj.sqlite")
    #c = conn.cursor()
    #speeds = "SELECT DISTINCT s_speed FROM speed ORDER BY s_speed"
    #c.execute(speeds)
    #speeds = [{'label': str(i[0]) + " mbps", 'value': i[0]} for i in c.fetchall()]
    #proj.closeConnection(conn, r"proj.sqlite")
    #return [speeds]


#callbacks for updates
@app.callback(
    [Output('Addresses', 'options'),
    Output('addies', 'options')],
    [Input('interval-update', 'n_intervals')])
def update_type_dropdown(n_intervals):
    db_data = getdb()
    haddresses = db_data["house"]["h_address"]
    fields = [{'label': i, 'value': i} for i in haddresses]
    return fields, fields

@app.callback(
    Output("drupd-text", "children"), 
    [Input("updcont", "value")])
def update_text2(updcont):
    if updcont != None:
        cont = updcont.split(", ")
        updatecon(cont[0], cont[1], cont[2], cont[3])
        return "Updated contract to: " + cont[2] + " " + cont[1] + " $" + cont[0] + " at " + cont[3]

@app.callback(
    Output("updcont", "options"), 
    [Input("Addresses", "value"),
    Input('interval-update', 'n_intervals')])
def update_con_drop(addname, n_intervals):
    if addname != None:
        sql = """SELECT DISTINCT h_address, cpl_conname, co_ispname, cpl_locname, s_speed
                FROM
                contractsoff,
                contractsperloc,
                speed,
                house
                WHERE (co_conname = cpl_conname) AND 
                (cpl_locname = s_locname) AND 
                (h_locname = cpl_locname) AND 
                (h_address = ?)
                ORDER BY h_address"""
        df = getdbq(sql, addname)
        df["prices"] = ""
        df["print"] = ""
        for index, row in df.iterrows():
            price = round(builddb.priceOfSpeed(row["s_speed"], row["co_ispname"]),2)
            df.loc[index, "prices"] = price
            df.loc[index, "print"] = str(price) + ", " + str(row["s_speed"]) + ", " + str(row["cpl_conname"]) + ", " + str(row["h_address"])
        haddresses = df["print"]
        fields = [{'label': i, 'value': i} for i in haddresses]
        return fields
    return []

@app.callback(
    #might need to update on update contract
    Output("drout-text", "children"), 
    [Input("Addresses", "value"),
    Input('interval-update', 'n_intervals')])
def update_text(addname, n_intervals):
    if addname != None:
        sql = """select * from network where n_address = ?"""
        df = getdbq(sql, addname)
        return """Current Contract Name: {}\n
                Price: ${}\n
                Speed: {}""".format(df.loc[0]["n_conname"],df.loc[0]["n_price"], df.loc[0]["n_speed"])

@app.callback(
    Output("funnel-graph", "figure"), 
    [Input("Addresses", "value"),
    Input('interval-update', 'n_intervals')])
def update_bar_chart(addname, n_intervals):
    bars=[]
    if addname != None:
        sql = """SELECT DISTINCT h_address, cpl_conname, co_ispname, cpl_locname, s_speed
                FROM
                contractsoff,
                contractsperloc,
                speed,
                house
                WHERE (co_conname = cpl_conname) AND 
                (cpl_locname = s_locname) AND 
                (h_locname = cpl_locname) AND 
                (h_address = ?)
                ORDER BY h_address"""
        df = getdbq(sql, addname)
        df["prices"] = ""
        for index, row in df.iterrows():
             df.loc[index, "prices"] = round(builddb.priceOfSpeed(row["s_speed"], row["co_ispname"]),2)

        
        for ispname in df["co_ispname"].unique():
            test = df[df["co_ispname"] == ispname]
            bars.append(
                go.Bar(
                    x = test["s_speed"],
                    y = test["prices"],
                    text = test["cpl_conname"],
                    name = ispname))
    fig = go.Figure(data=bars)
    fig.update_layout(barmode='group',
                    xaxis_title="Price",
                    yaxis_title="Speed")
    return fig

@app.callback(
    [Output('table', 'data'),
    Output('table','columns')],
    [Input('Addresses', 'value'),
    Input('interval-update', 'n_intervals')])
def updateTable(addname, n_intervals):
    if addname != None:
        sql = """SELECT DISTINCT h_address, cpl_conname, co_ispname, cpl_locname, s_speed
                FROM
                contractsoff,
                contractsperloc,
                speed,
                house
                WHERE (co_conname = cpl_conname) AND 
                (cpl_locname = s_locname) AND 
                (h_locname = cpl_locname) AND 
                (h_address = ?)
                ORDER BY h_address"""
        df = getdbq(sql, addname)
        df["prices"] = ""
        for index, row in df.iterrows():
             df.loc[index, "prices"] = round(builddb.priceOfSpeed(row["s_speed"], row["co_ispname"]),2)
        #del df["h_address"]
        col = [{"name": i, "id": i} for i in list(df.columns)]
        return df.to_dict('records'), col
    return [], []

if __name__ == '__main__':
    app.run_server(debug=True)
