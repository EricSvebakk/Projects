import React, { Component } from "react";

import "bootstrap/dist/css/bootstrap.min.css";

class Subjects extends Component {
  render() {
    const { nodesData, selected, sortBy, funcSelect, funcSort } = this.props;

    let data = nodesData.sort((a, b) => {
      switch (sortBy) {
        case "code":
          return a.code.localeCompare(b.code);
        case "title":
          return a.title.localeCompare(b.title);
        case "points":
          return b.points - a.points;
        case "semester":
          return a.semester.localeCompare(b.semester);
        case "priority":
          // console.log(a.requires, b.requires);
          let reqA = a.requires !== null ? a.requires : [""];
          let reqB = b.requires !== null ? b.requires : [""];

          let resA = reqA.sort().join();
          let resB = reqB.sort().join();

          return resB.localeCompare(resA);
        default:
          return 0;
      }
    });

    const c1 = { width: "10%" };
    const c2 = { width: "40%" };
    const c3 = { width: "15%" };
    const c4 = { width: "10%" };
    const c5 = { width: "15%" };

    const trStyle = (pred, sub) => {
      return {
        // backgroundColor: c,
        filter: "brightness(" + (pred ? "80" : "100") + "%)",
      };
    };
    
    const dark = {filter: "brightness("}

    const link = (code) =>
      "https://www.uio.no/studier/emner/matnat/ifi/" + code + "/index.html";

    // console.log(mand)

    const idk = data
    // .filter((n) => n.code[2] < 6)
    .map((row) => {
      
        const isSelected = selected.map((d) => d.id).includes(row.id); // || mand.includes(row.id);

        if (row.semester === null) {
          return (
            <tr key={row.id} style={trStyle(isSelected, row)}>
              <td style={c1}>
                <a style={{ color: "black" }} href={link(row.code)} target="_blank" rel="noopener noreferrer">
					        {row.code}
					      </a>
				      </td>
              <td style={c2} data-item={row.code}>{row.title}</td>
              <td style={c4} data-item={row.code}>{row.points}</td>
              <td style={c3} data-item={row.code}>{"utilgjengelig"}</td>
              <td style={c5} data-item={row.code}>{row.requires != null ? row.requires.join(", ") : ""}</td>
            </tr>
          );
        } else {
          return (
            <tr key={row.id} style={trStyle(isSelected, row)}>
              <td style={c1}>
                <a style={{ color: "black" }} href={link(row.code)} target="_blank" rel="noopener noreferrer">
                  {row.code}
                </a>
              </td>
              <td style={c2} data-item={row.code} onClick={funcSelect}>{row.title}</td>
              <td style={c4} data-item={row.code} onClick={funcSelect}>{row.points}</td>
              <td style={c3} data-item={row.code} onClick={funcSelect}>{row.semester}</td>
              <td style={c5} data-item={row.code} onClick={funcSelect}>{row.requires != null ? row.requires.join(", ") : ""}</td>
            </tr>
          );
        }
      });

    return (
      <div className="subject-container">
        <table className="subject-table">
          <thead>
            <tr>
              <th style={c1} data-item={"code"} onClick={funcSort}>code</th>
              <th style={c2} data-item={"title"} onClick={funcSort}>title</th>
              <th style={c4} data-item={"points"} onClick={funcSort}>points</th>
              <th style={c3} data-item={"semester"} onClick={funcSort}>semester</th>
              <th style={c5} data-item={"priority"} onClick={funcSort}>priority</th>
            </tr>
          </thead>
          <tbody>{idk}</tbody>
        </table>
      </div>
    );
  }
}

export default Subjects;
