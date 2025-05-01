$(document).ready(function () {
    $(".post-content").on("input", function () {
        let charCount = $(this).val().length;
        let charLimit = 512;

        // Update character counter
        $(".char-count").text(`${charCount}/${charLimit} characters`);

        // Check if near or over the limit
        if (charCount > charLimit - 50 && charCount <= charLimit) {
            $(".char-count").css("color", "orange"); // Warn the user
        } else if (charCount > charLimit) {
            $(".char-count").css("color", "red"); // Exceeded the limit
            $(".submit-btn").prop("disabled", true); // Disable submit button
        } else {
            $(".char-count").css("color", "black"); // Reset color
            $(".submit-btn").prop("disabled", false); // Enable submit button
        }
    });

    // Show Confirmation Popup Only When Clicking "Cancel"
    $(".draft-btn:contains('Cancel')").on("click", function () {
        $("#cancel-popup").fadeIn(200);
    });

    // If "Yes" is clicked, redirect to index.html
    $("#confirm-cancel").on("click", function () {
        console.log("✅ Forced redirect to home");
        window.location.href = "/";  // hardcoded test
    });
    
    console.log("hello");

    // If "No" is clicked, hide the popup using .closest()
    $("#cancel-no").on("click", function () {
        $(this).closest(".popup-overlay").fadeOut(200); // Using .closest() to traverse up to the popup container
    });
});
