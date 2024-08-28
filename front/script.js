document.addEventListener('DOMContentLoaded', () => {
    const localDeviceButton = document.getElementById('local-device-button');
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');

    localDeviceButton.addEventListener('click', () => {
        uploadContainer.style.display = 'block'; // Show the file input container
        fileInput.click(); // Automatically trigger file input dialog
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            console.log('File chosen:', file.name);
            // Handle the file here (e.g., upload it or process it)
        }
    });
});
