class Post {
    constructor(data) {
        this.data = data;
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

    render() {
        return `
<div class="col-sm-12">
    <div class="card card-block card-stretch card-height">
        <div class="card-body">
            <a href="/web/2/${this.data.id}">${this.data.title}</a>
            <div class="mt-3">on blog<div class="btn btn-primary ">on</div>&Tab;<a>edit</a>&Tab;on blog<div class="btn btn-primary">on</div>&Tab;on blog<div class="btn btn-primary">on</div></div>
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