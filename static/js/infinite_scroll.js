// Function to check if the user has scrolled to the bottom of the page
function isBottomOfPage() {
    return window.innerHeight + window.scrollY >= document.body.offsetHeight;
}
let offset = 0;  // Initial offset
const limit = 3; // Number of articles to load per request
// Function to load additional articles from the server
function loadMoreArticles() {
    // Send AJAX request to fetch more articles
    fetch('http://127.0.0.1:8000/api_news/list/?offset=' + offset + '&limit=' + limit)
        .then(response => {
            console.log('kukareku')
            if (!response.ok) {
                throw new Error('Failed to fetch articles');
            }
            return response.json();
        })
        .then(data => {
            // Check if there are more articles to load
            if (data.length > 0) {
                // Append new articles to the container
                const articleContainer = document.getElementById('articleContainer');
                data.forEach(article => {
                    const articleElement = document.createElement('div');
                    articleElement.classList.add('article');
                    articleElement.innerHTML = `<h2>${article.title}</h2><p>${article.body}</p>`;
                    articleContainer.appendChild(articleElement);
                });
                // Update offset for the next request
                offset += limit;
            } else {
                // No more articles to load
                console.log('No more articles to load');
            }
        })
        .catch(error => console.error(error));
}


// Event listener for scrolling
window.addEventListener('scroll', () => {
    // Check if the user has scrolled to the bottom of the page
    if (isBottomOfPage()) {
        // Load more articles
        loadMoreArticles();
    }
});

// Initial load of articles when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadMoreArticles();
});
