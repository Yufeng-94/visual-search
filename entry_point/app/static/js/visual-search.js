
function init () {
    setupEventListeners();
}

function setupEventListeners () {
    // Drop zone
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');

    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault(); 
        dropZone.style.borderColor = '#007bff';
    });
    dropZone.addEventListener('dragleave', (e) => {
        dropZone.style.borderColor = '#ccc';
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';

        const files = e.dataTransfer.files
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Control button
    const closeBtn = document.getElementById('close-btn');
    closeBtn.addEventListener('click', () => returnMain());
}

function handleFileUpload (file) {
    if (file.name.toLowerCase().endsWith('.jpg') || file.name.toLowerCase().endsWith('.jpeg')) {
        // Show loading div
        const loading = document.getElementById('loading');
        loading.style.display = 'flex';

        // Put upload file to upload-img div
        displayUploadedImage(file);

        // fetch file into a request
        const formData = new FormData();
        formData.append('file', file);


        fetch('/api/search', {method: 'POST', body: formData})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                displaySearchResults(data);
            }
        })
        .catch(error => alert('Error uploading file: ' + error))
        .finally(() => {loading.style.display='none';})

    } else {
        alert('Please upload a .jpg or .jpeg file');
    }
}

function displayUploadedImage(file) {
    // Fetch uploaded img
    const uploadImg = document.getElementById('upload-img');
    // Clear previous content
    uploadImg.innerHTML = '';

    const imgElement = document.createElement('img');
    imgElement.src = URL.createObjectURL(file);
    imgElement.alt = 'Uploaded image';

    uploadImg.appendChild(imgElement);
}

function displaySearchResults(data) {

    // Fetch searched img
    const resultsImg = document.getElementById('results-img');
    // Clear existing content
    resultsImg.innerHTML = '';

    data.similar_images.forEach(imgMeta => {
        const imgElement = document.createElement('img');
        imgElement.src = imgMeta.image_url;
        resultsImg.appendChild(imgElement);
    });

    // Show results page
    const resultsPage = document.getElementById('results-page');
    resultsPage.style.display = 'flex';
}

function returnMain () {
    const resultsPage = document.getElementById('results-page');
    resultsPage.style.display = 'none';
}

init();