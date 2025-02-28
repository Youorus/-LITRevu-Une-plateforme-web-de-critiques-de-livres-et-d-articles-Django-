document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[id^=star-container]").forEach(starContainer => {
        const isEditable = starContainer.getAttribute("data-edit") === "true"; // Vérifie le mode édition
        const stars = starContainer.querySelectorAll(".star");
        const ratingInput = starContainer.nextElementSibling; // Input caché (s'il existe)

        // 🟢 Correction : On récupère bien la valeur de la note actuelle
        let selectedRating = ratingInput ? ratingInput.value : starContainer.getAttribute("data-rating");

        // Convertir en entier pour éviter les bugs d'affichage
        selectedRating = parseInt(selectedRating, 10) || 0;

        function highlightStars(value) {
            stars.forEach(star => {
                let starValue = parseInt(star.getAttribute("data-value"), 10);
                let starSvg = star.querySelector(".star-svg");
                starSvg.setAttribute("fill", starValue <= value ? "gold" : "gray");
            });
        }

        // ✅ Appliquer immédiatement la note actuelle au chargement
        highlightStars(selectedRating);

        if (isEditable) {
            stars.forEach(star => {
                star.addEventListener("mouseover", function () {
                    highlightStars(this.getAttribute("data-value"));
                });

                star.addEventListener("mouseleave", function () {
                    highlightStars(selectedRating);
                });

                star.addEventListener("click", function () {
                    selectedRating = parseInt(this.getAttribute("data-value"), 10);
                    ratingInput.value = selectedRating; // ✅ Stocke la note
                    highlightStars(selectedRating);
                });

                // Accessibilité : Touche Enter pour valider
                star.addEventListener("keydown", function (event) {
                    if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        selectedRating = parseInt(this.getAttribute("data-value"), 10);
                        ratingInput.value = selectedRating;
                        highlightStars(selectedRating);
                    }
                });
            });
        } else {
            // Mode lecture : On applique seulement la note et on bloque les interactions
            stars.forEach(star => {
                star.setAttribute("disabled", "true");
                star.classList.add("pointer-events-none");
            });
        }
    });
});
