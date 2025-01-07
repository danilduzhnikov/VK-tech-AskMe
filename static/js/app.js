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
        const isLiked = heartIcon.getAttribute('data-liked') === 'true';
        const request = new Request(`${questionId}/like_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({ liked: !isLiked }) // Отправляем новый статус
        });

        fetch(request)
            .then(response => response.json())
            .then(data => {
                likeCounter.textContent = data.likes_count;
                heartIcon.style.color = data.is_liked ? 'red' : 'lightgray';
                heartIcon.setAttribute('data-liked', data.is_liked.toString());
            })
            .catch(error => console.error('Error:', error));
    });
}
