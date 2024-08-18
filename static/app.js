// static/app.js

document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with class 'formSubmit'
    const formSubmits = document.querySelectorAll('.formSubmit');

    // Iterate over each element with the 'formSubmit' class
    formSubmits.forEach(function(element) {
        // Add a click event listener to each element
        element.addEventListener('click', function() {
            // Get the values from data attributes
            const brand = element.getAttribute('data-brand');
            const name = element.getAttribute('data-name');

            // Find the closest form element related to the clicked 'formSubmit'
            const form = element.closest('li').querySelector('.descForm');

            // Ensure the form and input fields are found
            if (form) {
                // Set the hidden input fields with the data values
                const nameInput = form.querySelector('.name');
                const brandInput = form.querySelector('.brand')

                if (nameInput) nameInput.value = name;
                if (brandInput) brandInput.value = brand;

                // Submit the form
                form.submit();
            }
        });
    });

    const formLinkSubmits = document.querySelectorAll('.formLinkSubmit');

    // Iterate over each element with the 'formSubmit' class
    formLinkSubmits.forEach(function(element) {
        // Add a click event listener to each element
        element.addEventListener('click', function() {
            // Get the values from data attributes
            const url = element.getAttribute('data-url')

            // Find the closest form element related to the clicked 'formSubmit'
            const form = element.closest('li').querySelector('.purchaseForm');

            // Ensure the form and input fields are found
            if (form) {
                // Set the hidden input fields with the data values
                const urlInput = form.querySelector(".url")

                if (urlInput) urlInput.value = url;

                // Submit the form
                form.submit();
            }
        });
    });
});
