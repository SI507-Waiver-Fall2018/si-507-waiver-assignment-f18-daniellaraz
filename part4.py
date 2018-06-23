## Full Name: Daniella Raz
## Uniqname: drraz
## UMID: 86870313

import plotly
import csv
import plotly.plotly as py
import plotly.graph_objs as go

# plotly set-up
plotly.tools.set_credentials_file(username = "daniellaraz", api_key = "ooNZamadcvfla8lruAJ6")

# reading in csv file and making lists to use for plotly
nouns_list = []
count_list = []
with open('noun_data.csv') as csvfile:
    read_csv = csv.reader(csvfile)
    next(read_csv)
    for row in read_csv:
        nouns_list.append(row[0])
        count_list.append(row[1])

noun_data = [go.Bar(
        x = nouns_list,
        y = count_list
        )]

layout = go.Layout(title = "Frequency of Top Five Nouns", yaxis={'tickformat': ',d'})
fig = go.Figure(data = noun_data, layout = layout)
py.image.save_as(fig, filename = "part4_viz_image.png")
