document.addEventListener('DOMContentLoaded', function() {
    const contacts = JSON.parse(localStorage.getItem('contacts')) || [];

    const contactsTableBody = document.querySelector('#contactsTable tbody');

    contacts.forEach(contact => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${contact.name}</td>
            <td>${contact.location}</td>
            <td>${contact.contactInformation}</td>
            <td>${contact.email}</td>
            <td><a href="${contact.website}" target="_blank">${contact.website}</a></td>
        `;

        contactsTableBody.appendChild(row);
    });
});