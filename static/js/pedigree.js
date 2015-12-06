var gid = d3.select("#pedigree-tree").attr("data-gid"),
    pid = d3.select("#pedigree-tree").attr("data-pid");

d3.json("/gedgo/" + gid + "/pedigree/" + pid + "/", function(treeData) {

  // Create a svg canvas
  var vis = d3.select("#pedigree-tree").append("svg:svg")
    .attr("width", 500)
    .attr("height", 750)
    .append("svg:g")
    .attr("transform", "translate(20, -90)");

  // Create a tree "canvas"
  var gid = treeData.gid;
  var tree = d3.layout.tree()
    .size([800,100]);

  var diagonal = d3.svg.diagonal()
    // change x and y (for the left to right tree)
    .projection(function(d) { return [d.y, d.x]; });

  // Preparing the data for the tree layout, convert data into an array of nodes
  var nodes = tree.nodes(treeData);
  // Create an array with all the links
  var links = tree.links(nodes);

  var link = vis.selectAll("pathlink")
    .data(links)
    .enter().append("svg:path")
    .attr("d", diagonal);

  var node = vis.selectAll("g.node")
    .data(nodes)
    .enter().append("svg:g")
    .attr("transform", function(d) {
        return "translate(" + d.y + "," + d.x + ")"; });

  node.append("svg:rect")
    .attr("rx", 10)
    .attr("ry", 10)
    .attr("y", -35)
    .attr("x", -20)
    .attr("width", 1000)
    .attr("height", 60);

  node.append("svg:a")
    .attr("xlink:href", function(d) { return "/gedgo/" + gid + "/" + d.id; })
    .append("text")
    .attr("dx", -10)
    .attr("dy", -18)
    .attr("text-anchor", "start")
    .text(function(d) { return d.first_name; })
    .attr("font-family", "sans-serif")
    .attr("font-size", "11pt");

  node.append("svg:a")
    .attr("xlink:href", function(d) { return "/gedgo/" + gid + "/" + d.id; })
    .append("text")
    .attr("dx", -10)
    .attr("dy", 0)
    .attr("text-anchor", "start")
    .text(function(d) { return d.last_name; })
    .attr("font-family", "sans-serif")
    .attr("font-size", "11pt");


  node.append("svg:text")
    .attr("dx", -10)
    .attr("dy", 18)
    .attr("text-anchor", "start")
    .text(function(d) { return d.span; })
    .attr("font-family", "sans-serif")
    .attr("font-size", "11pt")
    .attr("fill", "gray");
});

