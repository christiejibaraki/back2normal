// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// parse the date and time
// strftime('%Y-%m-%d'
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// append the svg object to the body of the page
var svg = d3.select("#groudTruth")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

//Read the data
var data = gt_records

// handle the date
function datehandle(dataset) {
    dataset.forEach(function (d) {
        // console.log(d.STD_DATE, typeof(d.STD_DATE))
        d.STD_DATE = parseDate(d.STD_DATE);
        // console.log(d.STD_DATE, typeof(d.STD_DATE))
    });
};
datehandle(data)

// filter data
var group = "60614";

function datasetGroundTruthChosen(group) {
    var ds = [];
    for (x in data) {
        // this if statement filters on zipcode and filters out any rows with NaNs for AVG7DAY_BARS
        if (data[x].ZIPCODE == group && data[x].AVG7DAY_BARS == data[x].AVG7DAY_BARS) {
            console.log(data[x])
            ds.push(data[x]);
        }
    }
    return ds;
}

data = datasetGroundTruthChosen(group)

// group the data: I want to draw one line per group
function datafunc(d) {
    var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
        .key(function (d) {
            return d.ZIPCODE;
        })
        .entries(data);

    // Add X axis --> it is a date format
    var xScale = d3.scaleTime()
        .domain(d3.extent(data, function (d) {
            return d.STD_DATE;
        }))
        .range([0, width]);

    var xaxis = d3.axisBottom()
        .ticks(d3.timeDay.every(15))
        .tickFormat(d3.timeFormat('%b %d'))
        .scale(xScale);


    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(xaxis);

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function (d) {
            return +d.// group the data: I want to draw one line per group
function datafunc(d) {
    var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
        .key(function (d) {
            return d.ZIPCODE;
        })
        .entries(data);

    // Add X axis --> it is a date format
    var xScale = d3.scaleTime()
        .domain(d3.extent(data, function (d) {
            return d.STD_DATE;
        }))
        .range([0, width]);

    var xaxis = d3.axisBottom()
        .ticks(d3.timeDay.every(15))
        .tickFormat(d3.timeFormat('%b %d'))
        .scale(xScale);


    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(xaxis);

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function (d) {
            return +d.AVG7DAY_BARS;
        })])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // color palette
    var res = sumstat.map(function (d) {
        return d.key
    }) // list of group names
    var color = d3.scaleOrdinal()
        .domain(res)
        .range(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999'])

    // Draw the line
    svg.selectAll(".line")
        .data(sumstat)
        .enter()
        .append("path")
        .attr("fill", "none")
        .attr("stroke", function (d) {
            return color(d.key)
        })
        .attr("stroke-width", 1.5)
        .attr("d", function (d) {
            return d3.line()
                .x(function (d) {
                    return xScale(d.STD_DATE);
                })
                .y(function (d) {
                    return y(+d.AVG7DAY_BARS;
                })
                (d.values)
        })
}


datafunc(data)
;
        })])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // color palette
    var res = sumstat.map(function (d) {
        return d.key
    }) // list of group names
    var color = d3.scaleOrdinal()
        .domain(res)
        .range(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999'])

    // Draw the line
    svg.selectAll(".line")
        .data(sumstat)
        .enter()
        .append("path")
        .attr("fill", "none")
        .attr("stroke", function (d) {
            return color(d.key)
        })
        .attr("stroke-width", 1.5)
        .attr("d", function (d) {
            return d3.line()
                .x(function (d) {
                    return xScale(d.STD_DATE);
                })
                .y(function (d) {
                    return y(+d.AVG7DAY_BARS);
                })
                (d.values)
        })
}


datafunc(data)
