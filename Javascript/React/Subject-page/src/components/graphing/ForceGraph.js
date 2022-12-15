import React from "react";
import { runForceGraph } from "./ForceGraphGenerator";
import styles from "./forceGraph.module.css";

export function ForceGraph({
  linksData,
  nodesData,
  nodeHoverTooltip,
  mytemp,
  funcColor,
  setNodesPosition,
  nodesPosition,
}) {
  const containerRef = React.useRef(null);

  // let text = "text"
  // let hovered = (node) => {
    
  //   text = <div style={{padding: "10px", fontSize:"12pt", zIndex:100}}>{node.title}</div>
  //   console.log("h!", node.title, text)
  // }
  
  React.useEffect(() => {
    let destroyFn;

    if (containerRef.current) {
      const { destroy, update, nodes } = runForceGraph(
        containerRef.current,
        linksData,
        nodesData,
        funcColor,
        setNodesPosition,
        nodesPosition,
        nodeHoverTooltip,
        // hovered
      );
      destroyFn = destroy;

      nodes();

      mytemp(update);
    }

    return destroyFn;
  }, [nodesData, funcColor]);

  return (
    <>
      <div ref={containerRef} className={styles.container} />
      {/* <div className={styles.container}>{text}</div> */}
    </>
  );
}
