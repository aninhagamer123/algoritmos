"""
FEItv - Utilitários de Interface (Terminal)
Cores ANSI, formatação e helpers de exibição.
"""

import os

# ──────────────────────────────────────────────
# Cores ANSI
# ──────────────────────────────────────────────

class Cor:
    RESET   = "\033[0m"
    NEGRITO = "\033[1m"
    DIM     = "\033[2m"

    VERMELHO  = "\033[91m"
    VERDE     = "\033[92m"
    AMARELO   = "\033[93m"
    AZUL      = "\033[94m"
    MAGENTA   = "\033[95m"
    CIANO     = "\033[96m"
    BRANCO    = "\033[97m"

    BG_AZUL     = "\033[44m"
    BG_MAGENTA  = "\033[45m"
    BG_PRETO    = "\033[40m"


def c(texto, *cores):
    return "".join(cores) + str(texto) + Cor.RESET


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def linha(char="─", largura=60, cor=Cor.DIM):
    print(c(char * largura, cor))


def cabecalho(titulo: str):
    limpar()
    largura = 60
    print()
    print(c("█" * largura, Cor.AZUL))
    print(c("█" + " " * (largura - 2) + "█", Cor.AZUL))
    txt = f"  🎬 FEItv  —  {titulo}  "
    pad = largura - 2 - len(txt)
    print(c("█" + txt + " " * pad + "█", Cor.AZUL, Cor.NEGRITO))
    print(c("█" + " " * (largura - 2) + "█", Cor.AZUL))
    print(c("█" * largura, Cor.AZUL))
    print()


def sucesso(msg: str):
    print(c(f"  ✔  {msg}", Cor.VERDE, Cor.NEGRITO))


def erro(msg: str):
    print(c(f"  ✖  {msg}", Cor.VERMELHO, Cor.NEGRITO))


def aviso(msg: str):
    print(c(f"  ⚠  {msg}", Cor.AMARELO))


def info(msg: str):
    print(c(f"  ℹ  {msg}", Cor.CIANO))


def titulo_secao(txt: str):
    print()
    print(c(f"  ▶  {txt}", Cor.AMARELO, Cor.NEGRITO))
    linha()


def menu(opcoes: list[str]) -> str:
    """Exibe menu numerado e retorna a escolha do usuário."""
    print()
    for i, op in enumerate(opcoes, 1):
        num = c(f"  [{i}]", Cor.CIANO, Cor.NEGRITO)
        print(f"{num}  {op}")
    print()
    return input(c("  Sua escolha: ", Cor.BRANCO, Cor.NEGRITO)).strip()


def input_campo(prompt: str, obrigatorio=True) -> str:
    while True:
        val = input(c(f"  {prompt}: ", Cor.BRANCO)).strip()
        if val or not obrigatorio:
            return val
        erro("Campo obrigatório. Tente novamente.")


def pressione_enter():
    print()
    input(c("  Pressione Enter para continuar...", Cor.DIM))


def exibir_video(v: dict, usuario_id: str = None, curtidas_ids: set = None):
    """Exibe card completo de um vídeo."""
    print()
    largura = 60
    print(c("┌" + "─" * (largura - 2) + "┐", Cor.AZUL))

    titulo = v["titulo"][:largura - 8]
    tipo_str = c(f"[{v['tipo']}]", Cor.MAGENTA, Cor.NEGRITO)
    print(c("│", Cor.AZUL) + f"  {c(titulo, Cor.BRANCO, Cor.NEGRITO)}  {tipo_str}")

    print(c("│", Cor.AZUL) + c("├" + "─" * (largura - 3), Cor.DIM))

    campos = [
        ("Gênero",   v.get("genero", "-")),
        ("Ano",      v.get("ano", "-")),
        ("Diretor",  v.get("diretor", "-")),
        ("Elenco",   v.get("elenco", "-")[:50]),
        ("Nota",     f"⭐ {v.get('nota', '-')}"),
    ]
    for rotulo, valor in campos:
        rot = c(f"{rotulo:<10}", Cor.CIANO)
        print(c("│", Cor.AZUL) + f"  {rot}  {valor}")

    sinopse = v.get("sinopse", "")
    if sinopse:
        print(c("│", Cor.AZUL) + c("  Sinopse:", Cor.CIANO))
        palavras = sinopse.split()
        linha_atual = "    "
        for p in palavras:
            if len(linha_atual) + len(p) > largura - 4:
                print(c("│", Cor.AZUL) + c(linha_atual, Cor.DIM))
                linha_atual = "    " + p + " "
            else:
                linha_atual += p + " "
        if linha_atual.strip():
            print(c("│", Cor.AZUL) + c(linha_atual, Cor.DIM))

    curtidas = v.get("total_curtidas", "0")
    curtiu = curtidas_ids and v["id"] in curtidas_ids
    coracoes = c("❤ Curtido", Cor.VERMELHO) if curtiu else c("♡ Não curtido", Cor.DIM)
    print(c("│", Cor.AZUL) + f"  {coracoes}  {c(f'{curtidas} curtidas', Cor.DIM)}")
    print(c("│", Cor.AZUL) + f"  {c('ID: ' + v['id'], Cor.DIM)}")
    print(c("└" + "─" * (largura - 2) + "┘", Cor.AZUL))


def exibir_lista_videos(videos: list[dict], curtidas_ids: set = None):
    if not videos:
        aviso("Nenhum vídeo encontrado.")
        return
    for v in videos:
        exibir_video(v, curtidas_ids=curtidas_ids)


def exibir_playlist(p: dict, qtd_videos: int = 0):
    print()
    print(c(f"  📋 [{p['id']}] {p['nome']}", Cor.AMARELO, Cor.NEGRITO))
    if p.get("descricao"):
        print(c(f"      {p['descricao']}", Cor.DIM))
    print(c(f"      {qtd_videos} vídeo(s)", Cor.CIANO))
