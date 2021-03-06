/*
Code adapted from
diethardsteiner Block 3287802
http://bl.ocks.org/diethardsteiner/3287802
*/

var datasetPieChart = demographic_data;

var group = "60637";

pie_labels = {
    'pct_hispanic': 'Hispanic',
    'pct_asian': 'Asian',
    'pct_black': 'Black',
    'pct_white': 'White',
    'pct_pacific_islander': 'Pacific Islander',
    'pct_american_indian': 'American Indian',
    'pct_other_race': 'Other'
}

function datasetPieChosen(group) {
    var ds = [];
    for (x in datasetPieChart) {

        if (datasetBarChart[x].ZIPCODE == group) {
            if (['pct_hispanic', 'pct_asian', 'pct_black', 'pct_white', 'pct_pacific_islander', 'pct_american_indian', 'pct_other_race'].includes(datasetBarChart[x].CATEGORY)) {
                ds.push(datasetBarChart[x]);
            }
        }
    }
    return ds;
}


function dsPieChartBasics() {

    var width = 365,
        height = 365,
        outerRadius = Math.min(width, height) / 2,
        innerRadius = outerRadius * .999,
        // for animation
        innerRadiusFinal = outerRadius * .10,
        innerRadiusFinal3 = outerRadius * .08,
        color = d3.scale.category20c()    //builtin range of colors
    ;
    return {

        width: width,
        height: height,
        outerRadius: outerRadius,
        innerRadius: innerRadius,
        innerRadiusFinal: innerRadiusFinal,
        innerRadiusFinal3: innerRadiusFinal3,
        color: color

    }
        ;
}

function dsPieChart() {

    var pie_data_subset = datasetPieChosen(group)

    var basics =  dsPieChartBasics()

    var width = basics.width,
        height = basics.height,
        outerRadius = basics.outerRadius,
        innerRadius = basics.innerRadius,
        innerRadiusFinal = basics.innerRadiusFinal,
        innerRadiusFinal3 = basics.innerRadiusFinal3,
        color = basics.color;

    var vis = d3.select("#pieChart")
        .append("svg:svg")              //create the SVG element inside the <body>
        .data([pie_data_subset])                   //associate our data with the document
        .attr("width", width)           //set the width and height of our visualization (these will be attributes of the <svg> tag
        .attr("height", height)
        .append("svg:g")                //make a group to hold our pie chart
        .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")")    //move the center of the pie chart from 0, 0 to radius, radius
    ;

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
        .outerRadius(outerRadius).innerRadius(innerRadius);

    // for animation
    var arcFinal = d3.svg.arc().innerRadius(innerRadiusFinal).outerRadius(outerRadius);
    var arcFinal3 = d3.svg.arc().innerRadius(innerRadiusFinal3).outerRadius(outerRadius);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
        .value(function (d) {
            return d.VALUE;
        });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
        .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
        .attr("class", "slice")    //allow us to style things in the slices (like text)
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
    ;

    arcs.append("svg:path")
        .attr("fill", function (d, i) {
            return color(i);
        }) //set the color for each slice to be chosen from the color function defined above
        .attr("d", arc)     //this creates the actual SVG path using the associated data (pie) with the arc drawing function
        .append("svg:title") //mouseover title showing the figures
        .text(function (d) {
            return d.data.CATEGORY + ": " + formatAsPercentage1Dec(d.data.VALUE/100);
        });

    d3.selectAll("g.slice").selectAll("path").transition()
        .duration(750)
        .delay(10)
        .attr("d", arcFinal)
    ;

    // Add a label to the larger arcs, translated to the arc centroid and rotated.
    // source: http://bl.ocks.org/1305337#index.html
    arcs.filter(function (d) {
        return d.endAngle - d.startAngle > .2;
    })
        .append("svg:text")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
            return "translate(" + arcFinal.centroid(d) + ")rotate(" + angle(d) + ")";
        })
        //.text(function(d) { return formatAsPercentage(d.value); })
        .text(function (d) {
            return pie_labels[d.data.CATEGORY] + ": " + formatAsPercentage1Dec(d.data.VALUE/100);
        })
    ;

    // Computes the label angle of an arc, converting from radians to degrees.
    function angle(d) {
        var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
        return a > 90 ? a - 180 : a;
    }

    function mouseover() {
        d3.select(this).select("path").transition()
            .duration(750)
            //.attr("stroke","red")
            //.attr("stroke-width", 1.5)
            .attr("d", arcFinal3)
        ;
    }

    function mouseout() {
        d3.select(this).select("path").transition()
            .duration(750)
            //.attr("stroke","blue")
            //.attr("stroke-width", 1.5)
            .attr("d", arcFinal)
        ;
    }

}

dsPieChart();

function updatePieChart(group) {

    var pie_data_subset = datasetPieChosen(group)

    var basics =  dsPieChartBasics()

    var width = basics.width,
        height = basics.height,
        outerRadius = basics.outerRadius,
        innerRadius = basics.innerRadius,
        innerRadiusFinal = basics.innerRadiusFinal,
        innerRadiusFinal3 = basics.innerRadiusFinal3,
        color = basics.color;

    var vis = d3.select("#pieChart svg")
        // .append("svg:svg")              //create the SVG element inside the <body>
        .data([pie_data_subset])                   //associate our data with the document
        .attr("width", width)           //set the width and height of our visualization (these will be attributes of the <svg> tag
        .attr("height", height)
        .append("svg:g")                //make a group to hold our pie chart
        .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")")    //move the center of the pie chart from 0, 0 to radius, radius
    ;

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
        .outerRadius(outerRadius).innerRadius(innerRadius);

    // for animation
    var arcFinal = d3.svg.arc().innerRadius(innerRadiusFinal).outerRadius(outerRadius);
    var arcFinal3 = d3.svg.arc().innerRadius(innerRadiusFinal3).outerRadius(outerRadius);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
        .value(function (d) {
            return d.VALUE;
        });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
        .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
        .attr("class", "slice")    //allow us to style things in the slices (like text)
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
    ;

    arcs.append("svg:path")
        .attr("fill", function (d, i) {
            return color(i);
        }) //set the color for each slice to be chosen from the color function defined above
        .attr("d", arc)     //this creates the actual SVG path using the associated data (pie) with the arc drawing function
        .append("svg:title") //mouseover title showing the figures
        .text(function (d) {
            return d.data.CATEGORY + ": " + formatAsPercentage1Dec(d.data.VALUE/100);
        });

    d3.selectAll("g.slice").selectAll("path").transition()
        .duration(350)
        .delay(10)
        .attr("d", arcFinal)
    ;

    // Add a label to the larger arcs, translated to the arc centroid and rotated.
    // source: http://bl.ocks.org/1305337#index.html
    arcs.filter(function (d) {
        return d.endAngle - d.startAngle > .2;
    })
        .append("svg:text")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
            return "translate(" + arcFinal.centroid(d) + ")rotate(" + angle(d) + ")";
        })
        //.text(function(d) { return formatAsPercentage(d.value); })
        .text(function (d) {
            return pie_labels[d.data.CATEGORY] + ": " + formatAsPercentage1Dec(d.data.VALUE/100);
        })
    ;

    // Computes the label angle of an arc, converting from radians to degrees.
    function angle(d) {
        var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
        return a > 90 ? a - 180 : a;
    }

    function mouseover() {
        d3.select(this).select("path").transition()
            .duration(750)
            .attr("d", arcFinal3)
        ;
    }

    function mouseout() {
        d3.select(this).select("path").transition()
            .duration(750)
            .attr("d", arcFinal)
        ;
    }
}