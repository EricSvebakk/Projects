
/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
const $ = (id) => document.getElementById(id);

/* const $set = (attribute, id, value) => $(id).setAttribute(attribute, value);
const $get = (attribute, id) => $(id).getAttribute(attribute); */

const $setVal = (id, val) => $(id).value = val;
const $getVal = (id) => $(id).value;

const $getClick = (id) => $(id).click();
const $setClick = (id,action) => $(id).onclick = action;

const uniqueData = (data) => [...new Set(data)];

/* const split = (input) => input.toString().split(".")[0]; */
/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
/* const keyPlusVal = (input, repeat) => {

    for (let i = 0; i < repeat; i++) input = values(input)[0];
    return [Object.keys(input), input, Object.keys(input).length];
} */

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
const lengthPerSegment = (input, repeat) => {

    for (let i = 0; i < repeat; i++) input = values(input)[0];
    return input;
}


/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function largestValue(data) {
    
    let largest = 0;

    let iterate = (obj) => {
        Object.keys(obj).forEach(key => {
            if (typeof obj[key] === 'object') {
                iterate(obj[key]);
            } else if (typeof obj[key] === 'number') {
                if (Math.abs(obj[key]) > Math.abs(largest)) largest = obj[key];
            }
        });
    }
    
    iterate(data);

    return largest;
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function numOfValues(obj) {
    
    let numObj = 0,
        numVal = 0

    Object.keys(obj).forEach(key => { numObj-- });

    console.log("start:", numObj);
    iterator(obj);

    function iterator(obj) {

        Object.keys(obj).forEach(key => {

            if (typeof obj[key] === 'object') {
                console.log("object:", key);
                iterator(obj[key]);
                numObj++;
            }
            else {
                numVal++;
                console.log("==> value:", key, obj[key]);
            }

        })
        console.log("");
    }

    return [numObj, numVal];
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
/* function objectsPerLevel(obj) {

    let opl = [0, 0, 0],
        index = -1;

    iterator(obj);

    function iterator(obj) {
        
        index++;
        
        Object.keys(obj).forEach(key => {

            opl[index]++;
            iterator(obj[key]);
        })
        index--;
    }

    return opl;
} */

function objectsPerLevel(obj) {

    let opl = [],
        level = -1;

    iterator(obj);

    function iterator(obj) {

        level++;

        Object.keys(obj).forEach(key => {

            if (typeof opl[level] === 'undefined') opl[level] = 0;

            opl[level]++;
            iterator(obj[key]);
        })
        level--;
    }

    return opl;
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function randomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function randomColour(shade=0) {
    const hex0 = "0123456789ABCDEF";
    const hex2 = "01234567";
    const hex1 = "89ABCDEF";

    let colour = "#";

    if (shade == 0) for (let i = 0; i < 6; i++) colour += hex0[Math.floor(Math.random() * hex0.length)];
    else if (shade == 1) for (let i = 0; i < 6; i++) colour += hex1[Math.floor(Math.random() * hex1.length)];
    else if (shade == 2) for (let i = 0; i < 6; i++) colour += hex2[Math.floor(Math.random() * hex2.length)];

    return colour;
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function randomOrder(array) {

    let currentIndex = array.length,
        temporaryValue,
        randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}