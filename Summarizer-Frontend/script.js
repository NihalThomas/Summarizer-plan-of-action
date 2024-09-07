var temp=false;
var summ,poa;
const localDeviceButton = document.getElementById('local-device-button');
const uploadContainer = document.getElementById('upload-container');
const fileInput = document.getElementById('file-input');
var elist=new Array();

const tenantId = 'your-tenant-id';
const clientId = 'your-client-id';
const clientSecret = 'your-client-secret';
const siteId = 'your-site-id';
const driveId = 'your-drive-id';


document.getElementById('teamsButton').addEventListener('click', function() {
    temp=!temp;
    document.getElementById('MSTeamcontainer').style.display = 'block';
    document.getElementById('loaderContainer').style.display = 'none';
    teamLoader();
});

localDeviceButton.addEventListener('click', () => {
    uploadContainer.style.display = 'block';
    document.getElementById('MSTeamcontainer').style.display = 'none';
    fileInput.click(); 
});


document.getElementById('file-input').addEventListener('change', function() {
    document.getElementById('local-device-button').disabled = true;
    document.getElementById('teamsButton').disabled = true;
    document.getElementById('loaderContainer').style.display = 'flex';
    elist.length = 0;
    const file = event.target.files[0];
    if (file) {
        console.log('File chosen:', file.name);
        processVideo(file);
    }
    emailList.innerHTML = '';
});

async function teamLoader(){
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
}


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

async function downloadFile() {
    const dropdown = document.getElementById('fileDropdown');
    const fileId = dropdown.value;
    
    if (!fileId || fileId === 'No files found') {
        alert('Please select a valid file to download.');
        return;
    }
    document.getElementById('MSTeamcontainer').style.display = 'none';
    document.getElementById('loaderContainer').style.display = 'flex';
    const token = await getAccessToken();
    
    
    fetch('http://127.0.0.1:5000/one-drive', {
    method: 'POST', 
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ FileId: fileId,SiteId:siteId,DriveId:driveId,Token:token })
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message === "File processed successfully") {
            summ=data.Summary;
            poa=data.POA;
            
            
            document.getElementById('card-summary').innerHTML=data.Summary;
            document.getElementById('card-poa').innerHTML=data.POA.replace(/\n/g, "<br>");
            document.getElementById('Msg-C').style.display='flex';
        }
        else{
            alert(data.message);
        }
    })
    .catch(error => {
        alert("Error"+error);
    });
    document.getElementById('loaderContainer').style.display = 'none';
}


function processVideo(VideoFile){
    const formData = new FormData();
    formData.append('file', VideoFile);
    fetch('http://127.0.0.1:5000/localsystem', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        if (data && data.message === "File processed successfully") {
            summ=data.Summary;
            poa=data.POA;
            document.getElementById('card-summary').innerHTML=data.Summary;
            document.getElementById('card-poa').innerHTML=data.POA.replace(/\n/g, "<br>");
            document.getElementById('Msg-C').style.display='flex';
        }
        else{
            alert(data.message);
        }
    })
    .catch(error => {
        alert("Error"+error);
    });
    document.getElementById('loaderContainer').style.display = 'none';
    document.getElementById('local-device-button').disabled = false;
    document.getElementById('teamsButton').disabled = false;
}

function sntmail(){
    if (elist.length != 0){
        fetch('http://127.0.0.1:5000/sentmail', {
        method: 'POST', 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: elist,Summary:summ,POA:poa })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.message === "Email sent successfully") {
                alert(data.message);
                document.getElementById('Msg-C').style.display='none';
                document.getElementById('local-device-button').disabled = false;
                document.getElementById('teamsButton').disabled = false;
            }
            else{
                alert(data.message);
            }
        })
        .catch(error => {
            alert("Error"+error);
        });
    }
    else{
       alert("Add Email Recipients");
    }
}




document.getElementById('emailForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const emailInput = document.getElementById('emailInput');
    const email = emailInput.value.trim();

    if (email) {
        const emailList = document.getElementById('emailList');

        // Create a container for the email item
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';

        // Create a text element for the email
        const emailText = document.createElement('span');
        emailText.textContent = email;

        // Create a remove button
        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.className = 'remove-button';

        // Add event listener to remove button
        removeButton.addEventListener('click', function() {
            emailList.removeChild(emailItem);
            let index = elist.indexOf(email);
            if (index !== -1) {
                elist.splice(index, 1); 
            }
            console.log(elist);
        });

        // Append the text and button to the email item container
        emailItem.appendChild(emailText);
        emailItem.appendChild(removeButton);

        // Append the email item to the email list
        emailList.appendChild(emailItem);
        elist.push(email)
        // Clear the input field
        emailInput.value = '';
    }
});




