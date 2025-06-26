class Post {
    constructor(data) {
        this.data = data;
    }

    flowing() {
        return this.data.flowed ? 'unflow': 'flow';
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
        return this.data.withmed ? `<div class="user-post">${this.mediaFromLinks()}</div>`: '';
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
        <h5 class="mb-0 d-inline-block">${this.data.sender}</h5>
        <p class="mb-0 d-inline-block">${this.data.title}</p>
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
        <p class="mb-0">See fewer posts like this.</p>
        </div>
        </div>
        </a>
        <a class="dropdown-item p-3" href="#">
        <div class="d-flex align-items-top">
        <i class="ri-user-unfollow-line h4"></i>
        <div class="data ms-2">
        <h6>${this.flowing()}</h6>
        <p class="mb-0">Stop seeing posts but stay friends.</p>
        </div>
        </div>
        </a>
        <a class="dropdown-item p-3" href="#">
        <div class="d-flex align-items-top">
        <i class="ri-notification-line h4"></i>
        <div class="data ms-2">
        <h6>Notifications</h6>
        <p class="mb-0">Turn on notifications for this post</p>
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
        <a class="ms-2 me-2 " id="likebu-${this.data.id}${this.data.section}" href="javascript:likit(${this.data.id},${this.data.section},0);" data-bs-toggle="tooltip" data-bs-placement="top" title="Like">
        <li class="far fa-thumbs-up"></li>
        </a>
        </div>
        <div class="total-like-block ms-2 me-3">
        <div class="dropdown">
        <span class="dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="button">
        <span id="like-${this.data.id}${this.data.section}">${this.data.Likes}</span> Likes
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
        <span id="num_com-${this.data.id}${this.data.section}">${this.data.num_com}</span> Comment
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
        <ul class="post-comments list-inline p-0 m-0" id='coms-${this.data.id}${this.data.section}'>
        ${this.generateComments()}
        </ul>
        <form class="comment-text d-flex align-items-center mt-3" id='comInput-${this.data.id}${this.data.section}' action="javascript:add_comment(${this.data.id},${this.data.section});">
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
        fetch(`/load`)
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
function add_comment(postId, sec) {
    let com_erea = document.getElementById('coms-'+postId+sec);
    let form = document.getElementById('comInput-'+postId+sec);
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
    .then(comment=> {
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
        </li>`+com_erea.innerHTML;
    })
    .catch(error => {
        console.error('Error:', error);
    });
    let num_com = document.getElementById('num_com-'+postId+sec);
    num_com.innerText = Number(num_com.innerText)+1;
    form.commentText.value = '';
}
document.addEventListener('DOMContentLoaded', () => {
    new Feed('content-page');
});

function likit(postId, sec, interaction) {
    fetch(`/liking?post=${postId}&interaction=${interaction}`)
    .then(response => response.json())
    .then(result => {
        if (result.status == 'ok') {
            let likes = document.getElementById('like-'+postId+sec);
            likes.innerText = Number(likes.innerText)+1; //="like-${this.data.id}${this.data.section}"
            let likebu = document.getElementById('likebu-'+postId+sec);
            likebu.innerHTML = '<li class="fas fa-thumbs-up"></li>';
        };
    })
    .catch(error=> {
        console.log(error)
    })
}