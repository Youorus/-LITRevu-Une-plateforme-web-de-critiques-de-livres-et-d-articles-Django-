function previewImage(event, fieldId) {
    const fileInput = event.target;
    const previewContainer = document.getElementById(`preview-container-${fieldId}`);
    const previewImage = document.getElementById(`preview-${fieldId}`);
    const placeholder = document.getElementById(`placeholder-${fieldId}`);

    // Vérifier si un fichier est sélectionné
    if (fileInput.files.length > 0) {
        const reader = new FileReader();

        reader.onload = function () {
            previewImage.src = reader.result;
            previewContainer.classList.remove("hidden");
            placeholder.classList.add("hidden"); // Cacher le placeholder
        };

        reader.readAsDataURL(fileInput.files[0]); // Lire le fichier sélectionné
    } else {
        // Vérifier si une image existante est définie
        const existingImage = previewImage.getAttribute("data-existing-image");

        if (existingImage) {
            previewImage.src = existingImage;
            previewContainer.classList.remove("hidden");
            placeholder.classList.add("hidden");
        } else {
            previewContainer.classList.add("hidden"); // Masquer l'aperçu
            placeholder.classList.remove("hidden"); // Afficher le placeholder
        }
    }
}
