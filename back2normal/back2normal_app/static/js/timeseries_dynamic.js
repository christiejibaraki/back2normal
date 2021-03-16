
var data4 = vacc_records

// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3
    .select("#dynamic_series")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg4 = svg
    .append("svg")
    .attr("id", "cvg_svgC4")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g");
// .attr("transform", "translate(" + +")");

// -------------------------------Data manipulation--------
const parse = d3.timeParse("%Y-%m-%d");

const parse4 = d3.timeParse("%Y-%m-%d %H:%M:%S")

//test if new parse works
// data4.forEach((element) => {
//     console.log("pre", element.STD_DATE, "is", typeof(element.STD_DATE));
//     console.log('post parse', parse4(element.STD_DATE), "is", typeof(parse4(element.STD_DATE)));
// });

//rename columns of data 4
data4 = data4.map((datum) =>{
    datum.date = parse4(datum.STD_DATE);
    datum.value = datum.AVG7DAY_total_doses_daily
    return datum
})

//filter out NaNs
function filterNaNs(dataset) {
    var filtered_data = [];
    for (x in dataset) {
        if (dataset[x].value == dataset[x].value) {
            filtered_data.push(dataset[x]);
        }
    }
    return filtered_data
}

data4 = filterNaNs(data4)

//filter on zip function
function filterOnZip(selected_ZIP) {
    var filtered_data = [];
    for (x in data4) {
        if (data4[x].ZIPCODE == selected_ZIP) {
            filtered_data.push(data4[x]);
        }
    }
    return filtered_data
}


// -------------------------------Data manipulation ends--------
// Add X axis --> it is a date format
var xAxisScale = d3
    .scaleTime()
    .domain(
        d3.extent(data4, function (d) { //replaced data3 with data4
            return d.date;
        })
    )
    .range([0, width]);

svg
    .append("g")
    .attr("class", "myXaxis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xAxisScale));

// Add Y axis
var yAxisScale = d3
    .scaleLinear()
    .domain([
        0,
        d3.max(data4, function (d) { //replaced data3 with data4
            return +d.value;
        })
    ])
    .range([height, 0]);

svg.append("g").call(d3.axisLeft(yAxisScale));


function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


function scatter(selected_ZIP) {

    d3.select("#cvg_svgC4").selectAll("path").remove();

    subset_data = filterOnZip(selected_ZIP)

    ranCol = getRandomColor()
    svg4
        .append("path")
        .datum(subset_data) //replaced data3 with data4
        .attr("fill", "none")
        .attr("stroke", "none")
        .attr("stroke-width", 2)
        .attr(
            "d",
            d3
                .line()
                .x(function (d) {
                    return xAxisScale(d.date);
                })
                .y(function (d) {
                    return yAxisScale(d.value);
                })
        )
        .style("stroke", ranCol);

    svg4
        .select(".myXaxis")
        .transition()
        .duration(800)
        .attr("opacity", "1")
        .call(d3.axisBottom(xAxisScale));

}
