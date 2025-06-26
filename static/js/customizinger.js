function setProto(jsData) {
      console.log(jsData);
      let item = jsData.Array[0];
      let elements = [];
      //console.log();
      // تحديد العناصر بناءً على نوع المحدد
      console.log('------');
      console.log(item.type);
      switch (item.type.toLowerCase()) {
        case 'class':
          elements = document.getElementsByClassName(item.value);
          break;
        case 'id':
          const el = document.getElementById(vitem.alue);
          if (el) elements = [el];
          break;
        case 'name':
          elements = document.getElementsByName(item.value);
          break;
        case 'tag':
          elements = document.getElementsByTagName(item.value);
          break;
        case 'tagns':
          // إذا كانت الخاصية namespace غير معرفة فسنستخدم null
          elements = document.getElementsByTagNameNS(namespace || null, value);
          break;
        default:
          console.warn(`Unknown selector type: ${item.type}`);
          return;
      }
  
      // إذا وُجدت خاصية لتعديلها وقيمة جديدة نطبق التعديل على كل العناصر
      if (item.attribute && item.newValue) {
        Array.from(elements).forEach(el => {
          // إذا كانت الخاصية تتعلق بالستايل (مثلاً "style.color")
          if (item.attribute.startsWith('style.')) {
            const styleProp = item.attribute.slice(6);
            el.style[styleProp] = item.newValue;
          } else {
            el.setAttribute(item.attribute, item.newValue);
          }
        });
      }
    }
  
function update() {
    fetch('/personalize')
        .then(response => setProto(response.json()))
}
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOMContentLoaded');
    update();
})

console.log('DOMContentLoaded');
  