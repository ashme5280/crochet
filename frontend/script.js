const API_BASE_URL = "https://ashme5280-amigurumi-api.onrender.com";

document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Modal Event Listeners ---
    setupModalTriggers();

    // --- 2. Unit System Switching ---
    const unitSystemSelect = document.getElementById('unitSystem');
    if (unitSystemSelect) {
        unitSystemSelect.addEventListener('change', () => {
            updateUnits();         // For sphere page
            updateCylinderUnits(); // For cylinder page
            updateEggUnits();      // For egg page
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

    // --- 5. Egg Input Mode & Shell Mode Switching ---
    const eggInputMode = document.getElementById('eggInputMode');
    if (eggInputMode) {
        eggInputMode.addEventListener('change', toggleEggInputMode);
    }

    const eggShellMode = document.getElementById('eggShellMode');
    if (eggShellMode) {
        eggShellMode.addEventListener('change', toggleEggShellMode);
        toggleEggShellMode(); // Ensure correct visibility on initial page load
    }

    // --- 6. Generate Button (Universal Handler) ---
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        generateBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (window.location.pathname.includes('cylinder') || document.getElementById('cylinderWidthMode')) {
                generateCylinderPattern();
            } else if (window.location.pathname.includes('cone') || document.getElementById('coneWidthMode')) {
                generateConePattern();
            } else if (window.location.pathname.includes('oval') || document.getElementById('ovalLength')) {
                generateOvalPattern();
            } else if (window.location.pathname.includes('egg') || document.getElementById('eggInputMode')) {
                generateEggPattern();
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

function toggleEggIdeas() {
    const content = document.getElementById('eggIdeasContent');
    const toggleBtn = document.getElementById('eggIdeasToggle');
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

function updateEggUnits() {
    const unit = document.getElementById('unitSystem').value;
    const unitLabel = unit === 'imperial' ? 'inches' : 'centimeters';

    const diamLabel = document.getElementById('eggDiamLabel');
    if (diamLabel) {
        diamLabel.innerText = `Target Max Diameter (${unitLabel}):`;
    }
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
    const diamGroup = document.getElementById('cylinderDiamGroup');
    const stitchGroup = document.getElementById('cylinderStitchGroup');

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

function toggleCylinderHeightMode() {
    const mode = document.getElementById('cylinderHeightMode').value;
    const heightGroup = document.getElementById('cylinderHeightGroup');
    const rowsGroup = document.getElementById('cylinderRowsGroup');

    if (heightGroup && rowsGroup) {
        if (mode === 'height') {
            heightGroup.style.display = 'block';
            rowsGroup.style.display = 'none';
        } else {
            heightGroup.style.display = 'none';
            rowsGroup.style.display = 'block';
        }
    }
}

function toggleEggInputMode() {
    const mode = document.getElementById('eggInputMode').value;
    const diamGroup = document.getElementById('eggDiamGroup');
    const stitchGroup = document.getElementById('eggStitchGroup');

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

function toggleEggShellMode() {
    const shellMode = document.getElementById('eggShellMode')?.value;
    const stuffingDetails = document.getElementById('eggStuffingDetails');
    const stuffingGroup = document.getElementById('eggStuffingGroup');
    const isWhole = shellMode === 'Whole shell';

    if (stuffingDetails) {
        stuffingDetails.style.display = isWhole ? 'block' : 'none';
    }
    if (stuffingGroup) {
        stuffingGroup.style.display = isWhole ? 'block' : 'none';
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

    const url = `${API_BASE_URL}/sphere/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate pattern.");
        }
        const data = await response.json();

        let sizeVal = unit === 'imperial' ? data.dimensions?.diameter_inches : data.dimensions?.diameter_cm;
        let sizeStr = sizeVal ? `${sizeVal} ${unit === 'imperial' ? 'inches' : 'cm'}` : 'N/A';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds || 'N/A'}</p>`;
        html += `<p><strong>Finished Diameter:</strong> ~${sizeStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need?.estimated_yarn || 'N/A'}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need?.hook || hook + ' mm'}</li>`;
        html += `<li><strong>Safety Eyes:</strong> ${data.supplies_you_need?.safety_eyes || safetyOpt}</li>`;
        html += `<li><strong>Stuffing:</strong> ${data.supplies_you_need?.stuffing_volume || stuffingOpt}</li>`;
        html += `</ul>`;
        html += `</div>`;
        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list" id="patternList">`;

        if (data.pattern && Array.isArray(data.pattern)) {
            data.pattern.forEach((step, index) => {
                const instructionText = typeof step === 'string' ? step : step.instruction;
                const stuffingText = step.stuffing_instruction || '';

                html += `<li data-index="${index}">`;
                html += `<label class="checkbox-label">`;
                html += `<input type="checkbox" class="row-checkbox"> `;
                html += `<span>${instructionText}</span>`;
                html += `</label>`;
                if (stuffingText) {
                    html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px; margin-left: 24px;">💡 ${stuffingText}</div>`;
                }
                html += `</li>`;
            });
        }
        html += `</ul>`;

        outputDiv.innerHTML = html;

        const checkboxes = outputDiv.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const listItem = e.target.closest('li');
                if (e.target.checked) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            });
        });
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

    const endsElement = document.getElementById('cylinderEnds');
    const endsVal = endsElement ? endsElement.value : 'closed';

    const stuffingOpt = document.getElementById('stuffingOpt').value;

    const isClosed = endsVal === 'closed' ? 'true' : 'false';
    const isStuffing = stuffingOpt === 'yes' ? 'true' : 'false';

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&closed=${isClosed}&stuffing=${isStuffing}`;

    const widthMode = document.getElementById('cylinderWidthMode').value;
    if (widthMode === 'diameter') {
        const val = document.getElementById('cylinderDiameter').value;
        queryParams += unit === 'imperial' ? `&max_diameter_inches=${val}` : `&max_diameter_cm=${val}`;
    } else {
        const stitches = document.getElementById('cylinderStitches').value;
        queryParams += `&target_stitches=${stitches}`;
    }

    const heightMode = document.getElementById('cylinderHeightMode').value;
    if (heightMode === 'height') {
        const val = document.getElementById('cylinderHeight').value;
        queryParams += unit === 'imperial' ? `&max_height_inches=${val}` : `&max_height_cm=${val}`;
    } else {
        const rows = document.getElementById('cylinderRows').value;
        queryParams += `&height_rounds=${rows}`;
    }

    const url = `${API_BASE_URL}/cylinder/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom cylinder pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate pattern.");
        }
        const data = await response.json();

        let diamVal = unit === 'imperial' ? data.dimensions?.diameter_inches : data.dimensions?.diameter_cm;
        let heightVal = unit === 'imperial' ? data.dimensions?.height_inches : data.dimensions?.height_cm;
        let unitStr = unit === 'imperial' ? 'inches' : 'cm';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds || 'N/A'}</p>`;
        html += `<p><strong>Finished Diameter:</strong> ~${diamVal || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Finished Height:</strong> ~${heightVal || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need?.estimated_yarn || 'N/A'}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need?.hook || hook + ' mm'}</li>`;
        html += `<li><strong>Stuffing Needed:</strong> ${data.supplies_you_need?.stuffing_volume || 'Standard'}</li>`;
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list" id="cylinderPatternList">`;
        if (data.pattern && Array.isArray(data.pattern)) {
            data.pattern.forEach((step, index) => {
                const instructionText = typeof step === 'string' ? step : step.instruction;
                const stuffingText = step.stuffing_instruction || '';

                html += `<li data-index="${index}">`;
                html += `<label class="checkbox-label">`;
                html += `<input type="checkbox" class="row-checkbox"> `;
                html += `<span>${instructionText}</span>`;
                html += `</label>`;
                if (stuffingText) {
                    html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px; margin-left: 24px;">💡 ${stuffingText}</div>`;
                }
                html += `</li>`;
            });
        }
        html += `</ul>`;

        outputDiv.innerHTML = html;

        const checkboxes = outputDiv.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const listItem = e.target.closest('li');
                if (e.target.checked) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            });
        });

    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

