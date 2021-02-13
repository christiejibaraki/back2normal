var movieData = data.movieList;


function compareDate(a,b){
    if (a.releaseDate < b.releaseDate)
        return -1;
    if (a.releaseDate > b.releaseDate)
        return 1;
    return 0;
}

function compareTitle(a,b) {
    if (a.title < b.title)
        return -1;
    if (a.title > b.title)
        return 1;
    return 0;
}

function comparePopularity(a,b){
    if (a.popularity < b.popularity)
        return -1;
    if (a.popularity > b.popularity)
        return 1;
    return 0;
}

movieData.sort(compareTitle);
movieData.reverse();
movieData.sort(compareDate);
movieData.reverse();
movieData.sort(comparePopularity);
movieData.reverse();


function addMoviesToDom(){

    var src = document.getElementsByClassName("data")[0];
    src.innerHTML = "";

    for(var movieIndex=0 ; movieIndex < 200; movieIndex++){

        // create article
        var dom_article = document.createElement("ARTICLE");
        dom_article.className = "movie";

        var dom_sectionImage = document.createElement("SECTION");
        dom_sectionImage.className = "featuredImage";

        var dom_img = document.createElement("img");
        dom_img.src = 'https://image.tmdb.org/t/p/w1280/' + movieData[movieIndex].posterUrl;

        dom_sectionImage.appendChild(dom_img);

        var movieYear = document.createElement("h4");
        var year = movieData[movieIndex].releaseDate === undefined? "" : movieData[movieIndex].releaseDate.substring(0,4);
        var yearText = document.createTextNode(year);
        yearText.className = "year";
        movieYear.appendChild(yearText);
        dom_sectionImage.appendChild(movieYear);

        dom_article.appendChild(dom_sectionImage);

        var movieTitle = document.createElement("h3");
        var titleText = document.createTextNode(movieData[movieIndex].title);
        movieTitle.appendChild(titleText);
        dom_article.appendChild(movieTitle);

        var textNode = document.createElement("p");
        textNode.className = "overview";
        textNode.innerHTML = movieData[movieIndex].overview;
        dom_article.appendChild(textNode);

        var src = document.getElementsByClassName("data")[0];
        dom_article.movie = movieData[movieIndex];
        src.appendChild(dom_article);
    }
}

addMoviesToDom();


$("#closeDetail").on('click', function () {
    $("#movieDetail").hide();
});

var ascending = false;
$("#ascending").on('click', function () {

    if(ascending==true){
        this.innerHTML = '&#9661;';
        ascending = false;

        movieData.sort(comparePopularity);
        movieData.reverse();
        addMoviesToDom();

    }else{
        this.innerHTML = '&#9651;';
        ascending = true;

        movieData.sort(comparePopularity);
        addMoviesToDom();
    }
});

$(".data").on('click', '.movie', function () {

    $("#movieDetail").show();

    var genres = "";
    if(this.movie.genres !== undefined){
        var genreList = this.movie.genres;
        for(var genreIndex in genreList){

            if(genres!==""){
                genres = genres + " / ";
            }
            genres = genres + genreList[genreIndex] + " ";
        }
    }

    genres = genres + " , " + this.movie.releaseDate.substring(0,4);


    var entityString = "";
    if(this.movie.locationSet !== undefined) {
        var locationSet = this.movie.locationSet;
        for(var locationIndex in locationSet){
            if(entityString!==""){
                entityString = entityString + ", ";
            }else{
                entityString = "Places: ";
            }
            entityString = entityString + locationSet[locationIndex].name;
        }
    }

    var peopleString = "";
    if(this.movie.personSet !== undefined) {
        var personSet = this.movie.personSet;
        for(var personIndex in personSet){


            if(peopleString!==""){
                peopleString = peopleString + ", ";
            }else{
                peopleString = "People: ";
            }
            peopleString = peopleString + personSet[personIndex];
        }
    }

    var orgString = "";
    if(this.movie.organizationSet !== undefined) {
        var orgSet = this.movie.organizationSet;
        for(var orgIndex in orgSet){


            if(orgString!==""){
                orgString = orgString + ", ";
            }else{
                orgString = "Organizations: ";
            }
            orgString = orgString + orgSet[orgIndex];
        }
    }

    var container = document.getElementById('content');
    container.innerHTML = "";

    var title = document.createElement("h1");
    title.className = "content-detail";
    title.appendChild(document.createTextNode(this.movie.title));

    var genreSection = document.createElement("SECTION");
    genreSection.className  ="genre";
    var testGenres = document.createElement("h4");
    testGenres.innerHTML = genres;
    genreSection.appendChild(testGenres);

    container.appendChild(title);
    container.appendChild(genreSection);

    var contentHolder = document.createElement("SECTION");
    contentHolder.className = "contentHolder";

    var dom_sectionImage = document.createElement("SECTION");
    dom_sectionImage.className = "bigImage";

    var dom_img = document.createElement("img");
    dom_img.src = 'https://image.tmdb.org/t/p/w1280/' + this.movie.posterUrl;

    dom_sectionImage.appendChild(dom_img);
    contentHolder.appendChild(dom_sectionImage);

    var textSection = document.createElement("SECTION");
    textSection.className = "text";
    var testText = document.createElement("p");
    testText.innerHTML = this.movie.overview;
    textSection.appendChild(testText);

    // entities
    var entitySection = document.createElement("SECTION");
    entitySection.className = "entities";

    var peopleText = document.createElement("h2");
    peopleText.innerHTML = peopleString;
    entitySection.appendChild(peopleText);

    var orgText = document.createElement("h2");
    orgText.innerHTML = orgString;
    entitySection.appendChild(orgText);

    var entityText = document.createElement("h2");
    entityText.innerHTML = entityString;
    entitySection.appendChild(entityText);

    contentHolder.appendChild(textSection);
    contentHolder.appendChild(entitySection);
    container.appendChild(contentHolder);

});


