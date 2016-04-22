from bokeh.charts import Bar, output_file, show, hplot

# best support is with data in a format that is table-like
data = {
    'emotion': ['positive', 'neutral', 'negative'],
    'Number of Tweets': [8, 5, 2] 
}

# table-like data results in reconfiguration of the chart with no data manipulation
bar2 = Bar(data, values='Number of Tweets', label=['emotion'],
           title="Twitter emotion", plot_width=400)

output_file("bar.html")
show(hplot(bar2))