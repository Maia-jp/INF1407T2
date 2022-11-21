function deleteCard(p) {
    // AJAX request using Jquery
    $.ajax(
        {
            type: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
            },
            data: {
                codeID: p
            },
            success: function (data) {
                removeElement(p)
            },
            error: function (request, status, error) {
                alert("Erro tentando deletar esse card");
            }

        })
}

// 
// AUX
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

function removeElement(id) {
    var elem = document.getElementById(id);
    return elem.parentNode.removeChild(elem);
}