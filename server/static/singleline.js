//Array used for week numbering
var weekNo = [
	1, 2, 3, 4,
	5, 6, 7, 8,
	9, 10, 11, 12,
	13, 14, 15, 16, 17
];

//Select the chart svg
//Define margin
//Calculate width and height of the drawing area
//Apprend graphic element "g" inside the svg
var chart = d3.select(".chart"),
	margin = {top: 20, right: 80, bottom: 80, left: 100},
	width = chart.attr("width") - margin.left - margin.right,
	height = chart.attr("height") - margin.top - margin.bottom,
	g = chart.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//Set ranges for x and y axes, and z (color)
var x = d3.scaleLinear().range([0, width]),
	y = d3.scaleLinear().range([height, 0]);
	z = d3.scaleOrdinal(["steelblue", "#dd1c77"]);

//Set domain for x axis, and z(color)
x.domain(d3.extent(weekNo));
z.domain(["Fall17", "Spring18"]);

//Define line function
var line = d3.line()
				.x(function(d) { return x(d.week); })
				.y(function(d) { return y(d.total); });

//Read data from 2 files, then use await() when finish reading and call assignData function
//callback function type() used for convert string to number
d3.queue()
	.defer(d3.csv, "https://raw.githubusercontent.com/jemiar/TAvisual/master/fall17data.csv", type)
	.defer(d3.csv, "https://raw.githubusercontent.com/jemiar/TAvisual/master/spring18data.csv", type)
	.await(processData);

//type function: convert string to number
function type(d) {
  	d.labtime = +d.labtime;
  	d.classtime = +d.classtime;
  	d.grading = +d.grading;
  	d.officehr = +d.officehr;
  	d.classprep = +d.classprep;
  	d.other = +d.other;
  	d.week = +d.week;
  	return d;
}

