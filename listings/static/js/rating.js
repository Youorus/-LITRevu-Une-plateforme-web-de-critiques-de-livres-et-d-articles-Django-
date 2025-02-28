document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById("rating-input");
    const ratingError = document.createElement("p");  // Crée un élément pour l'erreur
    ratingError.classList.add("text-red-600", "text-sm", "mt-1");
    ratingError.style.display = "none";  // Cache l'erreur au départ
    document.getElementById("star-container").appendChild(ratingError);

    stars.forEach(star => {
        star.addEventListener("mouseover", function () {
            let value = this.getAttribute("data-value");
            highlightStars(value);
        });

        star.addEventListener("click", function () {
            let value = this.getAttribute("data-value");
            ratingInput.value = value;  // ✅ Stocke la note
            highlightStars(value);
            ratingError.style.display = "none";  // ✅ Cache l'erreur après sélection
        });

        star.addEventListener("mouseleave", function () {
            let selectedValue = ratingInput.value;
            highlightStars(selectedValue);
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            let starValue = star.getAttribute("data-value");
            let starSvg = star.querySelector(".star-svg");
            if (starValue <= value) {
                starSvg.setAttribute("fill", "gold");
            } else {
                starSvg.setAttribute("fill", "gray");
            }
        });
    }

    // Vérifie la note avant de soumettre le formulaire
    document.querySelector("form").addEventListener("submit", function (event) {
        if (ratingInput.value === "0") {
            event.preventDefault();  // ✅ Bloque l'envoi du formulaire
            ratingError.innerText = "Veuillez sélectionner une note.";
            ratingError.style.display = "block";  // ✅ Affiche l'erreur
        }
    });
});
