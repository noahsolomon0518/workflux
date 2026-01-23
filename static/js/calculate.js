let dragged = null;

document.addEventListener("dragstart", e => {
    if (e.target.classList.contains("group-card")) {
        dragged = e.target;
    }
});

document.querySelectorAll(".dropzone").forEach(zone => {
    zone.addEventListener("dragover", e => {
        e.preventDefault();
        zone.classList.add("dragover");
    });

    zone.addEventListener("dragleave", () => {
        zone.classList.remove("dragover");
    });

    zone.addEventListener("drop", e => {
        e.preventDefault();
        zone.classList.remove("dragover");

        if (!dragged) return;

        // Prevent dropping into same container
        if (zone.contains(dragged)) return;

        zone.appendChild(dragged);
        dragged = null;
    });
});

document.getElementById("calculate-btn").addEventListener("click", () => {
    const selected = document.querySelectorAll("#groups-right .group-card");

    const groupIds = Array.from(selected).map(el =>
        parseInt(el.dataset.id)
    );

    fetch("/calculate/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ group_ids: groupIds })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Calculation result:", data);
        alert("Calculation complete. Check console.");
    });
});


document.querySelectorAll("#groups-left .group-card").forEach(card => {
    card.addEventListener("click", e => {
        // Prevent drag from triggering toggle
        if (e.target.classList.contains("group-card")) {
            const details = card.querySelector(".group-details");
            if (details) {
                if (details.style.display === "none") {
                    details.style.display = "block";
                } else {
                    details.style.display = "none";
                }
            }
        }
    });
});