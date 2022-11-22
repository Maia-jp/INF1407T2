# T2 ProgWeb
Joao P Maia - 1920354

# CodeShare - T2 Prog Web

---

Esse é o segundo trabalho da disciplina "Programação para Web" onde devemos criar um site.
O site que resolvi desenvolver se chama "CodeShare", um site para compartilhamentos de codigo.

Nesse site varios usuarios podem criar páginas com trechos de código para compartilhar com outras pessoas.

## Links

- [Web Server](http://joaozzx2.pythonanywhere.com/)
- [Github](https://github.com/Maia-jp/INF1407T2)

# Como funciona ?

---

### Pagina de Login

![Untitled](T2%20ProgWeb%20462cd025f7234403b0d9bb163609b9b3/Untitled.png)

Primeiramente temos uma página de login onde o usuário pode entrar com as suas credenciais. Somente logado um usuario pode criar/editar codigos. Um usuário sem Login pode somente vizualizar codigos (Read-Only).

Caso o usuario não tenha uma conta ele pode clicar em "Sign Up” para acessar a pagina de cadastro.

### Pagina de Cadastro

![Untitled](T2%20ProgWeb%20462cd025f7234403b0d9bb163609b9b3/Untitled%201.png)

Aqui o usuario entra com as suas credencias para criar uma nova conta. Feito isso ele pode voltar para tela de Login e Logar.

### Tela Principal

![Untitled](T2%20ProgWeb%20462cd025f7234403b0d9bb163609b9b3/Untitled%202.png)

Ao logar, o usuário entra na sua pagina principal onde ele pode criar um novo código (e vizualizar os antigos). No primeiro acesso o usuário não possui nenhum código ainda… Para isso ele precisa adicionar um novo.

### Adicionar Codigo

![Untitled](T2%20ProgWeb%20462cd025f7234403b0d9bb163609b9b3/Untitled%203.png)

Nessa tela o usuario pode criar um novo codigo. Esse código pode ser escrito em uma série de linguagens (selecionadas no topo da janela). Alem disso, o usuário pode colocar um titulo para esse código.

Atualmente o site suporta as seguintes linguagens:

- Go
- Javascript
- Lua
- Python

Ao clicar em salvar, o usuário ira direto para página do código. Podendo retornar clicando na logo dentro da NavBar.

Na pagina do código, o usuário pode compartilhar o link para qualquer pessoa. Entretando somente ele pode editar.

### Tela principal

![Untitled](T2%20ProgWeb%20462cd025f7234403b0d9bb163609b9b3/Untitled%204.png)

Ao adicionar um novo código veremos a tela principal assim. Com uma lista dos codigos do usuario.

# Como o projeto atende ao enunciado ?

---

## Deve conter as quatro operações básicas em banco de dados (CRUD)

### CREATE

A parte de criar podemos observar primeramente na criação de usuario. E posteiromente na parte de criar um Codigo de programacao. 

Isso ocorre no seguinte caminho [http://joaozzx2.pythonanywhere.com/snippet/new](http://joaozzx2.pythonanywhere.com/snippet/new)

Ao criarmos um código de programação ele é adicionado ao banco de dados (Back-End Django) através de um POST request:

```python
if request.method == "POST":
            user = User.objects.get(username=request.user.username)
            title = request.POST['snippetTitle']
            code = request.POST['snippet']
            lang = ProgLang.objects.get(name=request.POST['lang'])
            
            newSnippet = Snippet(author=user, code=code,
                                 lang=lang, title=title)
            newSnippet.save()
            return HttpResponse("{}".format(newSnippet.id))
```

### READ

A leitura é feita em diversar partes do projeto. Na página inicial ao carregar os códigos que o usuário ja criou, assim como em cada página de código criada. 

Como por exemplo:
[http://joaozzx2.pythonanywhere.com/snippet/01064eca-850d-4055-8b4e-7690dfbecbd6](http://joaozzx2.pythonanywhere.com/snippet/01064eca-850d-4055-8b4e-7690dfbecbd6)

Ao acessar essa pagina, realizamos uma operação de leitura no banco para encontrar o código desejado:

```python
def snippetTemplate(request, id):
    id = uuid.UUID(id)
    obj = Snippet.objects.get(id=id)

    context = {
        "code": obj.code,
        "author": obj.author.username,
        "title": obj.title,
        "date": obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
        "edit": request.user.username == obj.author.username,
        "lang": obj.lang_id
    }

    template = loader.get_template('snippet.html')
    return HttpResponse(template.render(context, request))
```

### UPDATE

O Update, fazemos principalmente na hora de alterar os códigos. Caso o usuário seja o criador do código. Para acessar uma página de edição basta clicar no botao "Editar” dentro da página do seu propio código.

```python
def snippetEditPost(request):
    id_inPost = request.POST['id']
    code = request.POST['snippet']

    id = uuid.UUID(id_inPost)
    Snippet.objects.filter(id=id).update(code=code)

    return HttpResponse(id_inPost)
```

### DELETE

A operação de deletar é realizada na pagina principal ao clicarmos em "Delete". Ela faz um request que deleta um código criado pelo usuário.

 

```python
#ajax requests
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    #DELETE
    if request.method == 'DELETE':
        if is_ajax:
            # Delete codeID
            qd = QueryDict(request.body)
            codeID = uuid.UUID(qd["codeID"])
            snippet = Snippet.objects.get(id=codeID)
            snippet.delete()
        
            #Respose
            response_data = {}
            response_data['status'] = 'ok'
            return HttpResponse(json.dumps(response_data))
```

## AJAX. O mesmo código que foi usado em sala de aula não conta.

O AJAX é utilizado na hora de deletar os códigos da página principal. Utilizamos ele para deletar códigos sem precisar recarregar as páginas.

```jsx
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
```

```python
#ajax requests
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    #DELETE
    if request.method == 'DELETE':
        if is_ajax:
            # Delete codeID
            qd = QueryDict(request.body)
            codeID = uuid.UUID(qd["codeID"])
            snippet = Snippet.objects.get(id=codeID)
            snippet.delete()
        
            #Respose
            response_data = {}
            response_data['status'] = 'ok'
            return HttpResponse(json.dumps(response_data))
```

## Login, acesso e/ou ações selecionadas por usuário. Cada usuário deverá ter visões diferentes do site.

Esse requisito é atendido durante todo o projeto. Cada usuário só pode alterar os seus próprios códigos por exempo. Assim como usuários só podem acessar a tela de edição se logados na conta que criou o código.

Usuario não logados não podem criar códigos.
