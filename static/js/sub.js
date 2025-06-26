let mypost = document.getElementById('createp');
let myform = new FormData(mypost);
let with_cheak=false;
function triggerFileInput() {
    document.getElementById('fileInput').click();
}
function triggerZIPInput() {
    document.getElementById('zipInput').click();
}
function triggerModelInput() {
    document.getElementById('modelInput').click();
}
function triggerGifInput() {
    document.getElementById('gifInput').click();
}

function add_cheak(){
    mypost = document.getElementById('createp');
    myform = new FormData(mypost);
    let place = document.getElementById('text_place');
    if(!with_cheak){
        place.innerHTML=
`               <div class="user-img" >
                                             <img src="/static/images/user/1.jpg" alt="userimg" class="avatar-60 rounded-circle img-fluid">
                                          </div>
                                             <input type="text" class="form-control rounded" placeholder="Write something here..." value="${myform.get('T')}" style="border:none;" id="T" name="T">
                                             <input type="checkbox">`;
        with_cheak=true;
        }
    else{place.innerHTML=
        `               <div class="user-img" >
                                                     <img src="/static/images/user/1.jpg" alt="userimg" class="avatar-60 rounded-circle img-fluid">
                                                  </div>
                                                     <input type="text" class="form-control rounded" placeholder="Write something here..." value="${myform.get('T')}"style="border:none;" id="T" name="T">`;
        with_cheak=false;
        
    }
}
function fet(event) {
    mypost = document.getElementById('createp');
    myform = new FormData(mypost);
    console.log('fet runned');
    console.log(myform.get('T'));

    fetch('/adds', {
        method: 'POST',
        body: myform
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false; // Prevent the form from submitting the traditional way
}