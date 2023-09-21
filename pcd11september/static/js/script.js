$(document).ready(function(){
    $('form input').change(function () {
      $('form p').text(this.files.length + " file(s) selected");
    });
  });

function preview() {
    frame.src=URL.createObjectURL(event.target.files[0]);
}

function uploadFile() {
    const uploadForm = document.getElementById('upload-form');
    uploadForm.submit();
}







