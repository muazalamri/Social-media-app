function liking(interaction,elementType,elemntId) {
    const likeBox = document.getElementById("like-box-"+elemntId);
    let data = {
        interaction: interaction,
        id: elemntId,
        elementType: elementType
    };
    fetch("/elementlike", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            likeBox.innerText=Number(likeBox.innerText)+1; // Append the new like to the like box
        }
    }).catch(error => {
        console.error("Error:", error);
    });
    
}
function setliking(){
    let likeBoxs = document.getElementsByClassName('likeingbox');
    //test if it has altribute functioned
    for (let i = 0; i < likeBoxs.length; i++) {
        let likeBox = likeBoxs[i];
        let elemntId = likeBox.getAttribute('id').split('-')[2];
        let elementType = likeBox.getAttribute('id').split('-')[1];
        let section = likeBox.getAttribute('id').split('-')[3];
        likeBox.addEventListener('click', function() {
            liking("like",section,elementType,elemntId);
        });
    }
};