var audioPlayer = document.getElementById("audioPlayer");

    function playAudio() {
      audioPlayer.play();
    }

    function pauseAudio() {
      audioPlayer.pause();
    }

    function stopAudio() {
      audioPlayer.pause();
      audioPlayer.currentTime = 0;
    }