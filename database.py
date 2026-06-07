import json
import os

BASE = os.path.join(os.path.dirname(__file__), "data")

def _carregar(arquivo):
    caminho = os.path.join(BASE, arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(arquivo, dados):
    caminho = os.path.join(BASE, arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def get_usuarios():
    return _carregar("usuarios.json")

def get_noticias():
    return _carregar("noticias.json")

def get_usuario_por_email(email):
    return next((u for u in get_usuarios() if u["email"] == email), None)

def get_usuario_por_id(usuario_id):
    return next((u for u in get_usuarios() if u["id"] == usuario_id), None)

def criar_noticia(dados):
    noticias = get_noticias()
    novo_id = max((n["id"] for n in noticias), default=0) + 1
    dados["id"] = novo_id
    noticias.append(dados)
    _salvar("noticias.json", noticias)
    return dados

def deletar_noticia(noticia_id):
    noticias = get_noticias()
    novas = [n for n in noticias if n["id"] != noticia_id]
    if len(novas) == len(noticias):
        return False
    _salvar("noticias.json", novas)
    return True

def atualizar_noticia(noticia_id, dados):
    noticias = get_noticias()
    for i, n in enumerate(noticias):
        if n["id"] == noticia_id:
            noticias[i] = {**n, **dados, "id": noticia_id}
            _salvar("noticias.json", noticias)
            return noticias[i]
    return None