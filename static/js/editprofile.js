function contact(){
    let myForm=document.getElementById('conForm');
    let NewData= new FormData(myForm);
    fetch('/updatepro',{
        method: 'POST',
        body: NewData
    });
}
function initcon(){
    fetch('/personal')
}