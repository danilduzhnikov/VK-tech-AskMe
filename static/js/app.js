function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const questions = document.getElementsByClassName('question');

for (const question of questions) {
    const likeCounter = question.querySelector('.like-counter');
    const likeButton = question.querySelector('.like-button');
    const heartIcon = likeButton.querySelector('i');
    const questionId = question.dataset.questionId;

    likeButton.addEventListener('click', () => {
        const isLiked = heartIcon.getAttribute('data-is-liked') === 'true';
        const request = new Request(`${questionId}/like_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
        });

        fetch(request)
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data) {
                    likeCounter.textContent = data.likes_count;
                    heartIcon.style.color = data.is_liked === 'true' ? 'red' : 'lightgray';
                }
            })
            .catch(error => console.error('Error:', error));
    });
}
