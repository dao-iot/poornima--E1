function loadData() {
    fetch("/status")
        .then(response => response.json())
        .then(data => {

            /* -----------------------------
               TABLE UPDATE (YOUR LOGIC)
            ------------------------------ */
            const tbody = document.getElementById("data");
            tbody.innerHTML = "";

            Object.keys(data).forEach(sensor => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${sensor}</td>
                    <td>${data[sensor].value}</td>
                    <td class="${data[sensor].status}">
                        ${data[sensor].status}
                    </td>
                `;
                tbody.appendChild(row);
            });

            /* -----------------------------
               SOC PROGRESS BAR (UI ONLY)
            ------------------------------ */
            const socData = data["soc_percent"];

            if (socData && socData.value !== "--") {
                const socValue = Number(socData.value);
                const socFill = document.getElementById("socFill");
                const socText = document.getElementById("socText");

                if (socFill && socText) {
                    socFill.style.width = socValue + "%";
                    socText.innerText = socValue + "%";

                    // Reset classes
                    socFill.classList.remove("warning", "critical");

                    // Color logic
                    if (socValue < 20) {
                        socFill.classList.add("critical");
                    } else if (socValue < 40) {
                        socFill.classList.add("warning");
                    }
                }
            }
        })
        .catch(err => console.error("Error:", err));
}

setInterval(loadData, 2000);
loadData();
