
import math

def translate():
    posBi = {
        pX: deltaX * cos + deltaY * sin,
        pY: deltaY * cos - deltaX * sin
    },



def sjekkKollisjon(objectA, objectB):

    deltaX = objectA.pX - objectB.pX,
    objectA.pY - objectB.pY,
    avstand = math.sqrt(deltaX * deltaX + deltaY * deltaY);

    if (avstand < objectA.radius + objectB.radius):
        vinkel = math.atan2(deltaY, deltaX)
        sin = math.sin(vinkel)
        cos = math.cos(vinkel)
        # roterer objektA startpos
        posAi = { pX: 0, pY: 0 },
        # roterer objectB startpos
        posBi = {
            pX: deltaX * cos + deltaY * sin,
            pY: deltaY * cos - deltaX * sin
        },
        # roterer objektA fartsvektor
        velAi = {
            vX: objectB.vX * cos + objectB.vY * sin,
            vY: objectB.vY * cos - objectB.vX * sin
        },
        # roterer objectB fartsvektor
        velBi = {
            vX: objectA.vX * cos + objectA.vY * sin,
            vY: objectA.vY * cos - objectA.vX * sin
        },
        vX_Total = velAi.vX - velBi.vX;

        velAi.vX =
            ((objectB.masse - objectA.masse) * velAi.vX + 2 * objectA.masse * velBi.vX) /
            (objectB.masse + objectA.masse);
        velBi.vX = vX_Total + velAi.vX;

        posAi.pX += velAi.vX;
        posBi.pX += velBi.vX;

        # roterer objektA posisjon tilbake
        let posAf = {
                pX: posAi.pX * cos - posAi.pY * sin,
                pY: posAi.pY * cos + posAi.pX * sin
            },
        # roterer objectB posisjon tilbake
        posBf = {
            pX: posBi.pX * cos - posBi.pY * sin,
            pY: posBi.pY * cos + posBi.pX * sin
        },
        # roterer objektA fartsvektor tilbake
        velAf = {
            vX: velAi.vX * cos - velAi.vY * sin,
            vY: velAi.vY * cos + velAi.vX * sin
        },
        # roterer objectB fartsvektor tilbake
        velBf = {
            vX: velBi.vX * cos - velBi.vY * sin,
            vY: velBi.vY * cos + velBi.vX * sin
        };

        # beveger objekter til ny posisjon
        objectA.pX = objectB.pX + posBf.pX;
        objectA.pY = objectB.pY + posBf.pY;
        objectB.pX = objectB.pX + posAf.pX;
        objectB.pY = objectB.pY + posAf.pY;

        # oppdaterer objekter med ny fart
        objectB.vX = velAf.vX;
        objectB.vY = velAf.vY;
        objectA.vX = velBf.vX;
        objectA.vY = velBf.vY;

        objectB.vX *= objectB.elastisitet;
        objectB.vY *= objectB.elastisitet;
        objectA.vX *= objectA.elastisitet;
        objectA.vY *= objectA.elastisitet;
    }
}
