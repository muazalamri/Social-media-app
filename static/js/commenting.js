function commeting(section,elementType, elemntId) {
    const commentBox = document.getElementById("comment-box-"+elemntId);
    const commentInput = document.getElementById("comment-input-"+elemntId);
    let data = {
        elementType: elementType,
        id: id,
        comment: commentInput.value
    };
    fetch("/elementcomment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            commentBox.innerHTML = commentTemplate(response.json())+ commentBox.innerHTML; // Append the new comment to the comment box
            commentInput.value = ""; // Clear the input field
        }
    }).catch(error => {
        console.error("Error:", error);
    });
    
};
function commentTemplate(comment) {
    return `
         <li class="mb-2">
           <div class="d-flex flex-wrap">
             <div class="user-img">
               <img src="${comment.img}" alt="userimg" class="avatar-35 rounded-circle img-fluid">
             </div>
             <div class="comment-data-block ms-3">
               <h6>${comment.name}</h6>
               <p class="mb-0">${comment.text}</p>
               <div class="d-flex flex-wrap align-items-center comment-activity">
                 <a href="javascript:void(0);">like</a>
                 <a href="javascript:void(0);">reply</a>
                 <a href="javascript:void(0);">translate</a>
                 <span>${comment.time}</span>
               </div>
             </div>
           </div>
         </li>`;
};
function setcommenting(){
    let commentBoxs = document.getElementsByClassName('commentingbox');
    //test if it has altribute functioned
    for (let i = 0; i < commentBoxs.length; i++) {
        let commentBox = commentBoxs[i];
        let elemntId = commentBox.getAttribute('id').split('-')[2];
        let elementType = commentBox.getAttribute('id').split('-')[1];
        let section = commentBox.getAttribute('id').split('-')[3];
        let commentInput = document.getElementById("comment-input-"+elemntId);
        commentInput.addEventListener('click', function() {
            commeting(section,elementType,elemntId);
        });
    }
};
setcommenting();
setliking();