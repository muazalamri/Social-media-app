// Global array to track selected files with their input information
let selectedFiles = [];

// Function to render files in .flist container
function renderFiles() {
    const flist = document.querySelector('.flist');
    flist.innerHTML = '';
    
    selectedFiles.forEach((fileEntry, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'btn d-flex align-items-center justify-content-between mb-2';
        fileDiv.innerHTML = `
            <span>${fileEntry.file.name}</span>
            <button class="btn btn-danger btn-sm delete-btn">&times;</button>
        `;
        
        fileDiv.querySelector('.delete-btn').addEventListener('click', () => {
            selectedFiles.splice(index, 1);
            renderFiles();
        });
        
        flist.appendChild(fileDiv);
    });
}

// Function to handle file input changes
function handleFileInputChange(event) {
    const input = event.target;
    const inputId = input.id;
    const files = Array.from(input.files);

    // Show upload progress spinner
    const progress = document.createElement('div');
    progress.className = 'upload-progress';
    progress.innerHTML = '<div class="spinner-border text-primary"></div>';
    document.body.appendChild(progress);

    // Process files after short delay to show spinner
    setTimeout(() => {
        // Remove previous entries from the same input
        selectedFiles = selectedFiles.filter(entry => entry.inputId !== inputId);
        
        // Add new files to selectedFiles
        files.forEach(file => {
            selectedFiles.push({
                inputId: inputId,
                file: file,
                inputName: input.name
            });
        });
        
        renderFiles();
        document.body.removeChild(progress);
    }, 300);
}

// Attach event listeners to all file inputs
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', handleFileInputChange);
});