// --- Cone Pattern Generation API Call ---
async function generateConePattern() {
    const unit = document.getElementById('unitSystem').value;
    const yarn = document.getElementById('yarnWeight').value;
    const hook = document.getElementById('hookSize').value;
    const tipOpt = document.getElementById('coneTip').value;
    const stuffingOpt = document.getElementById('stuffingOpt').value;

    const isStuffing = stuffingOpt === 'yes' ? 'true' : 'false';

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&tip_style=${encodeURIComponent(tipOpt)}&stuffing=${isStuffing}`;

    const widthMode = document.getElementById('coneWidthMode').value;
    if (widthMode === 'diameter') {
        const val = document.getElementById('coneDiameter').value;
        queryParams += unit === 'imperial' ? `&max_diameter_inches=${val}` : `&max_diameter_cm=${val}`;
    } else {
        const stitches = document.getElementById('coneStitches').value;
        queryParams += `&target_base_stitches=${stitches}`;
    }

    const heightMode = document.getElementById('coneHeightMode').value;
    if (heightMode === 'height') {
        const val = document.getElementById('coneHeight').value;
        queryParams += unit === 'imperial' ? `&max_height_inches=${val}` : `&max_height_cm=${val}`;
    } else {
        const rows = document.getElementById('coneRows').value;
        queryParams += `&height_rounds=${rows}`;
    }

    const url = `${API_BASE_URL}/cone/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom cone pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate cone pattern.");
        }
        const data = await response.json();

        let diamVal = unit === 'imperial' ? data.dimensions?.diameter_inches : data.dimensions?.diameter_cm;
        let heightVal = unit === 'imperial' ? data.dimensions?.height_inches : data.dimensions?.height_cm;
        let unitStr = unit === 'imperial' ? 'inches' : 'cm';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds || 'N/A'}</p>`;
        html += `<p><strong>Base Diameter:</strong> ~${diamVal || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Finished Height:</strong> ~${heightVal || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need?.estimated_yarn || 'N/A'}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need?.hook || hook + ' mm'}</li>`;
        html += `<li><strong>Stuffing Needed:</strong> ${data.supplies_you_need?.stuffing_volume || 'Standard'}</li>`;
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list" id="conePatternList">`;
        if (data.pattern && Array.isArray(data.pattern)) {
            data.pattern.forEach((step, index) => {
                const instructionText = typeof step === 'string' ? step : step.instruction;
                const stuffingText = step.stuffing_instruction || '';

                html += `<li data-index="${index}">`;
                html += `<label class="checkbox-label">`;
                html += `<input type="checkbox" class="row-checkbox"> `;
                html += `<span>${instructionText}</span>`;
                html += `</label>`;
                if (stuffingText) {
                    html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px; margin-left: 24px;">💡 ${stuffingText}</div>`;
                }
                html += `</li>`;
            });
        }
        html += `</ul>`;

        outputDiv.innerHTML = html;

        const checkboxes = outputDiv.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const listItem = e.target.closest('li');
                if (e.target.checked) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            });
        });

    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

