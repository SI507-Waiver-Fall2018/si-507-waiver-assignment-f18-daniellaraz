## Full Name: Daniella R. Raz
## Uniqname: drraz
## UMID: 86870313

# Imports -- you may add others but do not need to
import plotly
import csv
import plotly.plotly as py
import plotly.graph_objs as go

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

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

layout = go.Layout(title = "Frequency of Top Five Nouns")
fig = go.Figure(data = noun_data, layout = layout)
py.image.save_as(fig, filename = "part4_viz_image.png")
