let partIndex = 0;

function addPart(values = {}) {
    const container = document.getElementById("parts-container");

    const partDiv = document.createElement("div");
    partDiv.className = "part";
    partDiv.dataset.index = partIndex;

    // Prefill values or use empty string
    const customer = values.customer || "";
    const partNumber = values.external_part_number || "";
    const partName = values.external_part_name || "";
    const quantity = values.quantity ?? 1;
    const extraParts = values.extra_parts ?? 0;
    const revision = values.revision_number || "";
    const approval = values.approval_engineer || "";

    const od = values.od || "";
    const length = values.length || "";
    const barOrSlug = values.bar_or_slug || "";
    const workholdingGrip = values.workholding_grip || "";
    const clearance = values.clearance || "";
    const cutoff = values.cutoff_blade_width || "";
    const cleanAxial = values.clean_axial_stock || "";
    const cleanRadial = values.clean_radial_stock || "";
    const roundOD = values.round_outer_dimensions || "";
    const roundLength = values.round_length || "";
    partDiv.innerHTML = `
        <h3>General</h3>
        <label>Customer:<input class="customer" name="customer" list="customer-list" autocomplete="off" value="${customer}"></label>
        <label>Part Number:<input class="external_part_number" value="${partNumber}" required></label>
        <label>Part Name:<input class="external_part_name" value="${partName}"></label>
        <label>Quantity:<input class="quantity" type="number" value="${quantity}" required></label>
        <label>Extra Parts:<input class="extra_parts" type="number" value="${extraParts}" required></label>
        <label>Revision Number:<input class="revision_number" value="${revision}" required></label>
        <label>Approval Engineer:<input class="approval_engineer" value="${approval}"></label>

        <h4>Measurements</h4>
        <label>Outer Diameter:<input class="od" value="${od}" required></label>
        <label>Length:<input class="length" value="${length}" required></label>
        <label>Bar or Slug:<input class="bar_or_slug" value="${barOrSlug}" required></label>
        <label>Workholding Grip:<input class="workholding_grip" value="${workholdingGrip}"></label>
        <label>Clearance:<input class="clearance" value="${clearance}"></label>
        <label>Cutoff Blade Width:<input class="cutoff_blade_width" value="${cutoff}"></label>
        <label>Clean Axial Stock:<input class="clean_axial_stock" value="${cleanAxial}"></label>
        <label>Clean Radial Stock:<input class="clean_radial_stock" value="${cleanRadial}"></label>
        <label>Round Outer Dimensions:<input class="round_outer_dimensions" value="${roundOD}"></label>
        <label>Round Length:<input class="round_length" value="${roundLength}"></label>

        <br>
        <button type="button" class="delete-btn">🗑 Delete Part</button>
        <hr>
    `;

    
    container.appendChild(partDiv);
    updateCustomerDatalist();
    partIndex++;

    const deleteBtn = partDiv.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", () => {
        partDiv.remove();
    });
}

function updateCustomerDatalist() {
    fetch("/customers")
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById(`customer-list`);
        list.innerHTML = "";
        
        data.customers.forEach(name => {
            const option = document.createElement("option");
            option.value = name;
            list.appendChild(option);
        });
    });
}

function saveAll() {
    const parts = document.querySelectorAll("#parts-container .part");
    let valid = true;

    // Hide global error first
    const errorMsg = document.getElementById("error-message");
    errorMsg.style.display = "none";

    const successMsg = document.getElementById("success-message");
    successMsg.style.display = "none";

    
    parts.forEach(part => part.style.backgroundColor = "");


    ////////////////////
    // Error Checking //
    ////////////////////

    // Ensure at least one part
    if (parts.length === 0) {
        errorMsg.textContent = "Please add at least one part before saving.";
        errorMsg.style.display = "block";
        return;
    }

    const requiredFields = {
        "customer": (val) => val.trim() !== "",
        "external_part_number": (val) => val.trim() !== "",
        "external_part_name": (val) => val.trim() !== "",
        "quantity": (val) => !isNaN(parseInt(val)) && parseInt(val) > 0,
        "revision_number": (val) => val.trim() !== "",
        "od": (val) => val.trim() !== "",
        "length": (val) => val.trim() !== "",
        "bar_or_slug": (val) => val.trim() !== ""
    };

    // Check required fields
    parts.forEach((part, idx) => {
        Object.entries(requiredFields).forEach(([className, validator]) => {
            const input = part.querySelector(`.${className}`);
            if (!validator(input.value)) {
                input.style.borderColor = "red";
                input.style.borderWidth = "5px";
                part.style.backgroundColor = "#f8d7da"; // light red highlight
                errorMsg.textContent = `Please fill out all required fields for Parts.`;
                valid = false;
            }
            else {
                input.style.borderColor = "";
                input.style.borderWidth = "";
            }
        });
    });

    if (!valid) {
        errorMsg.style.display = "block";
        return; // stop POST if invalid
    }

    const payload = [];
    parts.forEach(part => {
        payload.push({
            base_stock: {
                customer_id: part.querySelector(".customer").value, //Eventually this needs to lookup customer id
                external_part_number: part.querySelector(".external_part_number").value,
                external_part_name: part.querySelector(".external_part_name").value,
                quantity: part.querySelector(".quantity").value,
                extra_parts: part.querySelector(".extra_parts").value,
                revision_number: part.querySelector(".revision_number").value,
                approval_engineer: part.querySelector(".approval_engineer").value
            },
            lathe_stock: {
                overall_outer_dimensions: part.querySelector(".od").value,
                overall_length: part.querySelector(".length").value,
                bar_or_slug: part.querySelector(".bar_or_slug").value,
                workholding_grip: part.querySelector(".workholding_grip").value,
                clearance: part.querySelector(".clearance").value,
                cutoff_blade_width: part.querySelector(".cutoff_blade_width").value,
                clean_axial_stock: part.querySelector(".clean_axial_stock").value,
                clean_radial_stock: part.querySelector(".clean_radial_stock").value,
                round_outer_dimensions: part.querySelector(".round_outer_dimensions").value,
                round_length: part.querySelector(".round_length").value
            }
        });
    });

    console.log("Payload:", payload);

    fetch("/create/save-parts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            group: {
                group_name: document.getElementById("group_name").value,
            },
            parts: payload
        })
    })
    .then(res => {
        res.json()
        console.log(res)
    })
    .then(data => {
        console.log(data);
        successMsg.style.display = "block";
        errorMsg.style.display = "none";
        updateCustomerDatalist();
    })
    .catch(err => console.error(err));
}