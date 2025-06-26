function comen(){
    comer=[{'img':'/static/images/user/1.jpg','text':'good reading','time':'3 days ago','name':'listner'},{'img':'/static/images/user/1.jpg','text':'good reading','time':'3 days ago','name':'listner'},{'img':'/static/images/user/1.jpg','text':'good reading','time':'3 days ago','name':'listner'},{'img':'/static/images/user/1.jpg','text':'good reading','time':'3 days ago','name':'listner'}];
    place=document.getElementById('comPlace');
    let data ='';
    comer.forEach(element=>{
        data+=`<li class="mb-2">
       <div class="d-flex flex-wrap">
          <div class="user-img">
             <img src="${element['img']}" alt="userimg" class="avatar-35 rounded-circle img-fluid">
          </div>
          <div class="comment-data-block ms-3">
             <h6>${element['name']}</h6>
             <p class="mb-0">${element['text']}</p>
             <div class="d-flex flex-wrap align-items-center comment-activity">
                <a href="javascript:void();">like</a>
                <a href="javascript:void();">reply</a>
                <a href="javascript:void();">translate</a>
                <span> ${element['time']} </span>
             </div>
          </div>
       </div>
    </li>`});
    place.innerHTML=data;
}
comen();