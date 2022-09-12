/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
class Cell {
    constructor(i, j, mazeWidth, cellWidth, colour=[], type) {
        this.i = i;
        this.j = j;

        this.mW = mazeWidth;
        this.cW = cellWidth;

        this.walls = [true, true, true, true];
        this.visited = false;

        this.type = type;

        this.c0 = [colour[0], colour[1], colour[2]];
        this.c1 = [0,0,0];
        this.c2 = "black"
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    index = (i,j) => {
        if (i < 0 || j < 0 || i > this.mW - 1 || j > this.mW - 1) return -1;
        return i + j * this.mW;
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    checkNeighbours = () => {
        let neighbours = [];

        let top =    grid[this.index(this.i, this.j-1)],
            right =  grid[this.index(this.i+1, this.j)],
            bottom = grid[this.index(this.i, this.j+1)],
            left =   grid[this.index(this.i-1, this.j)];
        
        if (top && !top.visited) {neighbours.push(top);}
        if (right && !right.visited) {neighbours.push(right);}
        if (bottom && !bottom.visited) {neighbours.push(bottom);}
        if (left && !left.visited) {neighbours.push(left);}

        if (neighbours.length > 0) {
            let r = Math.floor(randomNumber(0, neighbours.length-1));
            return neighbours[r];
        } else return undefined;
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    removeWalls(cell) {
        let x = this.i - cell.i,
            y = this.j - cell.j;

        if (x === 1) {
            this.walls[3] = false;
            cell.walls[1] = false;
        } else if (x === -1) {
            this.walls[1] = false;
            cell.walls[3] = false;
        } else if (y === 1) {
            this.walls[0] = false;
            cell.walls[2] = false;
        } else if (y === -1) {
            this.walls[2] = false;
            cell.walls[0] = false;
        }
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    show = () => {
        let x = this.i * this.cW,
            y = this.j * this.cW;

        if (this.walls[0]) {
            tegn.start(x, y);
            tegn.linje(x + this.cW, y, this.c2);
            tegn.stopp();
        }
        if (this.walls[1]) {
            tegn.start(x + this.cW, y);
            tegn.linje(x + this.cW, y + this.cW, this.c2);
            tegn.stopp();
        }
        if (this.walls[2]) {
            tegn.start(x + this.cW, y + this.cW);
            tegn.linje(x, y + this.cW, this.c2);
            tegn.stopp();
        }
        if (this.walls[3]) {
            tegn.start(x, y + this.cW);
            tegn.linje(x, y, this.c2);
            tegn.stopp();
        }
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    highlight = (dist) => {
        let x = this.i * this.cW,
            y = this.j * this.cW;

        if (this.type == "ordinær") {
            tegn.firkant(x, y, x + this.cW, y + this.cW, "rgb(" + this.c0[0] + "," + this.c0[1] + "," + this.c0[2] + ")");
        }

        if (this.type == "frekvens") {
            console.log(this.c2[0],this.c2[1],this.c2[2]);
            tegn.firkant(x, y, x + this.cW, y + this.cW, "rgb(" + this.c2[0] + "," + this.c2[1] + "," + this.c2[2] + ")");
            this.c2[0] += 25;
            this.c2[1] += 0;
            this.c2[2] += 15;
        }

        if (this.type == "avstand") {
            this.c1[0] = this.c0[0] + dist;
            this.c1[1] = this.c0[1] + dist;
            this.c1[2] = this.c0[2] + dist;
            /* tegn.sirkel(x + this.cW / 2, y + this.cW / 2, this.cW / 2, this.cW / 2, "rgb(" + this.c1[0] + "," + this.c1[1] + "," + this.c1[2] + ")"); */
            tegn.firkant(x, y, x + this.cW, y + this.cW, "rgb(" + this.c1[0] + "," + this.c1[1] + "," + this.c1[2] + ")");
        }
    }

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
    lowlight = (dist) => {
        if (this.type == "avstand") {
            this.c1[0] = this.c0[0] + dist;
            this.c1[1] = this.c0[1] + dist;
            this.c1[2] = this.c0[2] + dist;
        }
    }

}