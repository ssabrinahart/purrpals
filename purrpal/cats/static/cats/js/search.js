$(document).ready(function () {
    $("#search-form").on("submit", function (e) {
      e.preventDefault(); // Stop default page reload
  
      const query = $("#search-input").val().trim();
  
      if (!query) {
        $("#results").html("<p>Please enter a search term.</p>");
        return;
      }
  
      $.get("/search/?query=" + encodeURIComponent(query), function (data) {
        const posts = data.posts;
  
        if (posts.length === 0) {
          $("#results").html("<p>No posts found for your search.</p>");
          return;
        }
  
        let html = "";
        posts.forEach(post => {
        html += `
            <section class="post">
            <div class="vote" data-post-id="${post.id}">
                <button class="upvote-btn">🔼</button>
                <span class="vote-count">${post.votes}</span>
                <button class="downvote-btn">🔽</button>
            </div>
            <div class="post-content">
                <h2>${post.title}</h2>
                <p>${post.content}</p>
                <p><strong>By:</strong> ${post.author}</p>
                <p><strong>Posted:</strong> ${post.created_at}</p>
            </div>
            <div style="position: absolute; right: 0; padding-right: 5px; display: flex; flex-direction: column;">
                <a href="/posts/${post.id}/" style="padding-bottom: 5px;">
                <button class="draft-btn" type="button">View</button>
                </a>
            </div>
            </section>
        `;
        });

        $("#results").html(html);

      });
    });
  });
  