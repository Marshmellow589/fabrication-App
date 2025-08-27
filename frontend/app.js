// API base URL
const API_BASE_URL = 'http://localhost:8000';

// Global state
let materials = [];
let fitUps = [];
let finalInspections = [];
let ndtRequests = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAllData();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Tab change events
    const tabLinks = document.querySelectorAll('.nav-link');
    tabLinks.forEach(link => {
        link.addEventListener('click', function() {
            const target = this.getAttribute('href').substring(1);
            if (target === 'materials') {
                loadMaterials();
            } else if (target === 'fitup') {
                loadFitUps();
            } else if (target === 'final') {
                loadFinalInspections();
            } else if (target === 'ndt') {
                loadNDTRequests();
            }
        });
    });
}

// Load all data
async function loadAllData() {
    try {
        await Promise.all([
            loadMaterials(),
            loadFitUps(),
            loadFinalInspections(),
            loadNDTRequests()
        ]);
        updateDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading data. Please check if the backend server is running.');
    }
}

// Load materials
async function loadMaterials() {
    try {
        const response = await fetch(`${API_BASE_URL}/material_inspections/`);
        if (!response.ok) throw new Error('Failed to fetch materials');
        
        materials = await response.json();
        renderMaterialsTable();
        document.getElementById('material-count').textContent = materials.length;
    } catch (error) {
        console.error('Error loading materials:', error);
    }
}

// Load fit up inspections
async function loadFitUps() {
    try {
        const response = await fetch(`${API_BASE_URL}/fit_up_inspections/`);
        if (!response.ok) throw new Error('Failed to fetch fit up inspections');
        
        fitUps = await response.json();
        renderFitUpsTable();
        document.getElementById('fitup-count').textContent = fitUps.length;
    } catch (error) {
        console.error('Error loading fit up inspections:', error);
    }
}

// Load final inspections
async function loadFinalInspections() {
    try {
        const response = await fetch(`${API_BASE_URL}/final_inspections/`);
        if (!response.ok) throw new Error('Failed to fetch final inspections');
        
        finalInspections = await response.json();
        renderFinalInspectionsTable();
        document.getElementById('final-count').textContent = finalInspections.length;
    } catch (error) {
        console.error('Error loading final inspections:', error);
    }
}

// Load NDT requests
async function loadNDTRequests() {
    try {
        const response = await fetch(`${API_BASE_URL}/ndt_requests/`);
        if (!response.ok) throw new Error('Failed to fetch NDT requests');
        
        ndtRequests = await response.json();
        renderNDTRequestsTable();
        document.getElementById('ndt-count').textContent = ndtRequests.length;
    } catch (error) {
        console.error('Error loading NDT requests:', error);
    }
}

// Update dashboard counts
function updateDashboard() {
    document.getElementById('material-count').textContent = materials.length;
    document.getElementById('fitup-count').textContent = fitUps.length;
    document.getElementById('final-count').textContent = finalInspections.length;
    document.getElementById('ndt-count').textContent = ndtRequests.length;
}

