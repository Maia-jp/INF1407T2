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

// 
// CODE EDITOR
// 
const highlight = (editor) => {
  // highlight.js does not trims old tags,
  // let's do it by this hack.
  editor.textContent = editor.textContent;
  hljs.highlightBlock(editor);
};

const helloWorld = {
  "Python": 'print("Hello World!")',
  "Lua": 'print "Hello World!" ',
  "Go": 'import "fmt”\nfunc main() { fmt.Println("Hello world!") })',
  "Javascript": 'document.write("Hello world!");'
}

const editor = document.querySelector(".editor");
const jar = new CodeJar(editor, highlight);
editor.className = "editor language-Python"
jar.updateCode(helloWorld["Python"])

// Language change


function changeLang(){
  var langDoc = document.getElementById("codeLang");
  var lang = langDoc.value
  console.log("editor language ${lang}")
  editor.className = "editor language " + lang

  jar.updateCode(helloWorld[lang])
}



// AJAX Form
function saveSnippet(){
  //Get postData
  var langDoc = document.getElementById("codeLang");
  var lang = langDoc.value

  var titleDOC = document.getElementById("codeTitle");
  var title = titleDOC.value

  if (title.length < 1){
    title = "Novo"
  }

  var code = editor.textContent

  var data =  {
            snippetTitle: title,
            snippet: code,
            lang: lang
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
          const url = window.location.href.replace("new",data)
          window.location.href = url
        },
        error: function (request, status, error) {
            alert("Erro ao salvar o codigo");
        }

    })

}