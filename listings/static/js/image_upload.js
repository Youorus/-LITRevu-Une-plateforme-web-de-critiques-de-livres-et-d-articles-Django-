function previewImage(event, fieldId) {
    let fileInput = event.target;
    let previewContainer = document.getElementById(`preview-container-${fieldId}`);
    let previewImage = document.getElementById(`preview-${fieldId}`);

    // Vérifier si un fichier est sélectionné
    if (fileInput.files.length > 0) {
        let reader = new FileReader();

        reader.onload = function(){
            previewImage.src = reader.result;
            previewContainer.classList.remove("hidden"); // Afficher l'aperçu
        }

        reader.readAsDataURL(fileInput.files[0]); // Lire le fichier sélectionné
    } else {
        previewContainer.classList.add("hidden"); // Masquer si aucun fichier
    }
}
