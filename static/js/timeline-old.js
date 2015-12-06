var gid = d3.select("#timeline").attr("data-gid"),
    pid = d3.select("#timeline").attr("data-pid");

function wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}

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
                    .domain([0, 35 * 31556926]) // 35 years
                    .range([20, 650]);

    //Width and height
    var w = 300,
        h = hscale(deathyear - birthyear);
        scale = d3.scale.linear()
                  .domain([birthyear, deathyear])
                  .range([30, h - 30]);

    // Create SVG element
    var svg = d3.select("#timeline")
       .append("svg:svg")
       .attr("width", w)
       .attr("height", h);

	var lineX = w - 50;

    svg.selectAll("line")
        .data([1])
        .enter()
        .append("line")
        .attr("x1", lineX).attr("y1", 30)
        .attr("x2", lineX).attr("y2", h - 30)
        .attr("stroke", "teal");

    svg.selectAll("circle")
        .data(events)
        .enter()
        .append("circle")
        .attr("cx", lineX)
        .attr("cy", function(d) {
            return scale(d.timestamp);
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
            return lineX + 15;
          })
          .attr("y", function(d) {
           return scale(d.timestamp) + 5;
          })
          .attr("text-anchor", function(d,i) {
            return "start";
          })
          .attr("font-size", "9pt")
          .attr("fill", "black")
          .attr("font-weight", "bold");
        
    newNodes.append("text")
        .text(function(d) {
			console.log(d.year + ": " + d.text);
           return d.text;
          })
        .attr("x", function(d, i) {
            return lineX - 15;
          })
          .attr("y", function(d) {
           return scale(d.timestamp) + 5;
          })
		  .attr("dy", function(d) {
			  return 0;
		  })
          .attr("text-anchor", function(d,i) {
            return "end";
          })
          .attr("font-size", "9pt")
          .attr("fill", "gray");
          //.call(wrap, 200);    
          
  }
});