$(document).ready(function () {

    // movieData.forEach(function(d){
    for(var movieIndex in movieData){

        var d = movieData[movieIndex];

        var title  = "'" + d.title + "'";


        if(d.locationSet !== undefined) {
            var locationSet = d.locationSet;
            if(locationSet[0].coords !== undefined) {
                d["geo"] = locationSet[0].coords.x + "," + locationSet[0].coords.y + "," + title.replace(/[_,;]+/g," ").replace(/\s\s+/g, ' ').trim();
            }
        }


    }


    var ndx = crossfilter(movieData);

    var mapGeo = ndx.dimension(function(d){
        return d.geo;
    });
    var mapGeoGroup = mapGeo.group().reduceCount();

    var markerMap = dc.leafletMarkerChart("#marker-map")
        .dimension(mapGeo)
        .group(mapGeoGroup)
        .width(500)
        .height(300)
        .fitOnRender(true)
        .fitOnRedraw(true)
        .popupOnHover(true)
        .popup(function (d){
            return d.key.split(',')[2];
        })
        .cluster(true);





    dc.renderAll();

    // InitChart();
    //
    // function InitChart() {
    //
    //     console.log("init chart");
    //     var barData = [{
    //         'x': 1,
    //         'y': 5
    //     }, {
    //         'x': 20,
    //         'y': 20
    //     }, {
    //         'x': 40,
    //         'y': 10
    //     }, {
    //         'x': 60,
    //         'y': 40
    //     }, {
    //         'x': 80,
    //         'y': 5
    //     }, {
    //         'x': 100,
    //         'y': 60
    //     }];
    //
    //     var vis = d3.select('#visualisation'),
    //         WIDTH = 1000,
    //         HEIGHT = 500,
    //         MARGINS = {
    //             top: 20,
    //             right: 20,
    //             bottom: 20,
    //             left: 50
    //         },
    //         xRange = d3.scale.ordinal().rangeRoundBands([MARGINS.left, WIDTH - MARGINS.right], 0.1).domain(barData.map(function (d) {
    //             return d.x;
    //         })),
    //
    //
    //         yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,
    //             d3.max(barData, function (d) {
    //                 return d.y;
    //             })
    //         ]),
    //
    //         xAxis = d3.svg.axis()
    //             .scale(xRange)
    //             .tickSize(5)
    //             .tickSubdivide(true),
    //
    //         yAxis = d3.svg.axis()
    //             .scale(yRange)
    //             .tickSize(5)
    //             .orient("left")
    //             .tickSubdivide(true);
    //
    //
    //     vis.append('svg:g')
    //         .attr('class', 'x axis')
    //         .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
    //         .call(xAxis);
    //
    //     vis.append('svg:g')
    //         .attr('class', 'y axis')
    //         .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
    //         .call(yAxis);
    //
    //     vis.selectAll('rect')
    //         .data(barData)
    //         .enter()
    //         .append('rect')
    //         .attr('x', function (d) {
    //             return xRange(d.x);
    //         })
    //         .attr('y', function (d) {
    //             return yRange(d.y);
    //         })
    //         .attr('width', xRange.rangeBand())
    //         .attr('height', function (d) {
    //             return ((HEIGHT - MARGINS.bottom) - yRange(d.y));
    //         })
    //         .attr('fill', 'grey')
    //         .on('mouseover',function(d){
    //             d3.select(this)
    //                 .attr('fill', '#4424D6' );
    //         })
    //         .on('mouseout',function(d){
    //             d3.select(this)
    //                 .attr('fill','grey');
    //         });


});