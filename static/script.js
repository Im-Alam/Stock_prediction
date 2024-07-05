const fileInput = document.getElementById("fileInput");
const dragZone = document.querySelector('.dragZone');
const uploadButton = document.getElementById('upload');
const info = document.getElementById('info');
const analyse = document.getElementById('analyse');
const report = document.getElementById('report');



fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file) {
        info.textContent = `Selected file: ${file.name}`;
    }else{
        info.textContent = `Drag file here`;
    }
});

// Trigger file selection dialog on clicking the dragZone
dragZone.addEventListener('click', () => {
    fileInput.click();
});

dragZone.addEventListener('dragover', (event) => {
    event.preventDefault();
});

dragZone.addEventListener('dragleave', (event) => {
    event.preventDefault();
});

dragZone.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;

    // Check if a file is dropped
    if (files.length > 0) {
        // Assign dropped file(s) to the input element
        fileInput.files = files;

        // Trigger the `change` event on the `fileInput` to mimic manual selection
        fileInput.dispatchEvent(new Event('change'));
    }
});

uploadButton.addEventListener('click', (event) => {
    event.preventDefault();

    // Check if a file is selected
    if (!fileInput.files.length) {
        report.textContent = `Select a file to upload!`;
        report.style.color='red';
        analyse.style.display = 'none';
        return;
    }

    // Prepare the upload request (similar to previous approach)
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Make a POST request to your Flask route
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('File uploaded successfully!');
            report.textContent = `File uploaded sucessfully!`;
            report.style.color='green';
            analyse.style.display = 'unset';
        } else {
            console.error('Error uploading file:', response.statusText);
            report.textContent = `${response.statusText}!`;
            report.style.color='red';
            analyse.style.display = 'none';
            // Handle upload errors on the client-side (optional)
        }
    })
    .catch(error => {
        console.error('An unexpected error occurred during upload:', error);
        report.textContent = 'An unexpected error occurred during upload!!';
        analyse.style.display = 'none';
    });
    
});

analyse.addEventListener('click', (event) => {
    event.preventDefault();

    // Check if a file was uploaded successfully
    if (!report.textContent.includes('sucessfully')) {
        report.textContent = 'Please upload a file first!';
        report.style.color = 'red';
        return;
    }
    const file = fileInput.files[0];
    const url = '/IPO_page'//`/analysis/${encodeURIComponent(file.name)}`;
    window.location.href = url;


});