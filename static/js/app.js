function buildPlot(){
	var jobs_url='/api/jobs'
	d3.json(jobs_url).then(function(response){
		var data=response
		var trace={
			'x': response.map(result=>new Date(result['processed']*1000)), 
			'y': response.map(result=>result['bikes'])
			}
		var layout={
			'title': 'Activity Monitor', 
			'xaxis': {
				'title': 'Time'
				}, 
			'yaxis': {
				'title': 'Count'
				}
			}
		Plotly.newPlot("plot", [trace], layout, {'staticPlot': true});
		}
	)
}

buildPlot()