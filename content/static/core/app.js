// static/js/app.js
// Use a front-end framework like Vue.js or React for more complex interactions

// For simplicity, this example uses basic JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Fetch posts and render them
    fetch('/api/posts/')
      .then(response => response.json())
      .then(posts => {
        const app = document.getElementById('app');
        posts.forEach(post => {
          const postDiv = document.createElement('div');
          postDiv.className = 'post';
          postDiv.innerHTML = `
            <img src="${post.image}" alt="${post.caption}">
            <p>${post.caption}</p>
            <button onclick="likePost(${post.id})">Like</button>
            <button onclick="showComments(${post.id})">Comments</button>
            <div id="comments-${post.id}" style="display: none;"></div>
            <input type="text" id="comment-input-${post.id}" placeholder="Add a comment">
            <button onclick="addComment(${post.id})">Post</button>
          `;
          app.appendChild(postDiv);
        });
      });
  
    // Function to handle liking a post
    window.likePost = function (postId) {
      fetch('/api/likes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post: postId })
      })
        .then(response => response.json())
        .then(() => location.reload());
    };
  
    // Function to show/hide comments for a post
    window.showComments = function (postId) {
      const commentsDiv = document.getElementById(`comments-${postId}`);
      commentsDiv.style.display = commentsDiv.style.display === 'none' ? 'block' : 'none';
    };
  
    // Function to add a comment to a post
    window.addComment = function (postId) {
      const commentInput = document.getElementById(`comment-input-${postId}`);
      const commentText = commentInput.value;
  
      if (commentText.trim() !== '') {
        fetch('/api/comments/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ post: postId, text: commentText })
        })
          .then(response => response.json())
          .then(() => location.reload());
      }
    };
  });
  