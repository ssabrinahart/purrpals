$(document).ready(function () {
    // Speech Bubble Interaction
    const meowPhrases = [
        "Meow!",
        "Purr... 💤",
        "Feed me!",
        "Pet me!",
        "Hiss! 😾",
        "Mrrrow?"
    ];

    $(".cat-image-container img").on("click", function () {
        let randomPhrase = meowPhrases[Math.floor(Math.random() * meowPhrases.length)];
        $(".speech-bubble").text(randomPhrase).fadeOut(200).fadeIn(200);
    });

    // Radio Button Message Feature
    $(".radio-btn input[type='radio']").on("change", function () {
        let selectedValue = $(this).parent().text().trim(); // Get text from the parent <label>

        let message = selectedValue.includes("Yes")
            ? "Purrrrrrrrfect!! "
            : "Picky kitty? Edit profile!";

        // Check if message area exists; if not, create it
        if (!$(".radio-message").length) {
            $(".radio-btn").append("<p class='radio-message'></p>");
        }

        $(".radio-message").text(message);
    });
});
