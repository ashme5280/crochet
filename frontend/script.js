document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Modal Event Listeners ---
    setupModalTriggers();

    // --- 2. Unit System Switching ---
    const unitSystemSelect = document.getElementById('unitSystem');
    if (unitSystemSelect) {
        unitSystemSelect.addEventListener('change', () => {
            updateUnits();         // For sphere page
            updateCylinderUnits(); // For cylinder page
        });
    }

    // --- 3. Sphere Input Mode Switching ---
    const sphereInputModeSelect = document.getElementById('sphereInputMode');
    if (sphereInputModeSelect) {
        sphereInputModeSelect.addEventListener('change', toggleSphereInputMode);
    }

    // --- 4. Cylinder Input Mode Switching ---
    const cylinderWidthMode = document.getElementById('cylinderWidthMode');
    if (cylinderWidthMode) {
        cylinderWidthMode.addEventListener('change', toggleCylinderWidthMode);
    }

    const cylinderHeightMode = document.getElementById('cylinderHeightMode');
    if (cylinderHeightMode) {
        cylinderHeightMode.addEventListener('change', toggleCylinderHeightMode);
    }

    // --- 5. Generate Button (Universal Handler) ---
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // Check if we are on the cylinder page vs sphere page explicitly
            if (window.location.pathname.includes('cylinder') || document.getElementById('cylinderWidthMode')) {
                generateCylinderPattern();
            } else {
                generatePattern();
            }
        });
    }
});

// --- Modal Helper Functions ---
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function setupModalTriggers() {
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal-overlay')) {
            event.target.classList.remove('active');
        }
    });

    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal-overlay');
            if (modal) modal.classList.remove('active');
        });
    });
}

function toggleSphereIdeas() {
    const content = document.getElementById('sphereIdeasContent');
    const toggleBtn = document.getElementById('sphereIdeasToggle');
    if (content && toggleBtn) {
        if (content.style.display === 'none' || content.style.display === '') {
            content.style.display = 'block';
            toggleBtn.innerText = 'Need Ideas? ▲';
        } else {
            content.style.display = 'none';
            toggleBtn.innerText = 'Need Ideas? ▼';
        }
    }
}

function toggleCylinderIdeas() {
    const content = document.getElementById('cylinderIdeasContent');
    const toggleBtn = document.getElementById('cylinderIdeasToggle');
    if (content && toggleBtn) {
        if (content.style.display === 'none' || content.style.display === '') {
            content.style.display = 'block';
            toggleBtn.innerText = 'Need Ideas? ▲';
        } else {
            content.style.display = 'none';
            toggleBtn.innerText = 'Need Ideas? ▼';
        }
    }
}

// --- Dynamic Unit Conversion Labels ---
function updateUnits() {
    const unit = document.getElementById('unitSystem').value;
    const unitLabel = unit === 'imperial' ? 'inches' : 'centimeters';

    const diamLabel = document.getElementById('sphereDiamLabel');
    if (diamLabel) {
        diamLabel.innerText = `Target Diameter (${unitLabel}):`;
    }
}

function updateCylinderUnits() {
    const unit = document.getElementById('unitSystem').value;
    const unitLabel = unit === 'imperial' ? 'inches' : 'centimeters';

    const diamLabel = document.getElementById('cylinderDiamLabel');
    const heightLabel = document.getElementById('cylinderHeightLabel');

    if (diamLabel) diamLabel.innerText = `Target Diameter (${unitLabel}):`;
    if (heightLabel) heightLabel.innerText = `Target Height (${unitLabel}):`;
}

// --- Input Mode Toggles ---
function toggleSphereInputMode() {
    const mode = document.getElementById('sphereInputMode').value;
    const diamGroup = document.getElementById('sphereDiamGroup');
    const stitchGroup = document.getElementById('sphereStitchGroup');

    if (diamGroup && stitchGroup) {
        if (mode === 'diameter') {
            diamGroup.style.display = 'block';
            stitchGroup.style.display = 'none';
        } else {
            diamGroup.style.display = 'none';
            stitchGroup.style.display = 'block';
        }
    }
}

function toggleCylinderWidthMode() {
    const mode = document.getElementById('cylinderWidthMode').value;
    const diamInput = document.getElementById('cylinderDiameter');
    const stitchInput = document.getElementById('cylinderStitches');

    if (diamInput && stitchInput) {
        if (mode === 'diameter') {
            diamInput.disabled = false;
            stitchInput.disabled = true;
        } else {
            diamInput.disabled = true;
            stitchInput.disabled = false;
        }
    }
}

function toggleCylinderHeightMode() {
    const mode = document.getElementById('cylinderHeightMode').value;
    const heightInput = document.getElementById('cylinderHeight');
    const rowsInput = document.getElementById('cylinderRows');

    if (heightInput && rowsInput) {
        if (mode === 'height') {
            heightInput.disabled = false;
            rowsInput.disabled = true;
        } else {
            heightInput.disabled = true;
            rowsInput.disabled = false;
        }
    }
}

