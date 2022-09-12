
var tegn, bui, canvas, cols, rows, dist,
    mazeSize, cellSize, current, next,
    stack = [], grid = [];

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
window.onload = function winInit() {

    tegn = new canvasGRID("canvas", 600, 600, false);
    tegn.blankCanvas("black");
    
    bui = new betterUI("container");
    
    bui.text(["farge", "størrelse"]);
    bui.list(["type"],["ordinær","frekvens","avstand"])
    bui.bttn(["Go"], "container_form_input")
    
    $setVal("farge", "20,40,80");
    $setVal("størrelse", "40");
    
    $setClick("Go",setup);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function setup() {

    mazeSize    = $getVal("størrelse");
    cellSize    = $("canvas").width/mazeSize;
    colour      = eval("["+$getVal("farge")+"]");
    type        = $getVal("type");

    for (let y = 0; y < mazeSize; y++) {
        for (let x = 0; x < mazeSize; x++) {
            let cell = new Cell(x, y, mazeSize, cellSize, colour, type);
            grid.push(cell);
        }
    }

    dist = 0;
    current = grid[(mazeSize*mazeSize)/2 + (mazeSize/2)];

    setInterval(draw, 1);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function draw() {
    
    let change = 0.15;
    for (let i in grid) if (grid[i].visited) grid[i].show();

    current.visited = true;
    current.highlight(dist);
    next = current.checkNeighbours();

    if (next) {
        next.visited = true;
        stack.push(current);
        
        dist += change;
        current.highlight(dist);
        current.removeWalls(next);
        current = next;

    } else if (stack.length > 0) {
        dist -= change;
        current.lowlight(dist);
        current = stack.pop();
    }
}

/* function download() {
    var download = document.getElementById("download");
    var canvas = document.getElementById("canvas");
    var image = canvas.toDataURL("image/png")
    var replace = image.replace("image/png", "image/octet-stream");

    download.setAttribute("href", image);
} */