document.addEventListener('DOMContentLoaded', () => {
    const contentGrid = document.getElementById('content-grid'); // Updated to match the new ID
    let isLoading = false;
    let page = 2; // Start from page 2 since the server-side template renders page 1

    const loadMoreContent = () => {
        if (isLoading) return;
        isLoading = true;
        console.log('Loading more content...');
        
        fetch(`/load_groups?page=${page}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Data loaded:', data);
                if (data.length === 0) {
                    console.log('No more data to load.');
                    isLoading = false;
                    return;
                }
                data.forEach(element => {
                    contentGrid.innerHTML += Gtemplater(element);
                });
                page++; // Increment page after successful data load
                isLoading = false;
            })
            .catch(error => {
                console.error('Error loading groups:', error);
                isLoading = false;
            });
    };

    contentGrid.addEventListener('scroll', () => {
        if (contentGrid.scrollTop + contentGrid.clientHeight >= contentGrid.scrollHeight - 100) {
            loadMoreContent();
        }
    });

    function Gtemplater(group) {
        const members = group['mebs']
            .map(user => `<a href="/profile/${user.id}" class="iq-media">
                            <img class="img-fluid avatar-40 rounded-circle" src="/static/images/user/${user.id}.jpg" alt="">
                        </a>`)
            .join('');
        return `
            <div class="card mb-0">
                <div class="top-bg-image">
                    <img src="${group['backImg']}" class="img-fluid w-100" alt="group-bg">
                </div>
                <div class="card-body text-center">
                    <div class="group-icon">
                        <img src="${group['img']}" alt="profile-img" class="rounded-circle img-fluid avatar-120">
                    </div>
                    <div class="group-info pt-3 pb-3">
                        <h4><a href="/group-detail/${group['name']}">${group['name']}</a></h4>
                        <p>${group['disc']}</p>
                    </div>
                    <div class="group-details d-inline-block pb-3">
                        <ul class="d-flex align-items-center justify-content-between list-inline m-0 p-0">
                            <li class="pe-3 ps-3">
                                <p class="mb-0">Post</p>
                                <h6>${group['posts']}</h6>
                            </li>
                            <li class="pe-3 ps-3">
                                <p class="mb-0">Member</p>
                                <h6>${group['member']}</h6>
                            </li>
                            <li class="pe-3 ps-3">
                                <p class="mb-0">Visit</p>
                                <h6>${group['visit']}</h6>
                            </li>
                        </ul>
                    </div>
                    <div class="group-member mb-3">
                        <div class="iq-media-group">
                            ${members}
                        </div>
                    </div>
                    <a href="/group-detail/{{group['name']}}">
                        <button type="button" class="btn btn-primary d-block w-100">Join</button>
                    </a>
                </div>
            </div>`;
    }
});