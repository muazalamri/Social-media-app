let img=document.getElementById('gimg');
img.style.height='20hv';
img.style.width='20hv';
let inputFile=document.getElementById('img');
inputFile.addEventListener('change',function(){
    img.src=URL.createObjectURL(inputFile.files[0]);
    console.log('changeing');
});