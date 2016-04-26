from bokeh.charts import Bar, output_file, show, hplot
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

def plot(sentiment):
	# best support is with data in a format that is table-like
	data = {
	    'emotion': ['positive', 'neutral', 'negative'],
	    'Number of Tweets': [sentiment[0].pos, sentiment[0].neut, sentiment[0].neg] 
	}
	# table-like data results in reconfiguration of the chart with no data manipulation
	bar2 = Bar(data, values='Number of Tweets', label=['emotion'],
	           title="Twitter emotion", plot_width=400)

	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	script, div = components(bar2, INLINE)

	bar = [script,div,js_resources,css_resources]

	return bar