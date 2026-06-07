from database import get_usuario_por_id, get_noticias

def recomendar_noticias(usuario_id):
    usuario = get_usuario_por_id(usuario_id)
    if not usuario:
        return None

    recomendadas = []

    for noticia in get_noticias():
        mesma_unidade = usuario["unidade"] in noticia["unidades_alvo"]
        interesses_comuns = set(usuario["interesses"]) & set(noticia["tags"])

        if mesma_unidade or interesses_comuns:
            recomendadas.append({
                **noticia,
                "motivo": list(interesses_comuns) if interesses_comuns else ["Sua unidade"]
            })

    return {
        "usuario": usuario["nome"],
        "total": len(recomendadas),
        "noticias": recomendadas
    }