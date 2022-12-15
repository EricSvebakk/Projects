import * as d3 from "d3";
import styles from "./forceGraph.module.css";

export function runForceGraph(
  container,
  linksData,
  nodesData,
  funcColor,
  setNodesPosition,
  nodesPosition,
  nodeHoverTooltip
  // hovered,
) {
  const ids = nodesData.map((a) => a.id);
  const filteredLinks = (l, myIDS) => {
    let k = l.filter(
      (d) => myIDS.includes(d.source) && myIDS.includes(d.target)
    );
    return k;
  };

  const nodes = nodesData.map((d) => Object.assign({}, d));
  const links = filteredLinks(linksData, ids).map((d) => Object.assign({}, d));

  const containerRect = container.getBoundingClientRect();
  const height = containerRect.height;
  const width = containerRect.width;

  const node_radius = 24;
  const font_size = "11px";

  const node_highlighted = "black";
  const node_not_highlighted = "white";

  const link_highlighted = "black";
  const link_not_highlighted = "#ccc";
  const arrowPath = "M 4 -1.5 L 7 0 L 4 1.5";

  const drag = (simulation) => {
    const dragstarted = (d) => {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    };

    const dragged = (d) => {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    };

    const dragended = (d) => {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    };

    return d3
      .drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  };

  //   ============================================

  // Add the tooltip element to the graph
  const tooltip = document.querySelector("#graph-tooltip");
  if (!tooltip) {
    const tooltipDiv = document.createElement("div");
    tooltipDiv.classList.add(styles.tooltip);
    tooltipDiv.style.opacity = "0";
    tooltipDiv.id = "graph-tooltip";
    document.body.appendChild(tooltipDiv);
  }
  const div = d3.select("#graph-tooltip");

  const addTooltip = (hoverTooltip, d, x, y) => {
    const sw = document.body.querySelector(".App").offsetWidth;
    const rw = document.body.querySelector(".right").offsetWidth;

    div
      .transition()
      .duration(200)
      .style("opacity", 0.9);
    div
      .html(hoverTooltip(d))
      .style("width", "160px")
      .style("left", `${sw - rw + 10}px`)
      .style("top", `${y - 28}px`);
  };

  const removeTooltip = () => {
    div
      .transition()
      .duration(200)
      .style("opacity", 0);
  };

  //   ============================================

  // console.log(width, height)

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .distance(100)
        .id((d) => d.id)
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("x", d3.forceX(width / 2))
    .force("y", d3.forceY(height / 2))
    .force("collide", d3.forceCollide(node_radius + 5));

  const svg = d3.select(container).append("svg");

  // arrow
  svg
    .append("marker")
    .attr("id", "arrowhead-not-highlighted")
    .attr("viewBox", "-0 -5 10 10")
    .attr("refX", 13)
    .attr("refY", 0)
    .attr("orient", "auto")
    .attr("markerWidth", 13)
    .attr("markerHeight", 13)
    .append("svg:path")
    .attr("d", arrowPath)
    .attr("xoverflow", "visible")
    .attr("fill", link_not_highlighted);

  // arrow
  svg
    .append("marker")
    .attr("id", "arrowhead-highlighted")
    .attr("viewBox", "-0 -5 10 10")
    .attr("refX", 13)
    .attr("refY", 0)
    .attr("orient", "auto")
    .attr("markerWidth", 13)
    .attr("markerHeight", 13)
    .append("svg:path")
    .attr("d", arrowPath)
    .attr("xoverflow", "visible")
    .attr("fill", link_highlighted);

  // background, needed for clicking
  svg
    .append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("fill", "white")
    .style("cursor", "default")
    .lower()
    .on("click", function(d) {
      exit_highlight(d);
    });

  const link = svg
    .append("g")
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    // .attr("opacity", link_not_highlighted)
    .attr("marker-end", "url(#arrowhead-not-highlighted)")
    .attr("stroke", link_not_highlighted)
    .attr("stroke-dasharray", (d) => (d.mandatory ? 0 : 5))
    .attr("stroke-width", 3);

  const node = svg
    .append("g")
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", (d) => node_radius)
    .attr("fill", (d) => funcColor(d))
    .attr("cx", (d) => {
      for (let id in nodesPosition) {
        if (parseInt(id) === parseInt(d.id)) {
          return (d.x = nodesPosition[d.id][0]);
        }
      }
      return (d.x = width / 2);
    })
    .attr("cy", (d) => {
      for (let id in nodesPosition) {
        if (parseInt(id) === parseInt(d.id)) {
          return (d.y = nodesPosition[d.id][1]);
        }
      }
      return (d.y = height / 2);
    })
    .attr("stroke", node_not_highlighted)
    .attr("stroke-width", 2)
    .style("cursor", "pointer")
    .call(drag(simulation));

  const label = svg
    .style("font-size", font_size)
    .append("g")
    .attr("class", "labels")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .text((d) => d.code)
    .style("fill", "black")
    .style("cursor", "pointer")
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "central")
    .attr("class", `fa ${styles.male}`)
    .call(drag(simulation));

  //
  const updateNodes = () => {
    let tempNodes = {};

    node.attr("id", (d) => {
      tempNodes[d.id] = [d.x, d.y];
    });

    setNodesPosition(tempNodes);
    svg.remove();
  };

  // ============================================

  //
  function set_highlight(a) {
    // hovered(a)

    node.style("stroke", (n) => {
      return n.id === a.id ? node_highlighted : node_not_highlighted;
    });

    link.style("stroke", (l) => {
      return a.id === l.source.id || a.id === l.target.id
        ? link_highlighted
        : link_not_highlighted;
    });

    link.style("marker-end", (l) => {
      return a.id === l.source.id || a.id === l.target.id
        ? "url(#arrowhead-highlighted)"
        : "url(#arrowhead-not-highlighted)";
    });
  }

  //
  function exit_highlight(d) {
    svg.style("cursor", "move");

    node.style("stroke", node_not_highlighted);
    link.style("stroke", link_not_highlighted);
    link.style("marker-end", "url(#arrowhead-not-highlighted)");
  }

  //
  function updatePos(pos, lim) {
    return Math.max(node_radius, Math.min(lim - node_radius, pos));
  }

  //
  node
    .on("dbclick", (d) => {})
    .on("mouseover", (d) => {
      set_highlight(d);
      addTooltip(nodeHoverTooltip, d, d3.event.pageX + 15, d3.event.pageY);
    })
    .on("mouseout", (d) => {
      exit_highlight(d);
      removeTooltip();
    });

  //
  simulation.on("tick", () => {
    //update link positions
    link
      .attr("x1", (d) => (d.source.x = updatePos(d.source.x, width)))
      .attr("y1", (d) => (d.source.y = updatePos(d.source.y, height)))
      .attr("x2", (d) => (d.target.x = updatePos(d.target.x, width)))
      .attr("y2", (d) => (d.target.y = updatePos(d.target.y, height)));

    // update node positions
    node
      .attr("cx", (d) => (d.x = updatePos(d.x, width)))
      .attr("cy", (d) => (d.y = updatePos(d.y, height)));

    // update label positions
    label.attr("x", (d) => d.x).attr("y", (d) => d.y);
  });

  //   ============================================

  return {
    destroy: () => {
      simulation.stop();
    },
    update: () => {
      updateNodes();
    },
    nodes: () => {
      return svg.node();
    },
  };
}
