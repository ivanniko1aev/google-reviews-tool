document.getElementById("google-login").addEventListener("click", function() {
    window.location.href = "/auth";
});

document.getElementById("generate-code").addEventListener("click", function() {
    const bgColor = document.getElementById("bg-color").value;
    const reviewsHtml = document.getElementById("reviews").innerHTML;
    const embedCode = `<div style="background-color: ${bgColor};">${reviewsHtml}</div>`;
    document.getElementById("embed-code").value = embedCode;
});

// Fetch and display reviews
async function fetchReviews() {
    try {
        const response = await fetch('/reviews');  // Fetch reviews from backend
        if (!response.ok) {
            throw new Error('Failed to fetch reviews');
        }

        const data = await response.json();
        const reviewsDiv = document.getElementById("reviews");
        reviewsDiv.innerHTML = ""; // Clear existing reviews

        if (data.reviews && data.reviews.length > 0) {
            data.reviews.forEach(review => {
                const reviewElement = document.createElement("div");
                reviewElement.classList.add("review-card");
                reviewElement.innerHTML = `
                    <strong>${review.reviewer.displayName}</strong>
                    <p>${review.comment}</p>
                `;
                reviewsDiv.appendChild(reviewElement);
            });
        } else {
            reviewsDiv.innerHTML = "<p>No reviews found.</p>";
        }
    } catch (error) {
        console.error("Error fetching reviews:", error);
        document.getElementById("reviews").innerHTML = "<p>Error loading reviews.</p>";
    }
}

// Generate embed code dynamically
document.getElementById("generate-code").onclick = function() {
    const bgColor = document.getElementById("bg-color").value;
    const fontSize = document.getElementById("font-size").value;
    const reviewsHtml = document.getElementById("reviews").innerHTML;

    const embedCode = `
        <div style="background-color: ${bgColor}; font-size: ${fontSize}px; padding: 10px; border-radius: 8px;">
            ${reviewsHtml}
        </div>
    `;

    document.getElementById("embed-code").value = embedCode;
};

// Load reviews on page load
document.addEventListener("DOMContentLoaded", fetchReviews);
