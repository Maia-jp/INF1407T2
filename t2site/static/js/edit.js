// 
// CODE EDITOR
// 
const highlight = (editor) => {
    // highlight.js does not trims old tags,
    // let's do it by this hack.
    hljs.highlightBlock(editor);
};

const editor = document.querySelector(".editor");
const jar = new CodeJar(editor, highlight);
editor.textContent = editor.textContent.trim();




//
// AJAX Form
//
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}


function saveSnippet(id) {
    //Get postData
    var code = editor.textContent

    var data = {
        id:id,
        snippet: code
    }

    $.ajax(
        {
            type: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
            },
            data: data,
            success: function (data) {
                alert("Codigo Editado");
                const url = window.location.href.replace("/edit", "")
                window.location.href = url
            },
            error: function (request, status, error) {
                alert("Erro ao editar o codigo");
            }

        })

}