document.getElementById('done').addEventListener('click', function() {
    document.getElementById('subber').click();
})
document.getElementById('rew').addEventListener('', function() {})
document.getElementById('codeV').addEventListener('', function() {})
document.getElementById('adder').addEventListener('', function() {})
function fet() {
    let pform = document.getElementById('postForm');
    //alert('hi');
    let pdata = new FormData(pform);
    //console.log(data);
    fetch('/AIeditor', {
        method: 'post',
        body: pdata
    })
    .then(response=>response.text())
    .then(response=>{
        document.getElementById('viewDiv').innerHTML = response
    });
}
document.getElementById('prev').addEventListener('click', function() {
    document.getElementById('viewDiv').innerHTML = "pre";
    let pform = document.getElementById('postForm');
    //alert('hi');
    let pdata = new FormData(pform);
    document.getElementById('viewDiv').innerHTML = "pre2";
    //alert(data);
    document.getElementById('viewDiv').innerHTML = String(pdata.get('edited'));
});
document.getElementById('AI-ed').addEventListener('click', function() {
    document.getElementById('prompt').style['display'] = 'block';
    document.getElementById('prompt').style['width'] = '100%';
});
document.getElementById('AI-aed').addEventListener('click', function() {
    document.getElementById('prompt').style['display'] = 'block';
    document.getElementById('prompt').style['width'] = '100%';
});
document.getElementById('gener').addEventListener('', function() {});