// ============================================
// PATIENT FORM.JS - Dynamic Form Management
// ============================================

let conditionCount = 0;
let pastConditionCount = 0;
let medicationCount = 0;
let pastMedicationCount = 0;
let allergyCount = 0;
let familyHistoryCount = 0;

// ============================================
// ACTIVE CONDITIONS
// ============================================

function addCondition() {
    conditionCount++;
    const html = `
        <div class="item-block" id="condition${conditionCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${conditionCount}</span> ACTIVE CONDITION</h4>
                <button type="button" onclick="removeElement('condition${conditionCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>CONDITION NAME:</label>
                    <input type="text" id="condName${conditionCount}" placeholder="e.g., Type 2 Diabetes">
                </div>
                <div class="form-group">
                    <label>DIAGNOSED DATE:</label>
                    <input type="date" id="condDate${conditionCount}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>DIAGNOSED BY:</label>
                    <input type="text" id="condDoctor${conditionCount}" placeholder="e.g., Dr. Smith">
                </div>
                <div class="form-group">
                    <label>SEVERITY:</label>
                    <select id="condSeverity${conditionCount}">
                        <option value="">-- SELECT --</option>
                        <option value="mild">MILD</option>
                        <option value="moderate">MODERATE</option>
                        <option value="severe">SEVERE</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>NOTES:</label>
                    <textarea id="condNotes${conditionCount}" rows="2"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('conditionsList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// PAST CONDITIONS
// ============================================

function addPastCondition() {
    pastConditionCount++;
    const html = `
        <div class="item-block" id="pastCondition${pastConditionCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${pastConditionCount}</span> PAST CONDITION</h4>
                <button type="button" onclick="removeElement('pastCondition${pastConditionCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>CONDITION NAME:</label>
                    <input type="text" id="pastCondName${pastConditionCount}">
                </div>
                <div class="form-group">
                    <label>DIAGNOSED DATE:</label>
                    <input type="date" id="pastCondDiagDate${pastConditionCount}">
                </div>
                <div class="form-group">
                    <label>RESOLVED DATE:</label>
                    <input type="date" id="pastCondResolvedDate${pastConditionCount}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>NOTES:</label>
                    <textarea id="pastCondNotes${pastConditionCount}" rows="2"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('pastConditionsList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// CURRENT MEDICATIONS
// ============================================

function addMedication() {
    medicationCount++;
    const html = `
        <div class="item-block" id="medication${medicationCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${medicationCount}</span> CURRENT MEDICATION</h4>
                <button type="button" onclick="removeElement('medication${medicationCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>MEDICATION NAME:</label>
                    <input type="text" id="medName${medicationCount}" placeholder="e.g., Metformin">
                </div>
                <div class="form-group">
                    <label>DOSAGE:</label>
                    <input type="text" id="medDosage${medicationCount}" placeholder="e.g., 500mg">
                </div>
                <div class="form-group">
                    <label>FREQUENCY:</label>
                    <input type="text" id="medFreq${medicationCount}" placeholder="e.g., twice daily">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>ROUTE:</label>
                    <select id="medRoute${medicationCount}">
                        <option value="">-- SELECT --</option>
                        <option value="oral">ORAL</option>
                        <option value="iv">INTRAVENOUS (IV)</option>
                        <option value="topical">TOPICAL</option>
                        <option value="injection">INJECTION</option>
                        <option value="inhaled">INHALED</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>STARTED DATE:</label>
                    <input type="date" id="medStartDate${medicationCount}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>PRESCRIBED BY:</label>
                    <input type="text" id="medDoctor${medicationCount}" placeholder="e.g., Dr. Johnson">
                </div>
                <div class="form-group">
                    <label>PURPOSE:</label>
                    <input type="text" id="medPurpose${medicationCount}" placeholder="e.g., Diabetes management">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>NOTES:</label>
                    <textarea id="medNotes${medicationCount}" rows="2" placeholder="e.g., Take with food"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('medicationsList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// PAST MEDICATIONS
// ============================================

function addPastMedication() {
    pastMedicationCount++;
    const html = `
        <div class="item-block" id="pastMedication${pastMedicationCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${pastMedicationCount}</span> DISCONTINUED MEDICATION</h4>
                <button type="button" onclick="removeElement('pastMedication${pastMedicationCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>MEDICATION NAME:</label>
                    <input type="text" id="pastMedName${pastMedicationCount}">
                </div>
                <div class="form-group">
                    <label>DOSAGE:</label>
                    <input type="text" id="pastMedDosage${pastMedicationCount}">
                </div>
                <div class="form-group">
                    <label>FREQUENCY:</label>
                    <input type="text" id="pastMedFreq${pastMedicationCount}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>STARTED DATE:</label>
                    <input type="date" id="pastMedStartDate${pastMedicationCount}">
                </div>
                <div class="form-group">
                    <label>STOPPED DATE:</label>
                    <input type="date" id="pastMedStopDate${pastMedicationCount}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>REASON STOPPED:</label>
                    <textarea id="pastMedReason${pastMedicationCount}" rows="2"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('pastMedicationsList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// ALLERGIES
// ============================================

function addAllergy() {
    allergyCount++;
    const html = `
        <div class="item-block" id="allergy${allergyCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${allergyCount}</span> ALLERGY / INTOLERANCE</h4>
                <button type="button" onclick="removeElement('allergy${allergyCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>ALLERGEN:</label>
                    <input type="text" id="allergen${allergyCount}" placeholder="e.g., Penicillin">
                </div>
                <div class="form-group">
                    <label>REACTION:</label>
                    <input type="text" id="allergyReaction${allergyCount}" placeholder="e.g., Skin rash, hives">
                </div>
                <div class="form-group">
                    <label>SEVERITY:</label>
                    <select id="allergySeverity${allergyCount}">
                        <option value="">-- SELECT --</option>
                        <option value="mild">MILD</option>
                        <option value="moderate">MODERATE</option>
                        <option value="severe">SEVERE</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>ONSET DATE:</label>
                    <input type="date" id="allergyOnset${allergyCount}">
                </div>
                <div class="form-group">
                    <label>NOTES:</label>
                    <textarea id="allergyNotes${allergyCount}" rows="2"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('allergiesList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// FAMILY HISTORY
// ============================================

function addFamilyHistory() {
    familyHistoryCount++;
    const html = `
        <div class="item-block" id="family${familyHistoryCount}">
            <div class="item-block-header">
                <h4><span class="item-number">#${familyHistoryCount}</span> FAMILY MEMBER</h4>
                <button type="button" onclick="removeElement('family${familyHistoryCount}')" class="danger">REMOVE</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>RELATIVE:</label>
                    <select id="familyRelative${familyHistoryCount}">
                        <option value="">-- SELECT --</option>
                        <option value="Mother">MOTHER</option>
                        <option value="Father">FATHER</option>
                        <option value="Sister">SISTER</option>
                        <option value="Brother">BROTHER</option>
                        <option value="Maternal Grandmother">MATERNAL GRANDMOTHER</option>
                        <option value="Maternal Grandfather">MATERNAL GRANDFATHER</option>
                        <option value="Paternal Grandmother">PATERNAL GRANDMOTHER</option>
                        <option value="Paternal Grandfather">PATERNAL GRANDFATHER</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>AGE:</label>
                    <input type="number" id="familyAge${familyHistoryCount}">
                </div>
                <div class="form-group">
                    <label>STATUS:</label>
                    <select id="familyStatus${familyHistoryCount}">
                        <option value="alive">ALIVE</option>
                        <option value="deceased">DECEASED</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>CONDITIONS (comma separated):</label>
                    <textarea id="familyConditions${familyHistoryCount}" rows="2" placeholder="e.g., Diabetes (age 45), Heart Disease (age 60)"></textarea>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>NOTES:</label>
                    <textarea id="familyNotes${familyHistoryCount}" rows="2"></textarea>
                </div>
            </div>
        </div>
    `;
    document.getElementById('familyHistoryList').insertAdjacentHTML('beforeend', html);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function removeElement(elementId) {
    document.getElementById(elementId).remove();
}

// ============================================
// FORM SUBMISSION
// ============================================

document.getElementById('patientForm').onsubmit = async function(e) {
    e.preventDefault();
    
    // Collect basic demographics
    const patientData = {
        patientId: document.getElementById('patientId').value,
        name: `${document.getElementById('firstName').value} ${document.getElementById('lastName').value}`,
        dateOfBirth: document.getElementById('dob').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value,
        emergencyContact: {
            name: document.getElementById('emergencyName').value,
            relationship: document.getElementById('emergencyRelation').value,
            phone: document.getElementById('emergencyPhone').value
        },
        activeConditions: [],
        pastConditions: [],
        activeMedications: [],
        pastMedications: [],
        allergies: [],
        familyHistory: [],
        socialHistory: {
            smokingStatus: document.getElementById('smokingStatus').value,
            alcoholUse: document.getElementById('alcoholUse').value,
            occupation: document.getElementById('occupation').value,
            exerciseHabits: document.getElementById('exerciseHabits').value,
            diet: document.getElementById('diet').value
        },
        surgicalHistory: document.getElementById('surgicalHistory').value,
        immunizations: document.getElementById('immunizations').value,
        generalNotes: document.getElementById('generalNotes').value,
        visits: [],
        labResults: []
    };
    
    // Collect active conditions
    for (let i = 1; i <= conditionCount; i++) {
        const nameEl = document.getElementById(`condName${i}`);
        if (nameEl && nameEl.value) {
            patientData.activeConditions.push({
                condition: nameEl.value,
                diagnosedDate: document.getElementById(`condDate${i}`).value,
                diagnosedBy: document.getElementById(`condDoctor${i}`).value,
                severity: document.getElementById(`condSeverity${i}`).value,
                notes: document.getElementById(`condNotes${i}`).value,
                status: 'active'
            });
        }
    }
    
    // Collect past conditions
    for (let i = 1; i <= pastConditionCount; i++) {
        const nameEl = document.getElementById(`pastCondName${i}`);
        if (nameEl && nameEl.value) {
            patientData.pastConditions.push({
                condition: nameEl.value,
                diagnosedDate: document.getElementById(`pastCondDiagDate${i}`).value,
                resolvedDate: document.getElementById(`pastCondResolvedDate${i}`).value,
                notes: document.getElementById(`pastCondNotes${i}`).value
            });
        }
    }
    
    // Collect current medications
    for (let i = 1; i <= medicationCount; i++) {
        const nameEl = document.getElementById(`medName${i}`);
        if (nameEl && nameEl.value) {
            patientData.activeMedications.push({
                medication: nameEl.value,
                dosage: document.getElementById(`medDosage${i}`).value,
                frequency: document.getElementById(`medFreq${i}`).value,
                route: document.getElementById(`medRoute${i}`).value,
                startedDate: document.getElementById(`medStartDate${i}`).value,
                prescribedBy: document.getElementById(`medDoctor${i}`).value,
                purpose: document.getElementById(`medPurpose${i}`).value,
                notes: document.getElementById(`medNotes${i}`).value,
                status: 'active'
            });
        }
    }
    
    // Collect past medications
    for (let i = 1; i <= pastMedicationCount; i++) {
        const nameEl = document.getElementById(`pastMedName${i}`);
        if (nameEl && nameEl.value) {
            patientData.pastMedications.push({
                medication: nameEl.value,
                dosage: document.getElementById(`pastMedDosage${i}`).value,
                frequency: document.getElementById(`pastMedFreq${i}`).value,
                startedDate: document.getElementById(`pastMedStartDate${i}`).value,
                stoppedDate: document.getElementById(`pastMedStopDate${i}`).value,
                reasonStopped: document.getElementById(`pastMedReason${i}`).value
            });
        }
    }
    
    // Collect allergies
    for (let i = 1; i <= allergyCount; i++) {
        const allergenEl = document.getElementById(`allergen${i}`);
        if (allergenEl && allergenEl.value) {
            patientData.allergies.push({
                allergen: allergenEl.value,
                reaction: document.getElementById(`allergyReaction${i}`).value,
                severity: document.getElementById(`allergySeverity${i}`).value,
                onsetDate: document.getElementById(`allergyOnset${i}`).value,
                notes: document.getElementById(`allergyNotes${i}`).value
            });
        }
    }
    
    // Collect family history
    for (let i = 1; i <= familyHistoryCount; i++) {
        const relativeEl = document.getElementById(`familyRelative${i}`);
        if (relativeEl && relativeEl.value) {
            patientData.familyHistory.push({
                relative: relativeEl.value,
                age: document.getElementById(`familyAge${i}`).value,
                livingStatus: document.getElementById(`familyStatus${i}`).value,
                conditions: document.getElementById(`familyConditions${i}`).value,
                notes: document.getElementById(`familyNotes${i}`).value
            });
        }
    }
    
    // Save patient
    try {
        let result;
        if (isEditMode && editingPatientId) {
            // Update existing patient
            result = await apiPut(`/api/patients/${editingPatientId}`, patientData);
            showMessage('PATIENT UPDATED SUCCESSFULLY!', 'success');
        } else {
            // Create new patient
            result = await apiPost('/api/patients', patientData);
            showMessage('PATIENT REGISTERED SUCCESSFULLY!', 'success');
        }
        
        setTimeout(() => {
            if (isEditMode) {
                sessionStorage.setItem('currentPatientId', editingPatientId);
                window.location.href = '/patient-view';
            } else {
                window.location.href = '/';
            }
        }, 2000);
    } catch (error) {
        showMessage('ERROR SAVING PATIENT: ' + error.message, 'error');
    }
};
