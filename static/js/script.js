const likeForm = document.getElementById('likeForm');
const likeCount = document.getElementById('likeCount');

likeForm.addEventListener('submit', (event) => {
    event.preventDefault();

    fetch(window.location.href, {
        method: 'POST',
        body: new FormData(likeForm),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Failed to update like count');
    })
    .then(data => {
        likeCount.innerText = data.like_count;
    })
    .catch(error => console.error(error));
});