// Render materials table
function renderMaterialsTable() {
    const tbody = document.getElementById('materials-table-body');
    tbody.innerHTML = '';
    
    materials.forEach(material => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${material.id}</td>
            <td>${material.type_of_material}</td>
            <td>${material.material_grade}</td>
            <td>${material.thickness} mm</td>
            <td>${material.dia_for_pipe || 'N/A'}</td>
            <td>${material.heat_no}</td>
            <td>${material.mvr_report_no}</td>
            <td>${material.unique_piece_id}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editMaterial(${material.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteMaterial(${material.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Render fit up inspections table
function renderFitUpsTable() {
    const tbody = document.getElementById('fitup-table-body');
    tbody.innerHTML = '';
    
    fitUps.forEach(fitUp => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${fitUp.id}</td>
            <td>${fitUp.drawing_no}</td>
            <td>${fitUp.line_no}</td>
            <td>${fitUp.spool_no}</td>
            <td>${fitUp.joint_no}</td>
            <td>${fitUp.weld_type}</td>
            <td><span class="badge bg-${fitUp.inspection_result === 'PASS' ? 'success' : 'danger'}">${fitUp.inspection_result}</span></td>
            <td>Materials ${fitUp.material1_id} & ${fitUp.material2_id}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editFitUp(${fitUp.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteFitUp(${fitUp.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Render final inspections table
function renderFinalInspectionsTable() {
    const tbody = document.getElementById('final-table-body');
    tbody.innerHTML = '';
    
    finalInspections.forEach(final => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${final.id}</td>
            <td>${final.wps_no}</td>
            <td>${final.welder_no}</td>
            <td>${final.final_report_no}</td>
            <td>${final.ndt_results}</td>
            <td>User ${final.inspector_id}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editFinal(${final.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteFinal(${final.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Render NDT requests table
function renderNDTRequestsTable() {
    const tbody = document.getElementById('ndt-table-body');
    tbody.innerHTML = '';
    
    ndtRequests.forEach(ndt => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${ndt.id}</td>
            <td>${ndt.line_no}</td>
            <td>${ndt.spool_no}</td>
            <td>${ndt.joint_no}</td>
            <td>${ndt.weld_type}</td>
            <td>${ndt.thickness} mm</td>
            <td>${ndt.diameter} inches</td>
            <td>${ndt.rfi_no}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editNDT(${ndt.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteNDT(${ndt.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Show material form modal
function showMaterialForm() {
    const modal = new bootstrap.Modal(document.getElementById('materialModal'));
    document.getElementById('materialForm').reset();
    modal.show();
}

// Submit material form
async function submitMaterialForm() {
    const form = document.getElementById('materialForm');
    const formData = new FormData(form);
    
    const materialData = {
        type_of_material: formData.get('type_of_material'),
        material_grade: formData.get('material_grade'),
        thickness: parseFloat(formData.get('thickness')),
        dia_for_pipe: formData.get('dia_for_pipe') ? parseFloat(formData.get('dia_for_pipe')) : null,
        heat_no: formData.get('heat_no'),
        mvr_report_no: formData.get('mvr_report_no'),
        unique_piece_id: formData.get('unique_piece_id')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/material_inspections/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(materialData)
        });
        
        if (!response.ok) throw new Error('Failed to create material');
        
        const newMaterial = await response.json();
        materials.push(newMaterial);
        renderMaterialsTable();
        updateDashboard();
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('materialModal'));
        modal.hide();
        
        alert('Material created successfully!');
    } catch (error) {
        console.error('Error creating material:', error);
        alert('Error creating material. Please try again.');
    }
}

// Edit material
async function editMaterial(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/material_inspections/${id}`);
        if (!response.ok) throw new Error('Failed to fetch material');
        
        const material = await response.json();
        
        // Fill the form with existing data
        document.getElementById('materialForm').reset();
        document.querySelector('input[name="type_of_material"]').value = material.type_of_material;
        document.querySelector('input[name="material_grade"]').value = material.material_grade;
        document.querySelector('input[name="thickness"]').value = material.thickness;
        document.querySelector('input[name="dia_for_pipe"]').value = material.dia_for_pipe || '';
        document.querySelector('input[name="heat_no"]').value = material.heat_no;
        document.querySelector('input[name="mvr_report_no"]').value = material.mvr_report_no;
        document.querySelector('input[name="unique_piece_id"]').value = material.unique_piece_id;
        
        // Show modal and set up update handler
        const modal = new bootstrap.Modal(document.getElementById('materialModal'));
        modal.show();
        
        // Change submit button to update
        const submitBtn = document.querySelector('#materialModal .btn-primary');
        submitBtn.textContent = 'Update Material';
        submitBtn.onclick = () => updateMaterial(id);
    } catch (error) {
        console.error('Error loading material for edit:', error);
        alert('Error loading material for editing.');
    }
}

// Update material
async function updateMaterial(id) {
    const form = document.getElementById('materialForm');
    const formData = new FormData(form);
    
    const materialData = {
        type_of_material: formData.get('type_of_material'),
        material_grade: formData.get('material_grade'),
        thickness: parseFloat(formData.get('thickness')),
        dia_for_pipe: formData.get('dia_for_pipe') ? parseFloat(formData.get('dia_for_pipe')) : null,
        heat_no: formData.get('heat_no'),
        mvr_report_no: formData.get('mvr_report_no'),
        unique_piece_id: formData.get('unique_piece_id')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/material_inspections/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(materialData)
        });
        
        if (!response.ok) throw new Error('Failed to update material');
        
        const updatedMaterial = await response.json();
        materials = materials.map(m => m.id === id ? updatedMaterial : m);
        renderMaterialsTable();
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('materialModal'));
        modal.hide();
        
        alert('Material updated successfully!');
    } catch (error) {
        console.error('Error updating material:', error);
        alert('Error updating material. Please try again.');
    }
}

// Delete material
async function deleteMaterial(id) {
    if (!confirm('Are you sure you want to delete this material?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/material_inspections/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete material');
        
        materials = materials.filter(m => m.id !== id);
        renderMaterialsTable();
        updateDashboard();
        
        alert('Material deleted successfully!');
    } catch (error) {
        console.error('Error deleting material:', error);
        alert('Error deleting material. Please try again.');
    }
}

// Edit fit up inspection
async function editFitUp(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/fit_up_inspections/${id}`);
        if (!response.ok) throw new Error('Failed to fetch fit up inspection');
        
        const fitUp = await response.json();
        alert(`Edit fit up inspection ${id} - Data loaded: ${JSON.stringify(fitUp)}`);
        // TODO: Implement fit up edit form
    } catch (error) {
        console.error('Error loading fit up for edit:', error);
        alert('Error loading fit up inspection for editing.');
    }
}

// Edit final inspection
async function editFinal(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/final_inspections/${id}`);
        if (!response.ok) throw new Error('Failed to fetch final inspection');
        
        const final = await response.json();
        alert(`Edit final inspection ${id} - Data loaded: ${JSON.stringify(final)}`);
        // TODO: Implement final edit form
    } catch (error) {
        console.error('Error loading final for edit:', error);
        alert('Error loading final inspection for editing.');
    }
}

// Edit NDT request
async function editNDT(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/ndt_requests/${id}`);
        if (!response.ok) throw new Error('Failed to fetch NDT request');
        
        const ndt = await response.json();
        alert(`Edit NDT request ${id} - Data loaded: ${JSON.stringify(ndt)}`);
        // TODO: Implement NDT edit form
    } catch (error) {
        console.error('Error loading NDT for edit:', error);
        alert('Error loading NDT request for editing.');
    }
}

// Delete fit up inspection
async function deleteFitUp(id) {
    if (!confirm('Are you sure you want to delete this fit up inspection?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/fit_up_inspections/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete fit up inspection');
        
        fitUps = fitUps.filter(f => f.id !== id);
        renderFitUpsTable();
        updateDashboard();
        
        alert('Fit up inspection deleted successfully!');
    } catch (error) {
        console.error('Error deleting fit up inspection:', error);
        alert('Error deleting fit up inspection. Please try again.');
    }
}

// Delete final inspection
async function deleteFinal(id) {
    if (!confirm('Are you sure you want to delete this final inspection?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/final_inspections/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete final inspection');
        
        finalInspections = finalInspections.filter(f => f.id !== id);
        renderFinalInspectionsTable();
        updateDashboard();
        
        alert('Final inspection deleted successfully!');
    } catch (error) {
        console.error('Error deleting final inspection:', error);
        alert('Error deleting final inspection. Please try again.');
    }
}

// Delete NDT request
async function deleteNDT(id) {
    if (!confirm('Are you sure you want to delete this NDT request?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/ndt_requests/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete NDT request');
        
        ndtRequests = ndtRequests.filter(n => n.id !== id);
        renderNDTRequestsTable();
        updateDashboard();
        
        alert('NDT request deleted successfully!');
    } catch (error) {
        console.error('Error deleting NDT request:', error);
        alert('Error deleting NDT request. Please try again.');
    }
}

// Redis integration functions (placeholder)
function cacheData(key, data) {
    // This would integrate with Redis in a real implementation
    localStorage.setItem(key, JSON.stringify(data));
}

function getCachedData(key) {
    // This would integrate with Redis in a real implementation
    const cached = localStorage.getItem(key);
    return cached ? JSON.parse(cached) : null;
}
