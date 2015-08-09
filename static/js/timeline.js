var gid = d3.select("#timeline").attr("data-gid"),
    pid = d3.select("#timeline").attr("data-pid");

function splitTwo(str) {
  var words = str.split(" ");
  var str1 = "", str2 = "";
  str1 = words[0];
  var i;
  for (i = 1; i < words.length && str1.length < 35; i++) {
    str1 += " " + words[i];
  }
  for (; i < words.length; i++) {
    str2 += " " + words[i];
  }
  return [str1, str2];
}

d3.json("/gedgo/" + gid + "/timeline/" + pid + "/", function(data) {
  var events = data.events;
  if (events.length < 1) {
    $("#timeline-pod").remove();
  } else {
    var birthyear = data.start,
        deathyear = data.end,
        hscale = d3.scale.linear()
                    .domain([0, 35])
                    .range([20, 650]);

    //Width and height
    var w = 550,
        h = hscale(deathyear - birthyear);
        scale = d3.scale.linear()
                  .domain([birthyear, deathyear])
                  .range([30, h - 30]);

    // Create SVG element
    var svg = d3.select("#timeline")
       .append("svg:svg")
       .attr("width", w)
       .attr("height", h);

    svg.selectAll("line")
        .data([1])
        .enter()
        .append("line")
        .attr("x1", w/2).attr("y1", 30)
        .attr("x2", w/2).attr("y2", h - 30)
        .attr("stroke", "teal");

    svg.selectAll("circle")
        .data(events)
        .enter()
        .append("circle")
        .attr("cx", w/2)
        .attr("cy", function(d) {
            return scale(d.year);
        })
        .attr("r", 5)
        .attr("fill", function(d, i) {
          return (d.year == birthyear || d.year == deathyear) ? "teal" : "white";
        })
        .attr("stroke-width", 3)
        .attr("stroke", function(d, i) {
          return (d.type == 'personal') ? "teal" : "orange";
        });

    var newNodes = svg.selectAll("text").data(events).enter();
    
    newNodes.append("text")
        .text(function(d) {
           return '' + d.year;
          })
        .attr("x", function(d, i) {
            return (d.type == 'personal') ? w/2 - 15 : w/2 + 15;
          })
          .attr("y", function(d) {
           return scale(d.year) + 5;
          })
          .attr("text-anchor", function(d,i) {
            return (d.type == 'personal') ? "end" : "start";
          })
          .attr("font-size", "9pt")
          .attr("fill", "black")
          .attr("font-weight", "bold");
        
    newNodes.append("text")
        .text(function(d) {
           return splitTwo(d.text)[0];
          })
        .attr("x", function(d, i) {
            return (d.type == 'personal') ? w/2 + 15 : w/2 - 15;
          })
          .attr("y", function(d) {
           return scale(d.year) + 5;
          })
          .attr("text-anchor", function(d,i) {
            return (d.type == 'personal') ? "start" : "end";
          })
          .attr("font-size", "9pt")
          .attr("fill", "gray");    
          
    newNodes.append("text")
        .text(function(d) {
           return splitTwo(d.text)[1];
          })
        .attr("x", function(d, i) {
            return (d.type == 'personal') ? w/2 + 20 : w/2 - 20;
          })
          .attr("y", function(d) {
           return scale(d.year) + 20;
          })
          .attr("text-anchor", function(d,i) {
            return (d.type == 'personal') ? "start" : "end";
          })
          .attr("font-size", "9pt")
          .attr("fill", "gray");
  }
});
