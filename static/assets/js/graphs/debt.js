$(document).ready(function() {
    "use strict";

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 720 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var area = d3.svg.area()
        .x(function (d) {
            return x(d.date);
        })
        .y0(height)
        .y1(function (d) {
            return y(d.balance);
        });

    var svg = d3.select("#graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("/account/debt/summary/", function (error, data) {
        data.forEach(function (d) {
            d.date = parseDate(d.date);
            d.balance = +d.balance;
        });

        x.domain(d3.extent(data, function (d) {
            return d.date;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d.balance;
        })]);

        svg.append("path")
            .datum(data)
            .attr("class", "area")
            .attr("d", area);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .attr("font-weight", "bold")
            .style("text-anchor", "end")
            .text("Debt (£)");

        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", 5 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .attr("font-weight", "bold")
            .text("Total Debt");

    });

});