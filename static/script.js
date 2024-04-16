function uploadVideo() {
    const fileInput = document.getElementById('videoInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('video', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        console.log(result); // You can handle the result as needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
