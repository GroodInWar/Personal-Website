document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('submitForm');

    if (form) {
        form.addEventListener('submit', function(event) {
            if (this.checkValidity()) {
                event.preventDefault();
                
                const contacts = JSON.parse(localStorage.getItem('contacts')) || [];

                const newContact = {
                    name: document.getElementById('name').value,
                    location: document.getElementById('location').value,
                    contactInformation: document.getElementById('contactInformation').value,
                    email: document.getElementById('email').value,
                    website: document.getElementById('website').value,
                };

                contacts.push(newContact);
                localStorage.setItem('contacts', JSON.stringify(contacts));

                window.location.href = 'added-contacts.html';
            }
        });
    } else {
        console.error('Form element not found.');
    }
});

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 44.9727, lng: -93.23540000000003 },
    zoom: 14
  });
}