// script.js
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
        });

        // Append the text and button to the email item container
        emailItem.appendChild(emailText);
        emailItem.appendChild(removeButton);

        // Append the email item to the email list
        emailList.appendChild(emailItem);

        // Clear the input field
        emailInput.value = '';
    }
});