//called after reading data from 2 csv files finishes
function processData(error, dataFall17, dataSpring18) {
	if(error) throw error;

	//function used to group data by class, semester, week respectively
	function groupData(data) {
		return d3.nest()
					.key(function(d) { return d.classID; })
					.key(function(d) { return d.semester; })
					.key(function(d) { return d.week; })
					.rollup(function(v) { return {
						week: v[0].week,
						total: d3.sum(v, function(d) { return d.labtime + d.classtime + d.grading + d.officehr + d.classprep + d.other; })
						};
					})
					.entries(data);
	}

	//group Fall17 data by class, then semester and week
	var dataFall17_groupedByClass = groupData(dataFall17);
	console.log(dataFall17_groupedByClass);

	//group Spring18 data by class, then semester and week
	var dataSpring18_groupedByClass = groupData(dataSpring18);
	console.log(dataSpring18_groupedByClass);

	//function used to pad zero to missing week
	function padZero(data) {
		return data.map(function(d) {
			return {
				key: d.key,
				values: [{
					key: d.values[0].key,
					values: weekNo.map(function(w) {
						if(d.values[0].values.find(function(e) { return e.value.week == w; }))
							return d.values[0].values.find(function(e) { return e.value.week == w; }).value;
						else
							return {week: w, total: 0};
					})
				}]
			}
		});
	}

	//padding zero to fall17 data
	var dataFall17_paddedZero = padZero(dataFall17_groupedByClass);
	console.log(dataFall17_paddedZero);

	//padding zero to spring18 data
	var dataSpring18_paddedZero = padZero(dataSpring18_groupedByClass);
	console.log(dataSpring18_paddedZero);

	//merge 2 data: fall17 and spring18
	var data_Merged = d3.merge([dataFall17_paddedZero, dataSpring18_paddedZero]);
	console.log(data_Merged);

	//group data by class
	var data_Combined = d3.nest()
							.key(function(d) { return d.key; })
							.rollup(function(v) {
								return v.map(function(e) { return e.values; })
										//flatten array
										.reduce((accumulator, current) => accumulator.concat(current), []);
							})
							.entries(data_Merged);
			
	console.log(data_Combined);

	//Function to set axis y domain
	function setYDomain(data) {
		if(data.value.length > 1)
			y.domain(d3.extent(d3.merge([data.value[0].values.map(e => e.total), data.value[1].values.map(e => e.total)])));
		else
			y.domain(d3.extent(data.value[0].values.map(e => e.total)));
	}

	//Set y domain for 1st class
	setYDomain(data_Combined[0]);

	//Draw x axis
	g.append("g")
		.attr("id", "axisX")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x).ticks(17))
	.append("text")
		.attr("transform", "translate(" + (width/2) + ",30)")
		.attr("y", 8)
		.attr("dy", "0.71em")
		.attr("fill", "#000")
		.attr("text-align", "right")
		.style("font-size", "30px")
		.text("Week");

	//Draw y axis
	g.append("g")
		.attr("id", "axisY")
		.call(d3.axisLeft(y))
	.append("text")
		.attr("transform", "rotate(-90)")
		.attr("y", 0 - margin.left + 20)
		.attr("x", 0 - (height / 2) + 90)
		.attr("dy", "0.71em")
		.attr("fill", "#000")
		.style("font-size", "30px")
		.style("font-family", "sans-serif")
		.text("Working hours");

	//function to draw line chart and marker
	function draw_Line_Marker(selection) {
		//Draw line charts
		selection.append("path")
					.attr("class", "line")
					.attr("id", function(d) { return d.key; })
					.attr("d", function(d) { return line(d.values.sort(function(a, b) {return a.week - b.week; })); })
					.style("stroke", function(d) {return z(d.key); })
					.style("stroke-width", 4);

		//Draw circular markers
		selection.append("g")
					.selectAll(".marker")
					.data(function(d) { return d.values; })
					.enter()
				.append("circle")
					.attr("class", "marker")
					.attr("data-toggle", "tooltip")
					.attr("data-placement", "top")
					.attr("title", function(d) { return "Week " + d.week + ": " + d.total + " hrs"; })
					.attr("cx", line.x())
					.attr("cy", line.y())
					.attr("r", 4.0);

		//Color markers according to their semesters
		selection.selectAll("g")
					.style("stroke", function(d) { return z(d.key); })
					.style("stroke-width", 3)
					.style("fill", function(d) { return z(d.key); });

		//Add tooltip to markers
		//Because tooltip does not show up inside a svg element
		//We must set the option to show it in the <body>
		$(".marker").tooltip({ "container": "body"});
	}

	//Join data to g element
	var lineChart = g.selectAll(".lineGraphic")
						.data(data_Combined[0].value)
						.enter()
					.append("g")
						.attr("class", "lineGraphic");

	//Draw line charts and markers
	draw_Line_Marker(lineChart);

	//Append buttons to legend
	var legend = d3.select(".legend")
						.selectAll(".courseButton")
						.data(data_Combined)
						.enter()
						.append("button")
							.attr("class", "courseButton btn-sm")
						.append("text")
							.text(function(d) { return d.key; });

	//Color the 1st button
	$(".courseButton").first().css('background', 'blue').children().css('color', 'white');

	//Set event listener to course button
	d3.selectAll('.courseButton')
		.on('click', function(d, i) {
			//Set style for all buttons back to white background and black text
			d3.selectAll('.courseButton').style('background', 'white')
				.selectAll('text').style('color', 'black');
			//variable to store the ith element
			var nth_btn = '.courseButton:nth-child(' + (i + 1) + ')';
			//Set style of the clicked button to blue background and white text
			d3.select(nth_btn).style('background', 'blue')
				.select('text').style('color', 'white');
			//Set domain of y axis
			setYDomain(data_Combined[i]);
			//Animate change in y axis
			d3.select('#axisY')
				.transition().duration(500)
				.call(d3.axisLeft(y));

			//Update line chart data
			//NOTE: Need to use a parent selector. In this case 'g'
			//Do no use d3.selectAll
			//In order to use append below
			var lineChartUpdate = g.selectAll('.lineGraphic')
										.data(data_Combined[i].value);

			//Remove old data
			lineChartUpdate.exit().remove();

			//Append and merge new data
			lineChartUpdate.enter()
						.append('g')
							.attr('class', 'lineGraphic')
						.merge(lineChartUpdate);

			//Remove old line chart and marker
			d3.selectAll('.lineGraphic').selectAll('path').remove();
			d3.selectAll('.lineGraphic').selectAll('g').remove();

			//Select .lineGraphic elements
			var lineGraphicUpdate = d3.selectAll('.lineGraphic');

			//Redraw line charts and markers
			draw_Line_Marker(lineGraphicUpdate);
		});
}