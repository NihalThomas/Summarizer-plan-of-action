const tenantId = 'your-tenant-id';
const clientId = 'your-client-id';
const clientSecret = 'your-client-secret';
const siteId = 'your-site-id';
const driveId = 'your-drive-id';

// Function to get the access token
async function getAccessToken() {
    const tokenUrl = `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`;
    const scope = 'https://graph.microsoft.com/.default';

    const tokenData = new URLSearchParams();
    tokenData.append('grant_type', 'client_credentials');
    tokenData.append('client_id', clientId);
    tokenData.append('client_secret', clientSecret);
    tokenData.append('scope', scope);

    try {
        const response = await fetch(tokenUrl, {
            method: 'POST',
            body: tokenData
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch access token: ${response.statusText}`);
        }

        const data = await response.json();
        return data.access_token;

    } catch (error) {
        console.error("Error fetching access token:", error);
        alert("Failed to retrieve access token. Check console for details.");
    }
}

// Function to list items in the "Recordings" folder
async function listItemsInFolder(token) {
    const headers = new Headers({
        'Authorization': `Bearer ${token}`
    });
    const listItemsEndpoint = `https://graph.microsoft.com/v1.0/sites/${siteId}/drives/${driveId}/root:/Recordings:/children`;

    try {
        const response = await fetch(listItemsEndpoint, { headers });

        if (!response.ok) {
            throw new Error(`Failed to list items: ${response.statusText}`);
        }

        const data = await response.json();
        return data.value || [];

    } catch (error) {
        console.error("Error listing items:", error);
        alert("Failed to list files. Check console for details.");
    }
}

// Fetch the list of files when the page loads
document.addEventListener("DOMContentLoaded", async function () {
    const token = await getAccessToken();

    if (!token) return; // Exit if token retrieval failed

    const items = await listItemsInFolder(token);

    const dropdown = document.getElementById('fileDropdown');
    dropdown.innerHTML = ''; // Clear loading message

    if (items && items.length > 0) {
        items.forEach(file => {
            const option = document.createElement('option');
            option.value = file.id;
            option.textContent = file.name;
            dropdown.appendChild(option);
        });
    } else {
        const option = document.createElement('option');
        option.textContent = 'No files found';
        dropdown.appendChild(option);
    }
});

// Function to download the selected file
async function downloadFile() {
    const dropdown = document.getElementById('fileDropdown');
    const fileId = dropdown.value;
    const fileName = dropdown.options[dropdown.selectedIndex].text;

    if (!fileId || fileId === 'No files found') {
        alert('Please select a valid file to download.');
        return;
    }

    const token = await getAccessToken();
    const headers = new Headers({
        'Authorization': `Bearer ${token}`
    });
    const fileContentEndpoint = `https://graph.microsoft.com/v1.0/sites/${siteId}/drives/${driveId}/items/${fileId}/content`;

    try {
        const response = await fetch(fileContentEndpoint, { headers });

        if (!response.ok) {
            throw new Error(`Failed to download file: ${response.statusText}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error("Error downloading file:", error);
        alert("Failed to download file. Check console for details.");
    }
}