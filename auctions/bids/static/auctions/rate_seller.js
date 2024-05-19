document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#rate-seller-form').onsubmit = () => {
        const rating = document.querySelector('#rating').value;

        fetch(`/rate_seller/${seller_username}/${rating}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle success response, e.g., display a success message
            console.log(data);
        })
        .catch(error => {
            // Handle error, e.g., display an error message
            console.error('There was a problem with the fetch operation:', error);
        });

        return false; // Prevent default form submission
    };
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const stars = document.querySelectorAll('.rating > label');

    stars.forEach(star => {
        star.addEventListener('mouseover', (e) => {
            const rating = e.currentTarget;
            const siblings = getSiblings(rating);

            rating.classList.add('hover');
            siblings.forEach(sibling => sibling.classList.add('hover'));
        });

        star.addEventListener('mouseout', (e) => {
            const rating = e.currentTarget;
            const siblings = getSiblings(rating);

            rating.classList.remove('hover');
            siblings.forEach(sibling => sibling.classList.remove('hover'));
        });
    });

    function getSiblings(element) {
        const siblings = [];
        let sibling = element.previousElementSibling;

        while (sibling) {
            siblings.push(sibling);
            sibling = sibling.previousElementSibling;
        }

        return siblings;
    }
});
