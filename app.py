from flask import Flask, render_template, request, redirect, url_for, session
import requests, json
import simplejson as json
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_notebook, output_file, show, save, reset_output
from bokeh.embed import components

from bokeh.plotting import figure, show, output_file

from bokeh.sampledata.us_states import data as states
from bokeh.io import show
from bokeh.palettes import Viridis6 as palette

from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
    FixedTicker,
    FuncTickFormatter,
    CustomJS,
    LogTicker
)

import bokeh.palettes
from bokeh.layouts import column
from bokeh.models.widgets import Slider, Select, TextInput, Dropdown
from bokeh.embed import components
from ipywidgets import interact, interactive, fixed, interact_manual
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, column, row

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_notebook
from bokeh.layouts import widgetbox, column, row

del states["HI"]
del states["AK"]

summ = pd.read_csv('overviewSum.csv')
df = pd.read_csv('testtable.csv')
def overview(states):

    state_x = [(code, states[code]["lons"]) for code in states]
    state_xsTest = sorted(state_x, key = lambda x:x[0] )
    state_xf = [i[1] for i in state_xsTest]
    state_y = [(code, states[code]["lats"]) for code in states]
    state_ysTest = sorted(state_y, key = lambda x:x[0] )
    state_yf = [i[1] for i in state_ysTest]

    summ['plot'] = summ['percent'].copy()
    summ['true'] = summ['percent'].copy()
    colors = bokeh.palettes.Blues9[::-1]
    mapper = LinearColorMapper(palette = colors, nan_color = 'white',
                                   low = 0., high = 100.)
    ticker = FixedTicker(ticks=[0, 50, 100])
    cbar = ColorBar(color_mapper=mapper, ticker=ticker,
                     label_standoff=12, border_line_color=None, location=(0,0))


    source = ColumnDataSource(data=dict(
        x=state_xf,
        y=state_yf,
        plot=summ['plot'],
        true=summ['true'],
        user = summ['user'],
        job = summ['job'],
        JobPerUser = summ['jobPerUser'],
        percent = summ['percent'],
        state=summ['state']
    ))


    p = figure( tools = "pan, zoom_in, zoom_out, hover, save,reset", toolbar_location="right",
               plot_width=800, plot_height=450)
    #title='Overview of the job market', p.title.text_font_size = '20pt'
    p.patches('x', 'y', source = source, fill_color = {'field':'plot', 'transform': mapper},  fill_alpha=0.7,
              line_color="grey", line_width=2, line_alpha=0.3)
    p.add_layout(cbar, 'right')
    ##################call back
    callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var f = cb_obj.value
    var max_val = 0
    var min_val = 0
    cb_obj['attributes']['label'] = f;
    for (i = 0; i < data['x'].length; i++) {
        data['plot'][i] =  data[f][i]
    }
    for (i=0;i < data['x'].length;i++){
        if(data['plot'][i] > max_val){
            max_val = data['plot'][i];
        }
        if(data['plot'][i] < min_val){
            min_val = data['plot'][i];
        }

    }
    for (i=0;i < data['x'].length;i++){
        data['true'][i] = data['plot'][i]
        data['plot'][i] = 100. * (data['plot'][i])/ (max_val)
    }
    source.change.emit();
    """)
    ###################

    menu = [('User Number', 'user'), ('Job Number', 'job'), ('Jobs Per User', 'JobPerUser'), ('Percent: job application habit', 'percent')]
    dropdown = Dropdown(label='Select', button_type="warning", menu=menu)
    dropdown.js_on_change('value', callback)
    hover = p.select_one(HoverTool)
    hover.point_policy = 'follow_mouse'
    hover.tooltips = [
        ("State", '@state'),
        ('value', '@true')]
    layout1=row(p, dropdown)

    df1 = df[:8]

    data = dict(
            UserID = df1['UserID'],
            Title = df1['Title'],
            Description = df1['Description'],
            Requirements = df1['Requirements'],
            City = df1['City'],
            State = df1['State']
        )
    source = ColumnDataSource(data)

    columns = [
            TableColumn(field="UserID", title="UserID"),
            TableColumn(field="Title", title="Title"),
            TableColumn(field="City", title="City"),
            TableColumn(field="State", title="State"),
            TableColumn(field="Description", title="Description"),
            TableColumn(field="Requirements", title="Requirements")

        ]
    data_table = DataTable(source=source, columns=columns, width=1000, height=230)
    layout2 = row(data_table)
    script, divs = components({'plot':layout1, 'table':layout2})
    return render_template('index.html', script = script, div = divs)



app = Flask(__name__)
@app.route('/', methods = ['GET'])
def main():
    return overview(states)

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
