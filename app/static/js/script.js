document.getElementById("google-login").addEventListener("click", function() {
    window.location.href = "/auth";
});

document.getElementById("generate-code").addEventListener("click", function() {
    const bgColor = document.getElementById("bg-color").value;
    const reviewsHtml = document.getElementById("reviews").innerHTML;
    const embedCode = `<div style="background-color: ${bgColor};">${reviewsHtml}</div>`;
    document.getElementById("embed-code").value = embedCode;
});
