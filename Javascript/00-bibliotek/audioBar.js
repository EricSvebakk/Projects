
/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
class audioBar {
    constructor(width, height, colour1, colour2) {
        this.width = width;
        this.height = height;

        this.c1 = colour1;
        this.c2 = colour2;

        let temp = document.createElement("div");
        temp.id = "audioBar";
        temp.style.width = this.width;
        temp.style.height = this.height;
        document.body.appendChild(temp);

        // Creates progressbar
        temp = document.createElement("canvas");
        temp.id = "AB_progress";
        temp.width = this.width;
        temp.height = this.height;
        $("audioBar").appendChild(temp);
        this.progressBar = $("AB_progress").getContext("2d");

        // Creates audio-object
        temp = document.createElement("audio");
        temp.id = "AB_audio";
        temp.ontimeupdate = this.updateProgressBar;
        $("audioBar").appendChild(temp);

        // Creates span-tag to display current time
        temp = document.createElement("span");
        temp.id = "AB_currentTime";
        $("audioBar").appendChild(temp);

        // Creates span-tag to display audio duration
        temp = document.createElement("span");
        temp.id = "AB_duration";
        $("audioBar").appendChild(temp);

        // Creates play/pause button
        temp = document.createElement("div");
        temp.id = "AB_button";
        temp.style.width = "10px";
        temp.style.height = "10px";
        temp.style.backgroundColor = "green";
        $("audioBar").appendChild(temp);

        this.createBar();
    }

    audioSource(source) {
        $("AB_audio").src = source;
    }

    /* convertElapsedTime(inputSeconds) {

        let seconds = Math.floor(inputSeconds % 60),
            minutes = Math.floor(inputSeconds / 60);

        if (seconds < 10) seconds = "0" + seconds;
        return minutes + ":" + seconds;
    } */

    createBar() {
        let progressBar = $("AB_progress").getContext("2d");

        $("AB_button").addEventListener("click", () => this.toggleAudio() );

        $("AB_audio").addEventListener("loadedmetadata", () => {
            $("AB_duration").innerHTML = this.convertElapsedTime($("AB_audio").duration);
            $("AB_currentTime").innerHTML = this.convertElapsedTime($("AB_audio").currentTime);
            progressBar.fillRect(0,0, this.width, this.height);
        });
    }

    toggleAudio() {
        let toggleAudio = true,
            method = undefined;

        if (toggleAudio) {
            toggleAudio = false;
            method = "play";
        } else {
            toggleAudio = true;
            method = "pause";
        }

        console.log("heyyyyy");

        $("AB_audio")[method]();
    }

    updateProgressBar() {

        let progressBar = $("AB_progress").getContext("2d");

        progressBar.clearRect(0, 0, this.width, this.height);
        progressBar.fillStyle = "#000";
        progressBar.fillRect(0, 0, this.width, this.height);

        let currentTime = $("AB_audio").currentTime,
            duration = $("AB_audio").duration;

        let percentage = currentTime / duration,
            progress = (this.width * percentage);

        let seconds = Math.floor(currentTime % 60),
            minutes = Math.floor(currentTime / 60);

        if (seconds < 10) seconds = "0" + seconds;

        $("AB_currentTime").innerHTML = minutes + ":" + seconds;

        progressBar.fillStyle = "#FF0000"
        progressBar.fillRect(0, 0, progress, this.height);
    }
}