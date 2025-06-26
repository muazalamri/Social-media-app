function likeit(id){
    console.log('************fetching********');
    console.log(fetch(`/liking/${id}`)
    .then((response) =>{
        response = response.json();
        return response;
}).then(response => {response=response['lnum'];
    return response+3;
}));
    let lik=document.getElementById(`lila${id}`);
    console.log(lik);
    lik.innerText=Number(lik.innerText)+1;
}
