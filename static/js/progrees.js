document.getElementById('uploadButton').addEventListener('click', function() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append('file', file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/uploading', true);

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            var percentComplete = (event.loaded / event.total) * 100;
            document.getElementById('progress').style.width = percentComplete + '%';
        }
    };

    xhr.onload = function() {
        if (xhr.status == 200) {
            alert('File uploaded successfully!');
        } else {
            alert('File upload failed!');
        }
    };

    xhr.send(formData);
});
document.getElementById('fileInput').addEventListener('input',function(){
    //document.getElementById('uploadButton').click
    console.log('input')
})