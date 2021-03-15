// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#vaccTime")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Read the data
var data = [
  {'year': 1880, 'sex': 'F', 'name': 'Helen', 'n': 636, 'prop': 0.00651},
  {'year': 1881, 'sex': 'F', 'name': 'Helen', 'n': 241, 'prop': 0.00246},
  {'year': 1882, 'sex': 'F', 'name': 'Helen', 'n': 117, 'prop': 0.00119},
  {'year': 1883, 'sex': 'F', 'name': 'Helen', 'n': 636, 'prop': 0.00651},
  {'year': 1884, 'sex': 'F', 'name': 'Helen', 'n': 700, 'prop': 0.00651},
  {'year': 1880, 'sex': 'F', 'name': 'John', 'n': 400, 'prop': 0.00651},
  {'year': 1881, 'sex': 'F', 'name': 'John', 'n': 500, 'prop': 0.00246},
  {'year': 1882, 'sex': 'F', 'name': 'John', 'n': 200, 'prop': 0.00119},
  {'year': 1883, 'sex': 'F', 'name': 'John', 'n': 100, 'prop': 0.00651},
  {'year': 1884, 'sex': 'F', 'name': 'John', 'n': 50, 'prop': 0.00651}
]

//d3.csv("data.csv", function(data) {

// group the data: I want to draw one line per group
function datafunc(d){
var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
  .key(function(d) { return d.name;})
  .entries(data);

  // Add X axis --> it is a date format
var x = d3.scaleLinear()
  .domain(d3.extent(data, function(d) { return d.year; }))
  .range([ 0, width ]);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).ticks(5));

  // Add Y axis
var y = d3.scaleLinear()
  .domain([0, d3.max(data, function(d) { return +d.n; })])
  .range([ height, 0 ]);
svg.append("g")
  .call(d3.axisLeft(y));

  // color palette
var res = sumstat.map(function(d){ return d.key }) // list of group names
var color = d3.scaleOrdinal()
  .domain(res)
  .range(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999'])

  // Draw the line
svg.selectAll(".line")
    .data(sumstat)
    .enter()
    .append("path")
      .attr("fill", "none")
      .attr("stroke", function(d){ return color(d.key) })
      .attr("stroke-width", 1.5)
      .attr("d", function(d){
        return d3.line()
          .x(function(d) { return x(d.year); })
          .y(function(d) { return y(+d.n); })
          (d.values)
      })
}

datafunc(data)

