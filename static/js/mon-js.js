class Post {
  constructor(data) {
    this.data = data;
  }

  flowing() {
    return this.data.flowed ? 'unflow' : 'flow';
  }

  mediaFromLinks() {
    const links = this.data.media || [];
    if (links.length === 1) {
      return `
         <div class="d-grid grid-rows-2 grid-flow-col gap-3">
           <div class="row-span-2 row-span-md-1">
             <img src="/static/images/page-img/p2.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
         </div>`;
    } else if (links.length === 2) {
      return `
         <div class="d-grid grid-rows-2 grid-flow-col gap-3">
           <div class="row-span-2 row-span-md-1">
             <img src="/static/images/page-img/p2.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
           <div class="row-span-2 row-span-md-1">
             <img src="/static/images/page-img/p2.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
         </div>`;
    } else if (links.length > 2) {
      return `
         <div class="d-grid grid-rows-2 grid-flow-col gap-3">
           <div class="row-span-2 row-span-md-1">
             <img src="/static/images/page-img/p2.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
           <div class="row-span-1">
             <img src="/static/images/page-img/p1.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
           <div class="row-span-1">
             <img src="/static/images/page-img/p3.jpg" alt="post-image" class="img-fluid rounded w-100">
           </div>
         </div>`;
    }
    return '';
  }

  media() {
    return this.data.withmed ? `<div class="user-post">${this.mediaFromLinks()}</div>` : '';
  }

  generateCommenter() {
    let html = '';
    if (this.data.num_com > 0 && this.data.comer) {
      this.data.comer.forEach(comment => {
        html += `<a class="dropdown-item" href="#">${comment.name}</a>`;
      });
      if (this.data.com_other) {
        html += `<a class="dropdown-item" href="#">Other</a>`;
      }
    }
    return html;
  }

  generateLiker() {
    let html = '';
    if (this.data.Likes > 0 && this.data.liker) {
      this.data.liker.forEach(likerName => {
        html += `<a class="dropdown-item" href="#">${likerName}</a>`;
      });
      if (this.data.other) {
        html += `<a class="dropdown-item" href="#">Other</a>`;
      }
    }
    return html;
  }

  generateComments() {
    let html = '';
    if (this.data.comer) {
      this.data.comer.forEach(comment => {
        html += `
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
      });
    }
    return html;
  }

  render() {
    return `
       <div class="col-sm-12">
         <div class="card card-block card-stretch card-height">
           <div class="card-body">
             <div class="user-post-data">
               <div class="d-flex justify-content-between">
                 <div class="me-3">
                   <img class="rounded-circle img-fluid" src="${this.data.senderimg}" alt="">
                 </div>
                 <div class="w-100">
                   <div class="d-flex justify-content-between">
                     <div>
                       <h5 class="mb-0 d-inline-block"><a href="/profile/${this.data.senderid}">${this.data.sender}</a></h5>
                       <p class="mb-0 d-inline-block">${this.data.type}</p>
                       <p class="mb-0 text-primary">${this.data.time}</p>
                     </div>
                     <div class="card-post-toolbar">
                       <div class="dropdown">
                         <span class="dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="button">
                           <i class="ri-more-fill"></i>
                         </span>
                         <div class="dropdown-menu m-0 p-0">
                           <a class="dropdown-item p-3" href="#">
                             <div class="d-flex align-items-top">
                               <i class="ri-save-line h4"></i>
                               <div class="data ms-2">
                                 <h6>Save Post</h6>
                                 <p class="mb-0">Add this to your saved items</p>
                               </div>
                             </div>
                           </a>
                           <a class="dropdown-item p-3" href="#">
                             <div class="d-flex align-items-top">
                               <i class="ri-close-circle-line h4"></i>
                               <div class="data ms-2">
                                 <h6>Hide Post</h6>
                                 <p class="mb-0">MONEYTIZE.</p>
                               </div>
                             </div>
                           </a>
                           <a class="dropdown-item p-3" href="#">
                             <div class="d-flex align-items-top">
                               <i class="ri-user-unfollow-line h4"></i>
                               <div class="data ms-2">
                                 <p class="mb-0">EDIT.</p>
                               </div>
                             </div>
                           </a>
                           <a class="dropdown-item p-3" href="#">
                             <div class="d-flex align-items-top">
                               <i class="ri-notification-line h4"></i>
                               <div class="data ms-2">
                                 <h6>Notifications</h6>
                                 <p class="mb-0">CONTROL VISABLITY</p>
                               </div>
                             </div>
                           </a>
                         </div>
                       </div>
                     </div>
                   </div>
                 </div>
               </div>
             </div>
             <div class="mt-3">
               <p>${this.data.text}</p>
             </div>
             ${this.media()}
           </div>
           <div class="comment-area mt-3">
             <div class="d-flex justify-content-between align-items-center flex-wrap">
               <div class="like-block position-relative d-flex align-items-center">
                 <div class="d-flex align-items-center">
                   <div class="like-data">
                     <div class="dropdown">
                       <span class="dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="button">
                         <img src="/static/images/icon/01.png" class="img-fluid" alt="">
                       </span>
                       <div class="dropdown-menu py-2">
                         <a class="ms-2 me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Like">
                           <img src="/static/images/icon/01.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Love">
                           <img src="/static/images/icon/02.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Happy">
                           <img src="/static/images/icon/03.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="HaHa">
                           <img src="/static/images/icon/04.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Think">
                           <img src="/static/images/icon/05.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Sade">
                           <img src="/static/images/icon/06.png" class="img-fluid" alt="">
                         </a>
                         <a class="me-2" href="javascript:void(0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Lovely">
                           <img src="/static/images/icon/07.png" class="img-fluid" alt="">
                         </a>
                       </div>
                     </div>
                   </div>
                   <div class="total-like-block ms-2 me-3">
                     <div class="dropdown">
                       <span class="dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="button">
                         <span>${this.data.Likes}</span> Likes
                       </span>
                       <div class="dropdown-menu">
                         ${this.generateLiker()}
                       </div>
                     </div>
                   </div>
                 </div>
                 <div class="total-comment-block">
                   <div class="dropdown">
                     <span class="dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="button">
                       ${this.data.num_com} Comment
                     </span>
                     <div class="dropdown-menu">
                       ${this.generateCommenter()}
                     </div>
                   </div>
                 </div>
               </div>
               <div class="share-block d-flex align-items-center feather-icon mt-2 mt-md-0">
                 <a href="javascript:void(0);" data-bs-toggle="offcanvas" data-bs-target="#share-btn" aria-controls="share-btn">
                   <i class="ri-share-line"></i>
                   <span class="ms-1">${this.data.num_share} Share</span>
                 </a>
               </div>
             </div>
             <hr>
             <ul class="post-comments list-inline p-0 m-0" id='coms-${this.data.id}'>
               ${this.generateComments()}
             </ul>
             <form class="comment-text d-flex align-items-center mt-3" id='comInput-${this.data.id}' action="javascript:add_comment(${this.data.id});">
               <input type="text" name='commentText' class="form-control rounded" placeholder="Enter Your Comment" required>
               <div class="comment-attagement d-flex">
                 <a href="javascript:void(0);"><i class="ri-link me-3"></i></a>
                 <a href="javascript:void(0);"><i class="ri-user-smile-line me-3"></i></a>
                 <a href="javascript:void(0);"><i class="ri-camera-line me-3"></i></a>
               </div>
             </form>
           </div>
         </div>
       </div>`;
  }
}

class Feed {
  constructor(contentPageId) {
    this.contentPage = document.getElementById(contentPageId);
    this.isLoading = false;
    this.page = 1;
    this.initScrollListener();
    this.loadMoreContent();
  }

  initScrollListener() {
    this.contentPage.addEventListener('scroll', () => {
      if (this.contentPage.scrollTop + this.contentPage.clientHeight >= this.contentPage.scrollHeight - 1000) {
        this.loadMoreContent();
      }
    });
  }

  loadMoreContent() {
    if (this.isLoading) return;
    this.isLoading = true;
    fetch(`/userpost/1?page=${this.page}`)
      .then(response => response.json())
      .then(response => {
        const fragment = document.createDocumentFragment();
        response.data.forEach(element => {
          const post = new Post(element);
          const wrapper = document.createElement('div');
          wrapper.innerHTML = post.render();
          fragment.appendChild(wrapper.firstElementChild);
        });
        this.contentPage.appendChild(fragment);
        this.page++;
        this.isLoading = false;
      })
      .catch(error => {
        console.error(`Error: ${error.message}`);
        this.isLoading = false;
      });
  }
}
function add_comment(postId) {
  let com_erea = document.getElementById('coms-' + postId);
  let form = document.getElementById('comInput-' + postId);
  let data = new FormData(form);
  data.append('id', postId);
  fetch('/commentPost', {
    method: 'POST',
    body: data
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(comment => {
      com_erea.innerHTML = `
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
         </li>`+ com_erea.innerHTML;
    })
    .catch(error => {
      console.error('Error:', error);
    });
  this.page += 1;
  form.commentText.value = '';
}
document.addEventListener('DOMContentLoaded', () => {
  new Feed('content-page');
});