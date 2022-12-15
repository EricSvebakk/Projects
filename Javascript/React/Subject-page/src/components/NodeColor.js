
export function codeColor(node) {
    
	switch (node.code[2]) {
      case "1":
        return "#5db061";
      case "2":
        return "#c18541";
      case "3":
        return "#c44444";
      case "4":
        return "#4a93c8";
      case "5":
        return "#7f5fd0";
      default:
        return "#888";
    }
};

export function semesterColor(node) {
    switch (node.semester) {
      case "høst":
        return "#aa8c55";
      case "vår":
        return "#55a";
	  default:
	    return "#aaa";
    }
};

export function pointsColor(node) {
   
  switch (node.points) {
    case 10:
      return "#ff5dc9";
    case 15:
      return "#d41695";
    case 20:
      return "#6e094c";
    case 30:
      return "#b60e3b";
    default:
      return "#61001a";
  }
};
