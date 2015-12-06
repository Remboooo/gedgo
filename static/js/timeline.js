var gid = $("#timeline").attr("data-gid"),
    pid = $("#timeline").attr("data-pid");

function capitalizeFirst(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function wordwrap(textnode, x, y, width, padding, linePadding) {
	var x_pos = x,
		y_pos = y,
		boxwidth = width,
		fz = parseInt(window.getComputedStyle(textnode)['font-size']);

    var line_height = fz + linePadding;

    var wrapping = textnode.cloneNode(false);
    wrapping.setAttributeNS(null, 'x', x_pos + padding);
    wrapping.setAttributeNS(null, 'y', y_pos + padding);

    var testing = wrapping.cloneNode(false);
    testing.setAttributeNS(null, 'visibility', 'hidden'); // Comment this out to debug

    var testingTSPAN = document.createElementNS(null, 'tspan');
    var testingTEXTNODE = document.createTextNode(textnode.textContent);
    testingTSPAN.appendChild(testingTEXTNODE);

    testing.appendChild(testingTSPAN);
		var tester = document.getElementsByTagName('svg')[0].appendChild(testing);
    
    var words = textnode.textContent.split(" ");
    var line = line2 = "";
    var linecounter = 0;
	var testwidth;

    for (var n = 0; n < words.length; n++) {
		line2 = line + words[n] + " ";
		testing.textContent = line2;
		testwidth = testing.getBBox().width;
        if ((testwidth + 2*padding) > boxwidth) {
            testingTSPAN = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
            testingTSPAN.setAttributeNS(null, 'x', x_pos + padding);
            testingTSPAN.setAttributeNS(null, 'dy', line_height);
            
            testingTEXTNODE = document.createTextNode(line);
            testingTSPAN.appendChild(testingTEXTNODE);
            wrapping.appendChild(testingTSPAN);

            line = words[n] + " ";
            linecounter++;
        } else {
            line = line2;
        }
    }

    var testingTSPAN = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
    testingTSPAN.setAttributeNS(null, 'x', x_pos + padding);
    testingTSPAN.setAttributeNS(null, 'dy', line_height);

    var testingTEXTNODE = document.createTextNode(line);
    testingTSPAN.appendChild(testingTEXTNODE);

    wrapping.appendChild(testingTSPAN);

	testing.parentNode.removeChild(testing);
	textnode.parentNode.replaceChild(wrapping,textnode);

	//return (linecounter+1) * line_height;
	return wrapping;
}

$.getJSON("/gedgo/" + gid + "/timeline/" + pid + "/", function(data) {
  var events = data.events;
  if (events.length < 1) {
    $("#timeline-pod").remove();
  } else {
	var start = data.start,
		end = data.end;

	var hscale = function(timestamp) {
		return 20 + 630 * (timestamp / (35 /* years */ * 31556926 /* seconds/year */));
	}

    var w = 300,
        h = hscale(end - start);

	var textLineDist = 35;

	var scale = function(timestamp) {
		return 30 + (((timestamp - start) / (end - start)) * (h - 60));
	}

    var r = Raphael("timeline", w, h);

	var lineX = w - 10;
	r.path("M" + lineX + "," + 30 + "L" + lineX + "," + (h - 30))
	 .attr({
		       "stroke": "teal",
			   "stroke-width": .5,
	       });


	var nodes = [];

	events.sort(function(a, b) {return a.timestamp - b.timestamp;});

	$(events).each(function (i, evt) {
		var anchorY = scale(evt.timestamp);
		var textColor = evt.type == "personal" ? "black" : "gray";
		var t = r.text(lineX - textLineDist - 20, anchorY, capitalizeFirst(evt.text)).attr({
			"text-anchor": "end",
			"font-size": "14pt",
			"color": textColor,
		});
		t.node = wordwrap(t.node, lineX - textLineDist - 20, anchorY, lineX - textLineDist - 20, 0, 0);
		t.attr("y", anchorY);

		var year = r.text(lineX - 28, anchorY, evt.year).attr({"font-size": "10pt", "text-anchor": "end"});

		var anchor = r.set();

		var nodeColor = evt.type == "personal" ? "orange" : "teal";

		var outer = r.circle(lineX, anchorY, 7).attr({"fill": nodeColor, "stroke": "none"});
		var inner = r.circle(lineX, anchorY, 4).attr({"fill": "white", "stroke": "none"});
		anchor.push(outer, inner);

		var node = r.set();
		node.push(t, year);
		
		nodes.push({"anchor": anchor, "node": node, "text": evt.text});
	});

	console.log(nodes);

	var overlap = function(a, b, margin) {
		aBox = a.getBBox();
		bBox = b.getBBox();
		if (bBox.y < aBox.y2 + margin) {
			return (aBox.y2 + margin) - bBox.y;
		} else {
			return 0;
		}
	};

	var moveIterations = 0;
	var somethingMoved = false;

	do {
		somethingMoved = false;
		for (var i = 0; i < nodes.length - 1; i++) {
			var first = nodes[i].node;
			var second = nodes[i+1].node;
			var firstHeight = first.getBBox().height/2;
			var firstY = first.getBBox().y + firstHeight;
			var secondHeight = second.getBBox().height/2;
			var secondY = second.getBBox().y + secondHeight;
			var overlapY = overlap(first, second, 10);
			if (overlapY > 0) {
				var newFirstY = Math.max(20 + firstHeight, firstY - overlapY*.5 - 1);
				var firstYDelta = firstY - newFirstY;
				var newSecondY = Math.min(h - secondHeight - 20, secondY + overlapY*.5 + 1);
				var secondYDelta = secondY - newSecondY;

				var deltaDelta = secondYDelta + firstYDelta;

				if (deltaDelta > 0) {
					// Second node bumping into the bottom; add some delta to first node going up
					newFirstY -= deltaDelta;
				}
				if (deltaDelta < 0) {
					// First node bumping into the top; add some delta to second node going down
					newSecondY -= deltaDelta;
				}

				first.attr("y", newFirstY);
				second.attr("y", newSecondY);

				// WTFBBQ fix: objects don't actually end up where we want them to, there's some kind of offset.
				// So find out what that offset is, and correct for it.

				var firstActualY = first.getBBox().y + first.getBBox().height/2;
				first.attr("y", newFirstY + (newFirstY - firstActualY));

				var secondActualY = second.getBBox().y + second.getBBox().height/2;
				second.attr("y", newSecondY + (newSecondY - secondActualY));

				somethingMoved = true;
			}
		}
	} while (somethingMoved && ++moveIterations < 100);

	// Draw some lines
	for (var i = 0; i < nodes.length - 1; i++) {
		var anchor = nodes[i].anchor;
		var anchorY = anchor.getBBox().y + anchor.getBBox().height/2;
		
		var node = nodes[i].node;
		var nodeY = node.getBBox().y + node.getBBox().height/2;

		if (Math.abs(nodeY - anchorY) > 5) {
			r.path("M" + (lineX - textLineDist + 10) + "," + nodeY + "L" + (lineX) + "," + anchorY)
			 .attr({
						"stroke": "rgb(.1, .1, .1)",
						"stroke-width": ".25px",
					})
			.toBack();
		}
	}
  }
});
