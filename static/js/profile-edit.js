document.getElementById("personal-info").addEventListener("submit", function(event) {
    event.preventDefault();
    let form = document.getElementById("personal-info");
    let formData = new FormData(form);
    fetch("/edit/personal", {
        method: "POST",
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.href = "/profile/me";
        } else {
            response.text().then(text => {
                document.body.innerHTML = text;
            });
        }
    });});