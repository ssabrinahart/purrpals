$(document).ready(function () {
    $(".upvote-btn, .downvote-btn").on("click", function () {
      const container = $(this).closest(".vote");
      const postId = container.data("post-id");
      const action = $(this).hasClass("upvote-btn") ? "upvote" : "downvote";
  
      $.post(`/posts/${postId}/vote/`, {
        action: action,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      })
      .done(function (data) {
        container.find(".vote-count").text(data.votes);
      })
      .fail(function (xhr) {
        alert("Error: " + xhr.responseJSON?.error || "Could not vote.");
      });
    });
  });
  