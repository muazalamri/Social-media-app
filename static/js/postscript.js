function copyCode(button) {
    var code = button.nextElementSibling.textContent;
    navigator.clipboard.writeText(code).then(() => {
        button.textContent = "Copied!";
        setTimeout(() => { button.textContent = "Copy"; }, 2000);
    });
}