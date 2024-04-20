// function uploadVideo() {
//     const fileInput = document.getElementById('videoInput');
//     const file = fileInput.files[0];

//     const formData = new FormData();
//     formData.append('video', file);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.text())
//     .then(result => {
//         console.log(result); // You can handle the result as needed
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }


function is_valid_email(email) {
    // Regular expression pattern for a valid email address
    var pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Check if the email address matches the pattern
    if (pattern.test(email)) {
        return true;
    } else {
        return false;
    }
}

document.getElementById('upload-btn').addEventListener('click', function(event) {
    event.preventDefault();

    // Get the email address and validate it
    var email = document.getElementById('email').value;
    if (!is_valid_email(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    // Get the file input element and the selected file
    var fileInput = document.getElementById('file-upload');
    var file = fileInput.files[0];

    // Create a FormData object and add the file and email address to it
    var formData = new FormData();
    formData.append('video', file);
    formData.append('email', email);

    // Send a POST request to the /process_video endpoint with the FormData object
    fetch('/process_video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
