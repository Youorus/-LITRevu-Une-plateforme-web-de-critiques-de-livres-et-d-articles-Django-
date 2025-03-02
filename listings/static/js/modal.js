 function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove("hidden");
            modal.setAttribute("aria-hidden", "false");
        }
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add("hidden");
            modal.setAttribute("aria-hidden", "true");
        }
    }

    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            document.querySelectorAll("[id^='deleteTicketModal']").forEach(modal => {
                if (!modal.classList.contains("hidden")) {
                    closeModal(modal.id);
                }
            });
        }
    });