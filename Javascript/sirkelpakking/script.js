
/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
// variabler
var sirkler = [];
const bredde = window.innerWidth;
const høyde = window.innerHeight;

var antallTotal = 0,
    forsøkTotal = 0,
    finished = 0;

var tegn, bui;

/* const bilde = new Image();
    bilde.src = "test2.png";
    lagCanvas("bilde",bredde,høyde,"white");
    var bildedata = bilde.data;
    console.log(bildedata); */

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
window.onload = () => {
    tegn = new canvasGRID("canvas", 500, 500, false);
    
    requestAnimationFrame(animer);
};

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function animer() {

    let total = 5,
        antall = 0,
        forsøk = 0;

    while (antall < total) {
        
        let nyttForsøk = nySirkel();
        if (nyttForsøk != null) {
            sirkler.push(nyttForsøk)
            antall++;
            antallTotal++;
        }
        forsøk++;
        forsøkTotal++;

        if (forsøk >= total*10) {
            finished++;
            console.log("finished",antall,forsøk,finished,antallTotal,forsøkTotal);
            break;
        }
    }

    for (let i in sirkler) {
        if (sirkler[i].vokser) {

            if (sirkler[i].kant()) {
                sirkler[i].vokser = false;
            } 
            
            else {
                for (let j in sirkler) {
                    if (sirkler[i] != sirkler[j]) {

                        let d = dist(sirkler[i].x, sirkler[i].y, sirkler[j].x, sirkler[j].y);
                        if (d - 1.5 < sirkler[i].r + sirkler[j].r) {
                            sirkler[i].vokser = false;
                            break;
                        }
                    }  
                }
            }
            sirkler[i].voks();
            sirkler[i].tegn();
        }
    }
    /* output("output",true);
    output("output","Antall sirkler = " + antallTotal + "<br>" + "Antall forsøk = " + forsøkTotal); */
    if (finished >= 50) return;
    requestAnimationFrame(animer);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function nySirkel() {
    const begrensning = 50;

    let x = randomNumber(begrensning, 1000-begrensning),
        y = randomNumber(begrensning, 1000-begrensning),
        sF = randomNumber(280,280),
        iF = 4,
        r = 1,
        gyldig = true;

    for (let i in sirkler) {
        let d = dist(x, y, sirkler[i].x, sirkler[i].y);
        if (d < sirkler[i].r) {
            gyldig = false;
            break;
        }
    }

    if (gyldig) return new sirkel(x,y,r,sF,iF);
    else return null;
}

function dist(x, y, x_, y_) {
    return Math.hypot(x_ - x, y_ - y);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
class sirkel {
    constructor(x,y,r,startFarge,inkrementFarge) {
        this.cnv = $("canvas");
        this.ctx = this.cnv.getContext("2d");

        this.x = x;
        this.y = y;
        this.r = r;
        this.sF = startFarge;
        this.iF = inkrementFarge
        /* this.f = "hsl(0,0%,"+this.f1+"%"; */
        this.f = "hsl("+this.sF+",100%,50%";
        this.vokser = true;
    }

    voks() {
        if (this.vokser) {
            this.r += 0.5;
            this.sF += this.iF;
            /* this.f = "hsl(0,0%,"+this.f1+"%"; */
            this.f = "hsl("+this.sF+",100%,50%";
        }
    }

    kant() {
        return (this.x + this.r > this.cnv.width || this.x - this.r < 0 || this.y + this.r > this.cnv.height || this.y - this.r < 0)
    }

    tegn() {
        this.ctx.beginPath();
        this.ctx.fillStyle = this.f;
        this.ctx.arc(this.x,this.y,this.r,0*Math.PI,2*Math.PI);
        this.ctx.fill();

        this.ctx.beginPath();
        this.ctx.strokeStyle = "black";
        this.ctx.arc(this.x,this.y,this.r,0*Math.PI,2*Math.PI);
        this.ctx.stroke();
    }

}