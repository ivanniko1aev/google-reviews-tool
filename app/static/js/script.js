// ✅ Login Button (Optional)
const loginButton = document.getElementById("google-login");
if (loginButton) {
    loginButton.addEventListener("click", function() {
        window.location.href = "/auth";
    });
}

// ✅ Generate Embed Code (Keep this if needed)
const generateButton = document.getElementById("generate-code");
if (generateButton) {
    generateButton.addEventListener("click", function() {
        const bgColor = document.getElementById("bg-color").value;
        const reviewsHtml = document.getElementById("reviews").innerHTML;
        const embedCode = `<div style="background-color: ${bgColor}; padding: 10px;">${reviewsHtml}</div>`;
        document.getElementById("embed-code").value = embedCode;
    });
}

// ✅ Fetch and display reviews
async function fetchReviews() {
    try {
        console.log("🔄 Fetching reviews...");

        const response = await fetch('/reviews', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        console.log("📡 API Response Status:", response.status);

        if (!response.ok) {
            throw new Error(`Failed to fetch reviews: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ API Response Data:", data);

        const reviewsDiv = document.getElementById("reviews");
        reviewsDiv.innerHTML = ""; // Clear existing reviews

        if (data.reviews && data.reviews.length > 0) {
            data.reviews.forEach(review => {
                const reviewElement = document.createElement("div");
                reviewElement.classList.add("review-card");
                reviewElement.innerHTML = `
                    <strong>${review.reviewer.displayName}</strong>
                    <p>${review.comment || "No comment provided."}</p>
                    <small>⭐ Rating: ${review.starRating || "N/A"}</small>
                `;
                reviewsDiv.appendChild(reviewElement);
            });
        } else {
            reviewsDiv.innerHTML = "<p>No reviews found.</p>";
        }
    } catch (error) {
        console.error("❌ Error fetching reviews:", error);
        document.getElementById("reviews").innerHTML = "<p>Error loading reviews.</p>";
    }
}

// ✅ Generate Embed Code
document.getElementById("generate-code").onclick = function () {
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

// ✅ Load reviews on page load
document.addEventListener("DOMContentLoaded", fetchReviews);