// --- Oval Pattern Generation API Call ---
async function generateOvalPattern() {
    const unit = document.getElementById('unitSystem').value;
    const yarn = document.getElementById('yarnWeight').value;
    const hook = document.getElementById('hookSize').value;
    const lengthVal = document.getElementById('ovalLength').value;
    const heightVal = document.getElementById('ovalHeight').value;
    const stuffingOpt = document.getElementById('stuffingOpt').value;

    const isStuffing = stuffingOpt === 'yes' ? 'true' : 'false';

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&stuffing=${isStuffing}`;
    queryParams += unit === 'imperial' ? `&max_length_inches=${lengthVal}&max_height_inches=${heightVal}` : `&max_length_cm=${lengthVal}&max_height_cm=${heightVal}`;

    const url = `${API_BASE_URL}/oval/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom oval pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate oval pattern.");
        }
        const data = await response.json();

        let lengthDim = unit === 'imperial' ? data.dimensions?.max_length_inches : data.dimensions?.max_length_cm;
        let widthDim = unit === 'imperial' ? data.dimensions?.max_width_inches : data.dimensions?.max_width_cm;
        let heightDim = unit === 'imperial' ? data.dimensions?.height_inches : data.dimensions?.height_cm;
        let unitStr = unit === 'imperial' ? 'inches' : 'cm';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds || 'N/A'}</p>`;
        html += `<p><strong>Finished Length:</strong> ~${lengthDim || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Finished Width:</strong> ~${widthDim || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Calculated Height:</strong> ~${heightDim || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need?.estimated_yarn || 'N/A'}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need?.hook || hook + ' mm'}</li>`;
        html += `<li><strong>Stuffing Needed:</strong> ${data.supplies_you_need?.stuffing_volume || 'Standard'}</li>`;
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3><ul class="pattern-list" id="ovalPatternList">`;
        if (data.pattern && Array.isArray(data.pattern)) {
            data.pattern.forEach((step, index) => {
                const instructionText = typeof step === 'string' ? step : step.instruction;
                const stuffingText = step.stuffing_instruction || '';

                html += `<li data-index="${index}">`;
                html += `<label class="checkbox-label">`;
                html += `<input type="checkbox" class="row-checkbox"> `;
                html += `<span>${instructionText}</span>`;
                html += `</label>`;
                if (stuffingText) {
                    html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px; margin-left: 24px;">💡 ${stuffingText}</div>`;
                }
                html += `</li>`;
            });
        }
        html += `</ul>`;

        outputDiv.innerHTML = html;

        const checkboxes = outputDiv.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const listItem = e.target.closest('li');
                if (e.target.checked) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            });
        });

    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

