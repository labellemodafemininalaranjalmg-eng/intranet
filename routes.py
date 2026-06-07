from flask import Blueprint, request, jsonify, session
from database import get_usuario_por_email, get_noticias, criar_noticia, deletar_noticia, atualizar_noticia
from recomendacoes import recomendar_noticias
rotas = Blueprint("rotas", __name__)

def usuario_logado():
    return session.get("usuario_id")

def exige_login():
    if not usuario_logado():
        return jsonify({"erro": "Não autenticado"}), 401
    return None

from flask import render_template # Certifique-se de que render_template está no topo!


@rotas.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json()
    usuario = get_usuario_por_email(dados.get("email", ""))

    if not usuario or usuario["senha"] != dados.get("senha", ""):
        return jsonify({"erro": "Email ou senha incorretos"}), 401

    session["usuario_id"] = usuario["id"]
    return jsonify({"mensagem": "Login realizado!", "nome": usuario["nome"]})

@rotas.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado"})

@rotas.route("/api/me", methods=["GET"])
def get_me():
    id_atual = usuario_logado()
    if not id_atual:
        return jsonify({"erro": "Não autenticado"}), 401
    
    from database import get_usuario_por_id
    usuario = get_usuario_por_id(id_atual)
    if usuario:
        # O Dashboard precisa do 'nome' para exibir na tela
        return jsonify({"nome": usuario["nome"]})
    return jsonify({"erro": "Usuário não encontrado"}), 404

@rotas.route("/api/recomendacoes", methods=["GET"])
def recomendacoes():
    erro = exige_login()
    if erro:
        return erro
    resultado = recomendar_noticias(usuario_logado())
    return jsonify(resultado)

@rotas.route("/api/noticias", methods=["GET"])
def listar_noticias():
    erro = exige_login()
    if erro:
        return erro
    return jsonify(get_noticias())

@rotas.route("/api/noticias", methods=["POST"])
def nova_noticia():
    erro = exige_login() or exige_admin()
    if erro:
        return erro
    dados = request.get_json()
    from datetime import date
    dados["data"] = str(date.today())
    noticia = criar_noticia(dados)
    return jsonify(noticia), 201

@rotas.route("/api/noticias/<int:noticia_id>", methods=["DELETE"])
def remover_noticia(noticia_id):
    erro = exige_login() or exige_admin()
    if erro:
        return erro
    sucesso = deletar_noticia(noticia_id)
    if not sucesso:
        return jsonify({"erro": "Notícia não encontrada"}), 404
    return jsonify({"mensagem": "Notícia removida"})

# ── ADMIN ──────────────────────────────────
def exige_admin():
    from database import get_usuario_por_id
    usuario = get_usuario_por_id(usuario_logado())
    if not usuario or not usuario.get("admin"):
        return jsonify({"erro": "Acesso negado"}), 403
    return None

@rotas.route("/api/admin/noticias/<int:noticia_id>", methods=["PUT"])
def editar_noticia_admin(noticia_id):
    erro = exige_login() or exige_admin()
    if erro:
        return erro
    from database import atualizar_noticia
    dados = request.get_json()
    noticia = atualizar_noticia(noticia_id, dados)
    if not noticia:
        return jsonify({"erro": "Notícia não encontrada"}), 404
    return jsonify(noticia)

@rotas.route("/api/admin/disciplinas/<int:disciplina_id>", methods=["PUT"])
def editar_disciplina_admin(disciplina_id):
    erro = exige_login() or exige_admin()
    if erro:
        return erro
    import json, os
    caminho = os.path.join(os.path.dirname(__file__), "data", "disciplinas.json")
    with open(caminho, "r", encoding="utf-8") as f:
        disciplinas = json.load(f)
    dados = request.get_json()
    for i, d in enumerate(disciplinas):
        if d["id"] == disciplina_id:
            disciplinas[i] = {**d, **dados, "id": disciplina_id}
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(disciplinas, f, ensure_ascii=False, indent=2)
            return jsonify(disciplinas[i])
    return jsonify({"erro": "Disciplina não encontrada"}), 404

@rotas.route("/api/admin/verificar", methods=["GET"])
def verificar_admin():
    erro = exige_login()
    if erro:
        return erro
    from database import get_usuario_por_id
    id_atual = usuario_logado()
    usuario = get_usuario_por_id(id_atual)    
    if usuario:
        return jsonify({"admin": usuario.get("admin", False)})
    else:
    # Se não houver usuário, retorna falso ou erro 401 (Não autorizado)
        return jsonify({"admin": False, "erro": "Sessão inválida"}), 401

@rotas.route("/api/anotacoes/<int:disciplina_id>", methods=["GET"])
def get_anotacao(disciplina_id):
    erro = exige_login()
    if erro:
        return erro
    import json, os
    caminho = os.path.join(os.path.dirname(__file__), "data", "anotacoes.json")
    if not os.path.exists(caminho):
        return jsonify({"texto": ""})
    with open(caminho, "r", encoding="utf-8") as f:
        anotacoes = json.load(f)
    chave = f"{usuario_logado()}-{disciplina_id}"
    return jsonify({"texto": anotacoes.get(chave, "")})

@rotas.route("/api/anotacoes/<int:disciplina_id>", methods=["POST"])
def salvar_anotacao(disciplina_id):
    erro = exige_login()
    if erro:
        return erro
    import json, os
    caminho = os.path.join(os.path.dirname(__file__), "data", "anotacoes.json")
    anotacoes = {}
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            anotacoes = json.load(f)
    chave = f"{usuario_logado()}-{disciplina_id}"
    anotacoes[chave] = request.get_json().get("texto", "")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(anotacoes, f, ensure_ascii=False, indent=2)
    return jsonify({"mensagem": "Salvo!"}) 

@rotas.route("/api/disciplinas/<slug>", methods=["GET"])
def obter_disciplina_por_slug(slug):
    erro = exige_login()
    if erro:
        return erro
    
    import json, os
    caminho = os.path.join(os.path.dirname(__file__), "data", "disciplinas.json")
    
    with open(caminho, "r", encoding="utf-8") as f:
        disciplinas = json.load(f)
    
    # Busca a disciplina que tem o slug correspondente à URL
    disciplina = next((d for d in disciplinas if d.get("slug") == slug), None)
    
    if disciplina:
        return jsonify(disciplina)
    return jsonify({"erro": "Disciplina não encontrada"}), 404  

# cole no final do arquivo
@rotas.route("/api/disciplinas", methods=["GET"])
def listar_disciplinas():
    erro = exige_login()
    if erro:
        return erro
    import json, os
    caminho = os.path.join(os.path.dirname(__file__), "data", "disciplinas.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@rotas.route("/api/admin/noticias/<int:noticia_id>/destaque", methods=["POST"])
def toggle_destaque(noticia_id):
    erro = exige_login() or exige_admin()
    if erro:
        return erro
    from database import get_noticias
    noticias = get_noticias()
    for i, n in enumerate(noticias):
        if n["id"] == noticia_id:
            noticias[i]["destaque"] = not n.get("destaque", False)
            from database import _salvar
            _salvar("noticias.json", noticias)
            return jsonify({"destaque": noticias[i]["destaque"]})
    return jsonify({"erro": "Não encontrada"}), 404

@rotas.route("/api/noticias/destaque", methods=["GET"])
def noticias_destaque():
    erro = exige_login()
    if erro:
        return erro
    destaques = [n for n in get_noticias() if n.get("destaque")]
    return jsonify(destaques)