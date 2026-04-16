"""
FEItv - Gerenciador de Dados (Persistência em Arquivos .txt)
Todas as operações de leitura e escrita nos arquivos de texto.
"""

import os
import csv
import hashlib
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

USERS_FILE     = os.path.join(DATA_DIR, "usuarios.txt")
VIDEOS_FILE    = os.path.join(DATA_DIR, "videos.txt")
LIKES_FILE     = os.path.join(DATA_DIR, "curtidas.txt")
PLAYLISTS_FILE = os.path.join(DATA_DIR, "playlists.txt")
PL_ITEMS_FILE  = os.path.join(DATA_DIR, "playlist_videos.txt")

# ──────────────────────────────────────────────
# Utilidades internas
# ──────────────────────────────────────────────

def _ensure_files():
    """Garante que o diretório e todos os arquivos existem."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in [USERS_FILE, VIDEOS_FILE, LIKES_FILE, PLAYLISTS_FILE, PL_ITEMS_FILE]:
        if not os.path.exists(path):
            open(path, "w", encoding="utf-8").close()


def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def _ler_csv(caminho: str) -> list[dict]:
    """Lê um arquivo CSV e retorna lista de dicionários."""
    linhas = []
    if not os.path.exists(caminho):
        return linhas
    with open(caminho, "r", encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for row in leitor:
            linhas.append(dict(row))
    return linhas


def _escrever_csv(caminho: str, campos: list[str], linhas: list[dict]):
    """Escreve lista de dicionários em arquivo CSV."""
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)


# ──────────────────────────────────────────────
# USUÁRIOS
# ──────────────────────────────────────────────

CAMPOS_USUARIO = ["id", "nome", "email", "senha_hash", "criado_em"]


def listar_usuarios() -> list[dict]:
    return _ler_csv(USERS_FILE)


def buscar_usuario_por_email(email: str) -> dict | None:
    for u in listar_usuarios():
        if u["email"].lower() == email.lower():
            return u
    return None


def buscar_usuario_por_id(uid: str) -> dict | None:
    for u in listar_usuarios():
        if u["id"] == uid:
            return u
    return None


def cadastrar_usuario(nome: str, email: str, senha: str) -> dict | None:
    """Retorna o usuário criado ou None se e-mail já existe."""
    if buscar_usuario_por_email(email):
        return None
    usuarios = listar_usuarios()
    novo_id = str(len(usuarios) + 1)
    novo = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "senha_hash": _hash_senha(senha),
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    usuarios.append(novo)
    _escrever_csv(USERS_FILE, CAMPOS_USUARIO, usuarios)
    return novo


def autenticar_usuario(email: str, senha: str) -> dict | None:
    """Retorna usuário se credenciais válidas, senão None."""
    u = buscar_usuario_por_email(email)
    if u and u["senha_hash"] == _hash_senha(senha):
        return u
    return None


# ──────────────────────────────────────────────
# VÍDEOS
# ──────────────────────────────────────────────

CAMPOS_VIDEO = ["id", "titulo", "tipo", "genero", "ano", "sinopse",
                "elenco", "diretor", "nota", "total_curtidas"]


def listar_videos() -> list[dict]:
    return _ler_csv(VIDEOS_FILE)


def buscar_video_por_id(vid: str) -> dict | None:
    for v in listar_videos():
        if v["id"] == vid:
            return v
    return None


def buscar_videos_por_nome(termo: str) -> list[dict]:
    termo_lower = termo.lower()
    return [v for v in listar_videos() if termo_lower in v["titulo"].lower()]


def adicionar_video(titulo, tipo, genero, ano, sinopse, elenco, diretor, nota) -> dict:
    videos = listar_videos()
    novo_id = str(len(videos) + 1)
    novo = {
        "id": novo_id,
        "titulo": titulo,
        "tipo": tipo,
        "genero": genero,
        "ano": str(ano),
        "sinopse": sinopse,
        "elenco": elenco,
        "diretor": diretor,
        "nota": str(nota),
        "total_curtidas": "0",
    }
    videos.append(novo)
    _escrever_csv(VIDEOS_FILE, CAMPOS_VIDEO, videos)
    return novo


def _atualizar_video(video: dict):
    videos = listar_videos()
    for i, v in enumerate(videos):
        if v["id"] == video["id"]:
            videos[i] = video
            break
    _escrever_csv(VIDEOS_FILE, CAMPOS_VIDEO, videos)


# ──────────────────────────────────────────────
# CURTIDAS
# ──────────────────────────────────────────────

CAMPOS_CURTIDA = ["usuario_id", "video_id", "curtido_em"]


def listar_curtidas() -> list[dict]:
    return _ler_csv(LIKES_FILE)


def usuario_curtiu(usuario_id: str, video_id: str) -> bool:
    for c in listar_curtidas():
        if c["usuario_id"] == usuario_id and c["video_id"] == video_id:
            return True
    return False


def curtir_video(usuario_id: str, video_id: str) -> bool:
    """Retorna True se curtiu (False se já tinha curtido)."""
    if usuario_curtiu(usuario_id, video_id):
        return False
    curtidas = listar_curtidas()
    curtidas.append({
        "usuario_id": usuario_id,
        "video_id": video_id,
        "curtido_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _escrever_csv(LIKES_FILE, CAMPOS_CURTIDA, curtidas)
    # Incrementa contador no vídeo
    v = buscar_video_por_id(video_id)
    if v:
        v["total_curtidas"] = str(int(v["total_curtidas"]) + 1)
        _atualizar_video(v)
    return True


def descurtir_video(usuario_id: str, video_id: str) -> bool:
    """Retorna True se descurtiu (False se não havia curtido)."""
    curtidas = listar_curtidas()
    novas = [c for c in curtidas
             if not (c["usuario_id"] == usuario_id and c["video_id"] == video_id)]
    if len(novas) == len(curtidas):
        return False
    _escrever_csv(LIKES_FILE, CAMPOS_CURTIDA, novas)
    v = buscar_video_por_id(video_id)
    if v:
        total = max(0, int(v["total_curtidas"]) - 1)
        v["total_curtidas"] = str(total)
        _atualizar_video(v)
    return True


def curtidas_do_usuario(usuario_id: str) -> list[dict]:
    """Retorna lista de vídeos curtidos pelo usuário."""
    ids = [c["video_id"] for c in listar_curtidas() if c["usuario_id"] == usuario_id]
    return [v for v in listar_videos() if v["id"] in ids]


# ──────────────────────────────────────────────
# PLAYLISTS
# ──────────────────────────────────────────────

CAMPOS_PLAYLIST = ["id", "usuario_id", "nome", "descricao", "criado_em"]
CAMPOS_PL_ITEM  = ["playlist_id", "video_id", "adicionado_em"]


def listar_playlists() -> list[dict]:
    return _ler_csv(PLAYLISTS_FILE)


def playlists_do_usuario(usuario_id: str) -> list[dict]:
    return [p for p in listar_playlists() if p["usuario_id"] == usuario_id]


def buscar_playlist_por_id(pid: str) -> dict | None:
    for p in listar_playlists():
        if p["id"] == pid:
            return p
    return None


def criar_playlist(usuario_id: str, nome: str, descricao: str = "") -> dict:
    playlists = listar_playlists()
    novo_id = str(len(playlists) + 1)
    nova = {
        "id": novo_id,
        "usuario_id": usuario_id,
        "nome": nome,
        "descricao": descricao,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    playlists.append(nova)
    _escrever_csv(PLAYLISTS_FILE, CAMPOS_PLAYLIST, playlists)
    return nova


def editar_playlist(playlist_id: str, usuario_id: str,
                    novo_nome: str = None, nova_descricao: str = None) -> bool:
    playlists = listar_playlists()
    for p in playlists:
        if p["id"] == playlist_id and p["usuario_id"] == usuario_id:
            if novo_nome is not None:
                p["nome"] = novo_nome
            if nova_descricao is not None:
                p["descricao"] = nova_descricao
            _escrever_csv(PLAYLISTS_FILE, CAMPOS_PLAYLIST, playlists)
            return True
    return False


def excluir_playlist(playlist_id: str, usuario_id: str) -> bool:
    playlists = listar_playlists()
    novas = [p for p in playlists
             if not (p["id"] == playlist_id and p["usuario_id"] == usuario_id)]
    if len(novas) == len(playlists):
        return False
    _escrever_csv(PLAYLISTS_FILE, CAMPOS_PLAYLIST, novas)
    # Remove itens da playlist
    itens = _ler_csv(PL_ITEMS_FILE)
    itens = [i for i in itens if i["playlist_id"] != playlist_id]
    _escrever_csv(PL_ITEMS_FILE, CAMPOS_PL_ITEM, itens)
    return True


def videos_da_playlist(playlist_id: str) -> list[dict]:
    itens = _ler_csv(PL_ITEMS_FILE)
    ids = [i["video_id"] for i in itens if i["playlist_id"] == playlist_id]
    return [v for v in listar_videos() if v["id"] in ids]


def adicionar_video_playlist(playlist_id: str, video_id: str) -> bool:
    itens = _ler_csv(PL_ITEMS_FILE)
    for i in itens:
        if i["playlist_id"] == playlist_id and i["video_id"] == video_id:
            return False  # Já existe
    itens.append({
        "playlist_id": playlist_id,
        "video_id": video_id,
        "adicionado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _escrever_csv(PL_ITEMS_FILE, CAMPOS_PL_ITEM, itens)
    return True


def remover_video_playlist(playlist_id: str, video_id: str) -> bool:
    itens = _ler_csv(PL_ITEMS_FILE)
    novos = [i for i in itens
             if not (i["playlist_id"] == playlist_id and i["video_id"] == video_id)]
    if len(novos) == len(itens):
        return False
    _escrever_csv(PL_ITEMS_FILE, CAMPOS_PL_ITEM, novos)
    return True


# ──────────────────────────────────────────────
# Inicialização
# ──────────────────────────────────────────────

def inicializar():
    """Cria estrutura de arquivos e popula vídeos de exemplo se necessário."""
    _ensure_files()
    if not listar_videos():
        _popular_videos_demo()


def _popular_videos_demo():
    videos_demo = [
        ("Interestelar", "Filme", "Ficção Científica", 2014,
         "Um grupo de exploradores viaja pelo buraco de minhoca em busca de um novo lar para a humanidade.",
         "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "Christopher Nolan", 9.0),
        ("Breaking Bad", "Série", "Drama/Thriller", 2008,
         "Um professor de química do ensino médio, diagnosticado com câncer terminal, começa a fabricar metanfetamina.",
         "Bryan Cranston, Aaron Paul, Anna Gunn", "Vince Gilligan", 9.5),
        ("Parasita", "Filme", "Thriller", 2019,
         "Toda a família Kim está desempregada. Eles se aproximam da rica família Park e infiltram-se em suas vidas.",
         "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong", "Bong Joon-ho", 8.6),
        ("Stranger Things", "Série", "Ficção Científica/Terror", 2016,
         "Quando um garoto desaparece, sua mãe, um xerife e seus amigos devem confrontar forças sobrenaturais.",
         "Millie Bobby Brown, Finn Wolfhard, Winona Ryder", "Duffer Brothers", 8.7),
        ("O Poderoso Chefão", "Filme", "Crime/Drama", 1972,
         "O envelhecido patriarca de uma dinastia do crime organizado transfere o controle do seu império para seu filho relutante.",
         "Marlon Brando, Al Pacino, James Caan", "Francis Ford Coppola", 9.2),
        ("Dark", "Série", "Ficção Científica/Mistério", 2017,
         "Uma saga de viagem no tempo envolvendo quatro famílias interligadas em uma pequena cidade alemã.",
         "Louis Hofmann, Oliver Masucci, Karoline Eichhorn", "Baran bo Odar", 8.8),
        ("Cidade de Deus", "Filme", "Crime/Drama", 2002,
         "Dois meninos crescem na Cidade de Deus, favela violenta do Rio. Um quer ser fotógrafo; outro se torna chefão do tráfico.",
         "Alexandre Rodrigues, Leandro Firmino, Phellipe Haagensen", "Fernando Meirelles", 8.6),
        ("The Last of Us", "Série", "Drama/Ficção Científica", 2023,
         "Após uma pandemia devastadora, Joel e Ellie viajam pelo que restou dos EUA em busca de sobrevivência.",
         "Pedro Pascal, Bella Ramsey, Gabriel Luna", "Craig Mazin", 8.8),
        ("Clube da Luta", "Filme", "Drama/Thriller", 1999,
         "Um insone e um vendedor de sabão formam um clube de luta que se torna algo muito maior.",
         "Brad Pitt, Edward Norton, Helena Bonham Carter", "David Fincher", 8.8),
        ("La Casa de Papel", "Série", "Crime/Thriller", 2017,
         "Um misterioso Professor planeja o maior roubo da história da Espanha junto com oito ladrões.",
         "Álvaro Morte, Úrsula Corberó, Itziar Ituño", "Álex Pina", 8.3),
    ]
    for v in videos_demo:
        adicionar_video(*v)