// --- Egg Pattern Generation API Call ---
async function generateEggPattern() {
    const unit = document.getElementById('unitSystem').value;
    const yarn = document.getElementById('yarnWeight').value;
    const hook = document.getElementById('hookSize').value;
    const inputMode = document.getElementById('eggInputMode').value;
    const shellMode = document.getElementById('eggShellMode').value;
    const stuffingOpt = shellMode === 'Whole shell'
        ? (document.getElementById('stuffingOpt')?.value || 'yes')
        : 'no';

    let queryParams = `?yarn_weight=${encodeURIComponent(yarn)}&hook_size_mm=${encodeURIComponent(hook)}&shell_mode=${encodeURIComponent(shellMode)}&stuffing=${encodeURIComponent(stuffingOpt)}`;

    if (inputMode === 'diameter') {
        const diamVal = document.getElementById('eggDiameter').value;
        queryParams += unit === 'imperial'
            ? `&max_diameter_inches=${diamVal}`
            : `&max_diameter_cm=${diamVal}`;
    } else {
        const stitchesVal = document.getElementById('eggStitches').value;
        queryParams += `&max_diameter_stitches=${stitchesVal}`;
    }

    const url = `http://127.0.0.1:8000/egg/${queryParams}`;

    const outputDiv = document.getElementById('outputResults');
    outputDiv.innerHTML = "<p>Generating your custom egg pattern...</p>";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Failed to generate egg pattern.");
        }
        const data = await response.json();

        const diamDim = unit === 'imperial' ? data.dimensions?.diameter_inches : data.dimensions?.diameter_cm;
        const heightDim = unit === 'imperial' ? data.dimensions?.height_inches : data.dimensions?.height_cm;
        const unitStr = unit === 'imperial' ? 'inches' : 'cm';

        let html = `<h3>Pattern Specifications</h3>`;
        html += `<div class="metrics-card">`;
        html += `<p><strong>Shell Mode:</strong> ${data.parameters?.shell_mode || shellMode}</p>`;
        html += `<p><strong>Total Rounds:</strong> ${data.total_rounds || 'N/A'}</p>`;
        html += `<p><strong>Finished Max Diameter:</strong> ~${diamDim || 'N/A'} ${unitStr} (${data.parameters?.max_diameter_stitches || 'N/A'} sts)</p>`;
        html += `<p><strong>Calculated Height:</strong> ~${heightDim || 'N/A'} ${unitStr}</p>`;
        html += `<p><strong>Supplies You Need:</strong></p>`;
        html += `<ul class="supplies-list">`;
        html += `<li><strong>Estimated Yarn:</strong> ${data.supplies_you_need?.estimated_yarn || 'N/A'}</li>`;
        html += `<li><strong>Hook:</strong> ${data.supplies_you_need?.hook || hook + ' mm'}</li>`;
        if (shellMode === 'Whole shell') {
            html += `<li><strong>Stuffing Needed:</strong> ${data.supplies_you_need?.stuffing_volume || 'Standard'}</li>`;
        }
        html += `</ul>`;
        html += `</div>`;

        html += `<h3>Round-by-Round Instructions</h3>`;

        if (data.pattern && Array.isArray(data.pattern)) {
            if (shellMode === 'Split in half') {
                const topSteps = data.pattern.filter(s => s.phase && s.phase.startsWith('top_half'));
                const bottomSteps = data.pattern.filter(s => s.phase && s.phase.startsWith('bottom_half'));

                html += `<h4>Part 1: Top Half (Pointed Crown)</h4>`;
                html += renderEggStepList(topSteps, 'eggTopPatternList');

                html += `<h4>Part 2: Bottom Half (Rounded Base)</h4>`;
                html += renderEggStepList(bottomSteps, 'eggBottomPatternList');
            } else {
                html += renderEggStepList(data.pattern, 'eggPatternList');
            }
        }

        outputDiv.innerHTML = html;

        const checkboxes = outputDiv.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const listItem = e.target.closest('li');
                if (e.target.checked) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            });
        });
    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

function renderEggStepList(steps, listId) {
    let html = `<ul class="pattern-list" id="${listId}">`;
    steps.forEach((step, index) => {
        const instructionText = typeof step === 'string' ? step : step.instruction;
        const stuffingText = step.stuffing_instruction || '';

        html += `<li data-index="${index}">`;
        html += `<label class="checkbox-label">`;
        html += `<input type="checkbox" class="row-checkbox"> `;
        html += `<span>${instructionText}</span>`;
        html += `</label>`;
        if (stuffingText) {
            html += `<div style="color: #64748b; font-size: 0.9em; margin-top: 2px; margin-left: 24px;">💡 ${stuffingText}</div>`;
        }
        html += `</li>`;
    });
    html += `</ul>`;
    return html;
}
