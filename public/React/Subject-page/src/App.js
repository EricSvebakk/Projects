
import React, { Component } from "react";
import data from "./data/ifi_subjects_temp2.json";
import Subjects from "./components/Subjects";
import SemesterPlan from "./components/Semesterplan";

import { MyNavbar } from "./components/Navbar";
import { ForceGraph } from "./components/graphing/ForceGraph";
import { codeColor, semesterColor } from "./components/NodeColor";

class App extends Component {
  state = {
    selectedSubjects: [],
    nodesTopsorted: [],
    nodesPosition: [],
    semesters: [],
    sortingCategory: "",
    funcColor: codeColor,
  };

  // selects/deselects subjects to be show in force-graph
  toggleSubject = (e) => {
    const node = e.currentTarget.getAttribute("data-item");
    const temp = data.nodes.filter((a) => a.code === node)[0];

    const { selectedSubjects, forceGraphUpdater } = this.state;

    // console.log("ts!", node)
    
    if (!selectedSubjects.includes(temp)) {
      const result = this.toggleSubjectRecursive([temp]);
      const result2 = result.filter((n) => !selectedSubjects.includes(n));
      const result3 = [...new Set(result2)];

      this.setState({
        selectedSubjects: [...selectedSubjects, ...result3],
      });
    } else {
      this.setState({
        selectedSubjects: selectedSubjects.filter((sub) => sub !== temp),
      });
    }
    forceGraphUpdater();
  };

  // helper-function for toggleSubject()
  toggleSubjectRecursive = (nodeList) => {
    let result = [...nodeList];

    
    for (const node of nodeList) {
      
      let nodeUsed = node;
      let equivs = null;
      
      if (node.equivalent != null) {
        equivs = [...node.equivalent, node];
        equivs = equivs.sort((a, b) => a.code.localeCompare(b.code));
        nodeUsed = equivs[0];
        
        result.filter((a) => {
          for (const ntemp of equivs) {
            if (a.code == ntemp.code) {
              return false;
            }
          }
          return true;
        });
      }
      
      if (nodeUsed.msubs != null) {
        let rec = data.nodes.filter((n) => nodeUsed.msubs.includes(n.id));
        result = [...result, ...this.toggleSubjectRecursive(rec)];
      }

      if (nodeUsed.rsubs != null) {
        let rec = data.nodes.filter((n) => nodeUsed.rsubs.includes(n.id));
        result = [...result, ...this.toggleSubjectRecursive(rec)];
      }
      
      
      // if (equivs != null) {
        
      //   // result = []
      // }
    }
    

    return result;
  };

  // deselects all subjects
  clearSubjects = () => {
    const { forceGraphUpdater } = this.state;

    this.setState({
      selectedSubjects: [],
    });

    forceGraphUpdater();
  };

  // sets the color-mode for the force-graph
  setColorMode = (e) => {
    const mode = e.currentTarget.getAttribute("data-item");
    let temp;

    const { forceGraphUpdater, funcColor } = this.state;

    console.log(mode);

    switch (mode) {
      case "semester":
        temp = semesterColor;
        break;
      // case "points":
      //   temp = pointsColor;
      //   break;
      default:
        temp = codeColor;
        break;
    }

    if (temp !== funcColor) {
      this.setState({
        funcColor: temp,
      });
      forceGraphUpdater();
    }
  };

  // sets the function which must be called when updating forceGraph
  setForceGraphUpdater = (e) => {
    this.setState({
      forceGraphUpdater: e,
    });
  };

  //
  setTopsort = (e) => {
    this.setState({
      nodesTopsorted: e,
    });
  };

  setSemesters = (e) => {
    this.setState({
      semesters: e,
    });
  };

  chooseSort = (e) => {
    this.setState({
      sortingCategory: e.currentTarget.getAttribute("data-item"),
    });
  };

  //
  nodeHoverTooltip = (node) => {
    return node.title;
  };

  setNodesPosition = (arr) => {
    this.setState({
      nodesPosition: arr,
    });
  };

  render() {
    const {
      selectedSubjects,
      sortingCategory,
      nodesTopsorted,
      nodesPosition,
      semesters,
      funcColor,
    } = this.state;

    return (
      <div className="App">
        <MyNavbar></MyNavbar>
        <div className="app-container">
          
          
          
          <section className="left">
            
            <Subjects
              nodesData={data.nodes}
              selected={selectedSubjects}
              sortBy={sortingCategory}
              funcSelect={this.toggleSubject}
              funcSort={this.chooseSort}
              clearSubjects={this.clearSubjects}
            />
            <div className="spacer" />
            {/* <div style={{ display: "inline-block" }}>
              
              <button
                className="subject-button"
                data-item={"code"}
                onClick={this.setColorMode}
              >
                code
              </button>
              
              <button
                className="subject-button"
                data-item={"semester"}
                onClick={this.setColorMode}
              >
                semester
              </button>
              
            </div> */}
          </section>



          <section className="middle">
            <SemesterPlan
              nodesData={selectedSubjects}
              linksData={data.links}
              result={nodesTopsorted}
              funcColor={funcColor}
              setTopsort={this.setTopsort}
              setSemesters={this.setSemesters}
              sems={semesters}
            />
          </section>

          <section className="right">
            <ForceGraph
              linksData={data.links}
              nodesData={selectedSubjects}
              funcColor={funcColor}
              nodeHoverTooltip={this.nodeHoverTooltip}
              mytemp={this.setForceGraphUpdater}
              setNodesPosition={this.setNodesPosition}
              nodesPosition={nodesPosition}
            />
          </section>
        </div>
      </div>
    );
  }
}

export default App;
