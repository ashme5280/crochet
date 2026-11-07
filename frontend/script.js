document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Modal Event Listeners ---
    setupModalTriggers();

    // --- 2. Unit System Switching ---
    const unitSystemSelect = document.getElementById('unitSystem');
    if (unitSystemSelect) {
        unitSystemSelect.addEventListener('change', updateUnits);
    }

    // --- 3. Sphere Input Mode Switching ---
    const sphereInputModeSelect = document.getElementById('sphereInputMode');
    if (sphereInputModeSelect) {
        sphereInputModeSelect.addEventListener('change', toggleSphereInputMode);
    }

    // --- 4. Generate Button ---
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generatePattern);
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
    // Close modal when clicking outside the card overlay
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal-overlay')) {
            event.target.classList.remove('active');
        }
    });

    // Close buttons inside modals
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

// --- Dynamic Unit Conversion Labels ---
function updateUnits() {
    const unit = document.getElementById('unitSystem').value;
    const unitLabel = unit === 'imperial' ? 'inches' : 'centimeters';

    const diamLabel = document.getElementById('sphereDiamLabel');
    if (diamLabel) {
        diamLabel.innerText = `Target Diameter (${unitLabel}):`;
    }
}

// --- Sphere Input Mode Toggle ---
function toggleSphereInputMode() {
    const mode = document.getElementById('sphereInputMode').value;
    const diamInput = document.getElementById('sphereDiameter');
    const stitchInput = document.getElementById('sphereStitches');

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

// --- Pattern Generation API Call ---
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
