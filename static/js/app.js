// ============================================
// MAIN APP.JS - Common Functions
// ============================================

// ============================================
// API HELPER FUNCTIONS
// ============================================

async function apiGet(endpoint) {
    try {
        const response = await fetch(endpoint);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
        
        return result;
    } catch (error) {
        console.error('API GET Error:', error);
        throw error;
    }
}

async function apiPost(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            // Extract error message from response body
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
        
        return result;
    } catch (error) {
        console.error('API POST Error:', error);
        throw error;
    }
}

async function apiPut(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
        
        return result;
    } catch (error) {
        console.error('API PUT Error:', error);
        throw error;
    }
}

// ============================================
// PATIENT FUNCTIONS
// ============================================

async function loadRecentPatients() {
    try {
        const patients = await apiGet('/api/patients');
        displayPatients(patients);
        document.getElementById('totalPatients').textContent = patients.length;
    } catch (error) {
        document.getElementById('recentPatients').innerHTML = 
            '<div class="alert alert-error">ERROR LOADING PATIENT DATABASE</div>';
    }
}

function displayPatients(patients) {
    const container = document.getElementById('recentPatients');
    
    if (patients.length === 0) {
        container.innerHTML = '<div class="info-box">NO PATIENTS REGISTERED YET</div>';
        return;
    }
    
    let html = '';
    // Show most recent 10 patients
    const recentPatients = patients.slice(-10).reverse();
    
    recentPatients.forEach(patient => {
        const lastVisit = patient.visits && patient.visits.length > 0 
            ? patient.visits[patient.visits.length - 1].date 
            : 'NO VISITS';
        
        html += `
            <div class="patient-card" onclick="viewPatient('${patient.patientId}')">
                <h3>► ${patient.name} [${patient.patientId}]</h3>
                <p>AGE: ${patient.age} | GENDER: ${patient.gender.toUpperCase()}</p>
                <p>LAST VISIT: ${lastVisit}</p>
                <div style="margin-top: 10px;">
                    <button onclick="event.stopPropagation(); viewPatient('${patient.patientId}')" class="primary">VIEW RECORD</button>
                    <button onclick="event.stopPropagation(); newVisit('${patient.patientId}')" class="success">NEW VISIT</button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function searchPatient() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    
    if (!searchTerm) {
        alert('PLEASE ENTER SEARCH TERM');
        return;
    }
    
    try {
        const results = await apiPost('/api/patients/search', { searchTerm });
        
        const resultsDiv = document.getElementById('searchResults');
        const resultsContainer = document.getElementById('resultsContainer');
        
        if (results.length === 0) {
            resultsContainer.innerHTML = '<div class="info-box warning">NO PATIENTS FOUND</div>';
        } else {
            displaySearchResults(results);
        }
        
        resultsDiv.classList.remove('hidden');
    } catch (error) {
        alert('ERROR SEARCHING PATIENTS');
    }
}

function displaySearchResults(patients) {
    const container = document.getElementById('resultsContainer');
    
    let html = '';
    patients.forEach(patient => {
        const lastVisit = patient.visits && patient.visits.length > 0 
            ? patient.visits[patient.visits.length - 1].date 
            : 'NO VISITS';
        
        html += `
            <div class="patient-card" onclick="viewPatient('${patient.patientId}')">
                <h3>► ${patient.name} [${patient.patientId}]</h3>
                <p>AGE: ${patient.age} | GENDER: ${patient.gender.toUpperCase()}</p>
                <p>LAST VISIT: ${lastVisit}</p>
                <div style="margin-top: 10px;">
                    <button onclick="event.stopPropagation(); viewPatient('${patient.patientId}')" class="primary">VIEW RECORD</button>
                    <button onclick="event.stopPropagation(); newVisit('${patient.patientId}')" class="success">NEW VISIT</button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function viewPatient(patientId) {
    sessionStorage.setItem('currentPatientId', patientId);
    window.location.href = '/patient-view';
}

function newVisit(patientId) {
    sessionStorage.setItem('currentPatientId', patientId);
    window.location.href = '/new-visit';
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function getCurrentDate() {
    const date = new Date();
    return date.toISOString().split('T')[0];
}

function getCurrentDateTime() {
    return new Date().toISOString();
}

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchPatient();
            }
        });
    }
});
