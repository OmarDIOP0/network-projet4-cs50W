// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('.edit-button').forEach(button => {
//         button.addEventListener('click', (e) => {
//             e.preventDefault();
//             const postId = e.target.getAttribute('data-post-id');
//             const postContent = document.getElementById(`post-content-${postId}`);
//             const originalContent = postContent.querySelector('p').innerText;

//             postContent.innerHTML = `
//                 <textarea class="form-control" id="edit-content-${postId}">${originalContent}</textarea>
//                 <button class="btn btn-primary save-button" data-post-id="${postId}">Save</button>
//             `;

//             document.querySelector(`.save-button[data-post-id="${postId}"]`).addEventListener('click', (event) => {
//                 event.preventDefault();
//                 const newContent = document.getElementById(`edit-content-${postId}`).value;

//                 fetch(`/edit-post/${postId}/`, {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': getCookie('csrftoken')
//                     },
//                     body: JSON.stringify({ content: newContent })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         postContent.innerHTML = `<p>${data.content}</p>`;
//                     } else {
//                         alert('An error occurred while saving the post.');
//                     }
//                 });
//             });
//         });
//     });

//     document.querySelectorAll('.like-button').forEach(button => {
//         button.addEventListener('click', (e) => {
//             e.preventDefault();
//             const postId = e.target.getAttribute('data-post-id');
//             const likesCountElement = document.getElementById(`likes-count-${postId}`);

//             fetch(`/toggle-like/${postId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken')
//                 },
//                 body: JSON.stringify({})
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     const newLikesCount = data.likes_count;
//                     likesCountElement.innerText = newLikesCount;

//                     const likeButton = e.target;
//                     if (data.liked) {
//                         likeButton.innerHTML = '<i class="bi bi-heart-fill"></i> Je n\'aime pas';
//                     } else {
//                         likeButton.innerHTML = '<i class="bi bi-heart"></i> J\'aime';
//                     }
//                 } else {
//                     alert('An error occurred while updating the like status.');
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//         });
//     });
// });

// // Helper function to get CSRF token from cookies
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
