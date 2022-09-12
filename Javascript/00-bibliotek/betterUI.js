
class betterUI {
    constructor(contentID="container", output=false, width="190", height = "194") {

        this.bredde = width;

        // Div containing input and output
        this.container = document.createElement("div");
        this.container.id = contentID;
        this.container.style.float = "left";
        this.container.style.width = parseInt(width) + 30 + "px";
        document.body.appendChild(this.container);

        // form containing input
        this.form = document.createElement("form");
        this.form.id = contentID + "_form_input";
        this.form.style.margin = "10px";
        this.form.style.padding = "5px";
        this.form.style.paddingBottom = "7px";
        this.form.style.backgroundColor = "white";
        this.form.style.float = "left";
        this.form.style.width = width + "px";
        $(this.container.id).appendChild(this.form);

        // this.button = document.createElement("input");
        // this.button.id = contentID + "_form_button";
        // this.button.type = "button";
        // this.button.value = "Start";
        // this.button.style.width = "99%";
        // this.button.style.height = "20px";
        // $(this.form.id).appendChild(this.button);

        if (output) {
            // div containing output
            this.outputDiv = document.createElement("div");
            this.outputDiv.id = contentID + "_form_output";
            this.outputDiv.style.width = width + "px";
            this.outputDiv.style.height = height + "px";
            this.outputDiv.style.backgroundColor = "white";
            this.outputDiv.style.float = "left";
            this.outputDiv.style.margin = "10px";
            this.outputDiv.style.padding = "5px";
            $(this.container.id).appendChild(this.outputDiv);
        }
        this.antallINP = 0;
    }

    text(inputID=[]) {
        for (let i in inputID) {
            this.inputDiv = document.createElement("div");
            this.label = document.createElement("label");
            this.input = document.createElement("input");

            this.inputDiv.style.margin = "5px";
            this.inputDiv.style.height = "20px";
            this.inputDiv.style.width = "96%";
            this.inputDiv.id = "div_" + inputID[i];
            $(this.form.id).insertBefore(this.inputDiv, this.button);

            this.label.for = inputID[i];
            this.label.innerHTML = inputID[i];
            this.label.style.float = "left";
            this.label.style.width = this.bredde * 0.4 + "px";
            this.label.style.height = "15px";
            $(this.inputDiv.id).appendChild(this.label);
            
            this.input.id = inputID[i];
            this.input.type = "text";
            this.input.placeholder = "skriv her";
            this.input.style.float = "right";
            this.input.style.width = "98px";
            this.input.style.border = "1px solid grey";
            $(this.inputDiv.id).appendChild(this.input);
        }
        this.antallINP += 1;
    }

    list(inputID=[],dropdownID=[]) {
        for (let i in inputID) {
            this.inputDiv = document.createElement("div");
            this.label = document.createElement("label");
            this.input = document.createElement("input");

            this.inputDiv.style.margin = "5px";
            this.inputDiv.style.height = "20px";
            this.inputDiv.style.width = "96%";
            this.inputDiv.id = "div_" + inputID[i];
            $(this.form.id).insertBefore(this.inputDiv, this.button);

            this.label.for = inputID[i];
            this.label.innerHTML = inputID[i];
            this.label.style.float = "left";
            this.label.style.width = this.bredde * 0.4 + "px";
            this.label.style.height = "15px";
            $(this.inputDiv.id).appendChild(this.label);

            this.select = document.createElement("select");
            this.select.id = inputID[i];
            this.select.style.float = "right";
            this.select.style.width = "100px";
            this.select.style.border = "1px solid grey";
            $(this.inputDiv.id).appendChild(this.select);

            for (let j in dropdownID) {
                this.option = document.createElement("option");
                this.option.id = inputID[i] + "_" + dropdownID[j];
                this.option.innerHTML = dropdownID[j];
                $(this.select.id).appendChild(this.option);
            }
        }
        this.antallINP += 1;
    }

    checkbox(inputID=[]) {
        for (let i in inputID) {
            this.inputDiv = document.createElement("div");
            this.label = document.createElement("label");
            this.input = document.createElement("input");

            this.inputDiv.style.margin = "5px";
            this.inputDiv.style.height = "20px";
            this.inputDiv.style.width = "96%";
            this.inputDiv.id = "div_" + inputID[i];
            $(this.form.id).insertBefore(this.inputDiv, this.button);

            this.label.for = inputID[i];
            this.label.innerHTML = inputID[i];
            this.label.style.float = "left";
            this.label.style.width = "70px";
            this.label.style.height = "15px";
            $(this.inputDiv.id).appendChild(this.label);

            this.input.id = inputID[i];
            this.input.type = "checkbox";
            this.input.placeholder = "skriv her";
            this.input.style.float = "right";
            this.input.style.width = "98px";
            this.input.style.border = "1px solid grey";
            $(this.inputDiv.id).appendChild(this.input);
        }
        this.antallINP += 1;
    }

    bttn(inputID=[], destination) {
        for (let i in inputID) {
            this.button = document.createElement("input");
            this.button.id = inputID;
            this.button.type = "button";
            this.button.value = inputID;
            this.button.style.width = "100px";
            this.button.style.height = "20px";
            this.button.style.float = "left";
            $(destination).appendChild(this.button);
        }
    }

    div(inputID, width, height) {
        this.div = document.createElement("div");
        this.div.id = inputID;
        this.div.style.width = width + "px";
        this.div.style.height = height + "px";
        this.div.style.backgroundColor = "white";
        this.div.style.float = "left";
        this.div.style.margin = "10px";
        this.div.style.padding = "5px";
        document.body.appendChild(this.div);
    }

    delete(deletionID) {
        
        var elem = $(deletionID);
        elem.parentNode.removeChild(elem);
    }

    out(output, tøm=false) {
        this.output = document.createElement("p");
        this.output.style.margin = "5px";
        this.output.style.textOverflow = "clip";
        /* console.log($(this.outputDiv.id).style.height) // = "400px" (194 - (parseInt(this.antallINP)*20)) + "px";
        console.log(this.outputDiv.style.height); */
        
        if (tøm) {
            let slettOut = $(this.outputDiv.id);
            while (slettOut.firstChild) {
                slettOut.removeChild(slettOut.firstChild);
            }
        }

        this.output.innerHTML = output;
        $(this.outputDiv.id).appendChild(this.output);
    }

    slett(slettID) {
        let slett = $("div_"+slettID);
        slett.parentNode.removeChild(slett);
    }

    slettOutput(){
        let slettOut = $(this.outputDiv.id)
        while (slettOut.firstChild) {
            slettOut.removeChild(slettOut.firstChild);
        }
    }

    slettAlle() {
        let slettIn = $(this.form.id);
        while (slettIn.firstChild) {
            slettIn.removeChild(slettIn.firstChild);
        }

        this.antallINP = 0;
        
        this.button = document.createElement("input");
        this.button.id = "form_knapp";
        this.button.type = "button";
        this.button.value = "Start";
        this.button.style.width = "99%";
        this.button.style.height = "20px";
        $(this.form.id).appendChild(this.button);
    }
}
