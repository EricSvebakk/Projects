import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

export function SemesterPlan({
  nodesData,
  linksData,
  result: sortedNodes,
  sems,
  setTopsort,
  setSemesters,
  funcColor,
}) {
  const containerRef = React.useRef("huurdur");

  //
  React.useEffect(() => {
    const ids = nodesData.map((a) => a.id);
    const links = linksData.filter(
      (d) => ids.includes(d.source) && ids.includes(d.target)
    );

    if (containerRef.current) {
		
		// nodesData.sort((n, m) =>
		// n.code.localeCompare(m.code) ? -1 : 1
    	// )
		
      let result = topSort(nodesData, links);

      setTopsort(result);
    //   console.log("sort result", result);
    }
  }, [nodesData]);

  //
  React.useEffect(() => {
    if (containerRef.current) {
      let result = getSems(sortedNodes, funcColor);

      setSemesters(result);
      console.log("sem result", result);
    }
  }, [sortedNodes, funcColor]);

  return (
    <table className="semester-table">
      <thead>
        <tr key={"header"}>
          <th colSpan={3} style={{ textAlign: "center" }}>
            semester plan
          </th>
        </tr>
      </thead>
      <tbody>{sems}</tbody>
    </table>
  );
}

export default SemesterPlan;

//
function getSems(nodes, funcColor) {
  let remainingNodes = nodes.slice();
  let allSems = [];
  let type = "";

  console.log("\n\n");

  //
  while (remainingNodes.length > 0) {
    let semester = [];
    let totPoints = 0;
    let i = 0;

    type = type === "høst" ? "vår" : "høst";

    // console.log("remaining", remainingNodes, type);

    //
    while (i < remainingNodes.length && totPoints < 30) {
      let node = remainingNodes[i];
      let reqs = get_reqs_recursive([node], nodes);
      reqs = reqs.filter((n) => node !== n);

      //
      if (node.semester.toLowerCase().includes(type)) {
        let result = reqs.filter((n) => semester.includes(n));

        //
        if (result.length === 0 && totPoints + node.points <= 30) {
          semester.push(node);
          totPoints += node.points;

        //   console.log("sem sub added", node, semester);
        }
      }

      i++;
    }

    //
    if (totPoints > 0) {
      allSems.push(semester.slice());
      remainingNodes = remainingNodes.filter((n) => !semester.includes(n));
    }
  }

//   console.log("the sems", allSems);

  let i = 0;
  let elems = [];

  //
  while (i < allSems.length) {
    let sem = allSems[i].slice().reverse();
    let totPoints = 0;
    let r = [];

    //
    while (totPoints < 30 && sem.length > 0) {
      let temp = sem.pop();
      if (temp) {
        totPoints += temp.points;
        r.push(temp);
      }
    }
	
    //
	let j = 0;
    r = r.map((node) => {
		j++;
      let styleOuter = {
        padding: "3px",
      };
	  
      let style = {
        backgroundColor: funcColor(node),
        textAlign: "center",
        outline: "1px solid black",
        padding: "5px",
      };
	  
      return (
        <td key={"sp"+i+(j++)}colSpan={node.points / 10} style={styleOuter}>
          <div style={style}>{node.code}</div>
        </td>
      );
    });

    //
    while (totPoints < 30) {
      r.push(<td key={"sp"+i+(j++)}></td>);
      totPoints += 10;
    }

    //
    elems.push(
      <tr key={"sp"+i} style={{ border: "none" }}>
        {r}
      </tr>
    );
    i++;
  }

  return elems;
}

//
function get_reqs_recursive(nodeList, allNodes) {
  let result = nodeList;

  for (const node of nodeList) {
    if (node.msubs !== null) {
      // console.log("allnodes!", allNodes)
      let rec = allNodes.filter((n) => node.msubs.includes(n.id));
      let temp = get_reqs_recursive(rec, allNodes);
      result = [...result, ...temp];
    }

    if (node.rsubs !== null) {
      let rec = allNodes.filter((n) => node.rsubs.includes(n.id));
      let temp = get_reqs_recursive(rec, allNodes);
      result = [...result, ...temp];
    }
  }
  return result;
}

//
function topSort(nodes, links) {
  const ids = nodes.map((a) => a.id);
  let remainingLinks = links.filter(
    (d) => ids.includes(d.source) && ids.includes(d.target)
  );

  let S = nodes.filter((n) => !links.map((l) => l.target).includes(n.id));
  let L = [];

  // console.log(nodes.map((n) => n.id), S.map((n) => n.id))

  while (S.length > 0) {
    const nTemp = S.sort((n, m) =>
      n.code.localeCompare(m.code) ? -1 : 1
    ).pop();
    L.push(nTemp);

    // console.log("nTemp", nTemp.code, remainingLinks)

    for (const mTemp of nodes) {
      let link = areNodesLinked(nTemp, mTemp, remainingLinks);

      if (!link) continue;

      remainingLinks = remainingLinks.filter((l) => l !== link);

      // console.log("mTemp", mTemp.code)

      if (remainingLinks.filter((l) => l.target === mTemp.id).length === 0) {
        S.push(mTemp);
      }
    }
  }

  if (remainingLinks.length > 0) {
    // console.log("result?", remainingLinks)
    return "error!";
  }

  return L;
}

//
function areNodesLinked(n1, n2, links) {
  for (const l of links) {
    if (l.source === n1.id && l.target === n2.id) return l;
    if (l.source === n2.id && l.target === n1.id) return l;
  }

  return false;
}
