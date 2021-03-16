// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// parse the date and time
// strftime('%Y-%m-%d'
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// append the svg object to the body of the page
var svg = d3.select("#vaccTime")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Read the data
var data = vacc_records
//var data = [{"index": 1345, "ZIPCODE": "60629", "STD_DATE": "2021-02-19 00:00:00", "total_doses_daily": 486, "total_doses_cumulative": 10606, "vaccine_series_completed_daily": 180, "vaccine_series_completed_percent_population": 0.018000000000000002, "population": 110029, "AVG7DAY_total_doses_daily": 357.0, "AVG7DAY_vaccine_series_completed_daily": 98.85714285714286},
//            {"index": 812, "ZIPCODE": "60617", "STD_DATE": "2021-02-19 00:00:00", "total_doses_daily": 403, "total_doses_cumulative": 8982, "vaccine_series_completed_daily": 252, "vaccine_series_completed_percent_population": 0.028999999999999998, "population": 83553, "AVG7DAY_total_doses_daily": 280.7142857142857, "AVG7DAY_vaccine_series_completed_daily": 136.42857142857142},
//            {"index": 3235, "ZIPCODE": "60661", "STD_DATE": "2021-02-19 00:00:00", "total_doses_daily": 46, "total_doses_cumulative": 2389, "vaccine_series_completed_daily": 22, "vaccine_series_completed_percent_population": 0.083, "population": 10354, "AVG7DAY_total_doses_daily": 40.57142857142857, "AVG7DAY_vaccine_series_completed_daily": 16.857142857142858}]
  //{'year': 1884, 'sex': 'F', 'name': 'John', 'n': 50, 'prop': 0.00651}
  //{"index": 2293, "ZIPCODE": "60654", "STD_DATE": "2020-12-15 00:00:00", 
  //"total_doses_daily": 0, "total_doses_cumulative": 0,
  //"vaccine_series_completed_daily": 0, "vaccine_series_completed_percent_population": 0.0,
  //"population": 20022, "AVG7DAY_total_doses_daily": NaN,
  //"AVG7DAY_vaccine_series_completed_daily": NaN}

  //2021-02-19 00:00:00
  //%Y-%m-%d %H:%M:%S
// handle the date
function datehandle(dataset){
    dataset.forEach(function(d){
        // console.log(d.STD_DATE, typeof(d.STD_DATE))
        d.STD_DATE = parseDate(d.STD_DATE);
        // console.log(d.STD_DATE, typeof(d.STD_DATE))
    });
};
datehandle(data)

// filter data
var group = "60605";

function datasetVaccLineChosen(group) {
    var ds = [];
    for (x in data) {

        if (data[x].ZIPCODE == group && data[x].AVG7DAY_total_doses_daily == data[x].AVG7DAY_total_doses_daily) {
            console.log(data[x])
            ds.push(data[x]);
        }
    }
    return ds;
}

data = datasetVaccLineChosen(group)

// group the data: I want to draw one line per group
function datafunc(d){
var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
  .key(function(d) { return d.ZIPCODE;})
  .entries(data);

  // Add X axis --> it is a date format
var x = d3.scaleLinear()
  .domain(d3.extent(data, function(d) { return d.STD_DATE; }))
  .range([ 0, width ]);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).ticks(5));

  // Add Y axis
var y = d3.scaleLinear()
  .domain([0, d3.max(data, function(d) { return +d.AVG7DAY_total_doses_daily; })])
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
          .x(function(d) { return x(d.STD_DATE); })
          .y(function(d) { return y(+d.AVG7DAY_total_doses_daily); })
          (d.values)
      })
}

//datehandle(data)
datafunc(data)