// --- Sphere Pattern Generation API Call ---
async function generatePattern() {
    const unit = document.getElementById('unitSystem').value;
    const yarn = document.getElementById('yarnWeight').value;
    const hook = document.getElementById('hookSize').value;
    const safetyOpt = document.getElementById('safetyEyesOpt').value;
    const stuffingOpt = document.getElementById('stuffingOpt').value;

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&safety_eyes=${encodeURIComponent(safetyOpt)}&stuffing=${encodeURIComponent(stuffingOpt)}`;

    const mode = document.getElementById('sphereInputMode').value;
    if (mode === 'diameter') {
        const val = document.getElementById('sphereDiameter').value;
        queryParams += unit === 'imperial' ? `&max_diameter_inches=${val}` : `&max_diameter_cm=${val}`;
    } else {
        const stitches = document.getElementById('sphereStitches').value;
        queryParams += `&max_stitches=${stitches}`;
    }

    const url = `http://127.0.0.1:8000/sphere/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate pattern.");
        }
        const data = await response.json();

        let sizeVal = unit === 'imperial' ? data.dimensions.diameter_inches : data.dimensions.diameter_cm;
        let sizeStr = `${sizeVal} ${unit === 'imperial' ? 'inches' : 'cm'}`;

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds}</p>`;
        html += `<p><strong>Finished Diameter:</strong> ~${sizeStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need.estimated_yarn}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need.hook}</li>`;
        html += `<li><strong>Safety Eyes:</strong> ${data.supplies_you_need.safety_eyes}</li>`;
        html += `<li><strong>Stuffing:</strong> ${data.supplies_you_need.stuffing_volume}</li>`;
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list">`;
        data.pattern.forEach(step => {
            html += `<li>${step.instruction}</li>`;
        });
        html += `</ul>`;

        outputDiv.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

// --- Cylinder Pattern Generation API Call ---
async function generateCylinderPattern() {
    const unit = document.getElementById('unitSystem').value;
    const yarn = document.getElementById('yarnWeight').value;
    const hook = document.getElementById('hookSize').value;

    // Safely check if cylinderEnds exists, fallback to closed if missing
    const endsElement = document.getElementById('cylinderEnds');
    const endsVal = endsElement ? endsElement.value : 'closed';

    const stuffingOpt = document.getElementById('stuffingOpt').value;

    const isClosed = endsVal === 'closed' ? 'true' : 'false';
    const isStuffing = stuffingOpt === 'yes' ? 'true' : 'false';

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&closed=${isClosed}&stuffing=${isStuffing}`;

    // Width/Diameter parameters
    const widthMode = document.getElementById('cylinderWidthMode').value;
    if (widthMode === 'diameter') {
        const val = document.getElementById('cylinderDiameter').value;
        queryParams += unit === 'imperial' ? `&max_diameter_inches=${val}` : `&max_diameter_cm=${val}`;
    } else {
        const stitches = document.getElementById('cylinderStitches').value;
        queryParams += `&target_stitches=${stitches}`;
    }

    // Height/Rows parameters
    const heightMode = document.getElementById('cylinderHeightMode').value;
    if (heightMode === 'height') {
        const val = document.getElementById('cylinderHeight').value;
        queryParams += unit === 'imperial' ? `&max_height_inches=${val}` : `&max_height_cm=${val}`;
    } else {
        const rows = document.getElementById('cylinderRows').value;
        queryParams += `&height_rounds=${rows}`;
    }

    const url = `http://127.0.0.1:8000/cylinder/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom cylinder pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate pattern.");
        }
        const data = await response.json();

        let diamVal = unit === 'imperial' ? data.dimensions.diameter_inches : data.dimensions.diameter_cm;
        let heightVal = unit === 'imperial' ? data.dimensions.height_inches : data.dimensions.height_cm;
        let unitStr = unit === 'imperial' ? 'inches' : 'cm';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds}</p>`;
        html += `<p><strong>Finished Diameter:</strong> ~${diamVal} ${unitStr}</p>`;
        html += `<p><strong>Finished Height:</strong> ~${heightVal} ${unitStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need.estimated_yarn}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need.hook}</li>`;
        html += `<li><strong>Stuffing Needed:</strong> ${data.supplies_you_need.stuffing_volume}</li>`;
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list">`;
        data.pattern.forEach(step => {
            html += `<li>${step.instruction}`;
            if (step.stuffing_instruction) {
                html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px;">💡 ${step.stuffing_instruction}</div>`;
            }
            html += `</li>`;
        });
        html += `</ul>`;

        outputDiv.innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}
