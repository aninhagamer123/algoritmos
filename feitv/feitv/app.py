"""
FEItv - Controlador Principal da Aplicação
Gerencia todos os menus, fluxos e interações do usuário.
"""

import dados
import ui
from ui import (cabecalho, sucesso, erro, aviso, info, titulo_secao,
                menu, input_campo, pressione_enter,
                exibir_video, exibir_lista_videos, exibir_playlist, c, Cor)


class FEItvApp:

    def __init__(self):
        dados.inicializar()
        self.usuario_logado: dict | None = None

    # ──────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────

    def _curtidas_ids(self) -> set:
        if not self.usuario_logado:
            return set()
        return {c["video_id"] for c in dados.listar_curtidas()
                if c["usuario_id"] == self.usuario_logado["id"]}

    def _pedir_video_id(self, prompt="ID do vídeo") -> str | None:
        vid_id = input_campo(prompt)
        v = dados.buscar_video_por_id(vid_id)
        if not v:
            erro("Vídeo não encontrado com esse ID.")
            pressione_enter()
            return None
        return vid_id

    # ══════════════════════════════════════════
    # LOOP PRINCIPAL
    # ══════════════════════════════════════════

    def run(self):
        while True:
            if self.usuario_logado:
                self._menu_principal()
            else:
                self._menu_boas_vindas()

    # ══════════════════════════════════════════
    # MENU DE BOAS-VINDAS (não logado)
    # ══════════════════════════════════════════

    def _menu_boas_vindas(self):
        cabecalho("Bem-vindo!")
        print(c("  A sua plataforma de informações sobre filmes e séries.", Cor.DIM))
        print()
        escolha = menu(["Fazer Login", "Cadastrar-se", "Sair"])
        if escolha == "1":
            self._tela_login()
        elif escolha == "2":
            self._tela_cadastro()
        elif escolha == "3":
            cabecalho("Até logo!")
            print(c("  Até a próxima! 🎬\n", Cor.CIANO))
            exit(0)
        else:
            erro("Opção inválida.")
            pressione_enter()

    # ──────────────────────────────────────────
    # Cadastro
    # ──────────────────────────────────────────

    def _tela_cadastro(self):
        cabecalho("Cadastro de Usuário")
        titulo_secao("Preencha seus dados")

        nome  = input_campo("Nome completo")
        email = input_campo("E-mail")

        # Verifica duplicidade antes de pedir senha
        if dados.buscar_usuario_por_email(email):
            erro("E-mail já cadastrado. Tente fazer login.")
            pressione_enter()
            return

        senha  = input_campo("Senha")
        senha2 = input_campo("Confirme a senha")

        if senha != senha2:
            erro("As senhas não coincidem.")
            pressione_enter()
            return

        u = dados.cadastrar_usuario(nome, email, senha)
        if u:
            sucesso(f"Conta criada com sucesso! Bem-vindo(a), {u['nome']}!")
        else:
            erro("Não foi possível criar a conta.")
        pressione_enter()

    # ──────────────────────────────────────────
    # Login
    # ──────────────────────────────────────────

    def _tela_login(self):
        cabecalho("Login")
        titulo_secao("Entre com suas credenciais")

        email = input_campo("E-mail")
        senha = input_campo("Senha")

        u = dados.autenticar_usuario(email, senha)
        if u:
            self.usuario_logado = u
            sucesso(f"Login realizado! Olá, {u['nome']}! 👋")
            pressione_enter()
        else:
            erro("E-mail ou senha incorretos.")
            pressione_enter()

    # ══════════════════════════════════════════
    # MENU PRINCIPAL (logado)
    # ══════════════════════════════════════════

    def _menu_principal(self):
        nome = self.usuario_logado["nome"].split()[0]
        cabecalho(f"Olá, {nome}!")
        escolha = menu([
            "🔍  Buscar vídeos",
            "❤   Meus vídeos curtidos",
            "📋  Minhas playlists",
            "🚪  Sair / Trocar conta",
        ])
        if escolha == "1":
            self._menu_busca()
        elif escolha == "2":
            self._menu_curtidos()
        elif escolha == "3":
            self._menu_playlists()
        elif escolha == "4":
            self.usuario_logado = None
            sucesso("Sessão encerrada.")
            pressione_enter()
        else:
            erro("Opção inválida.")
            pressione_enter()

    # ══════════════════════════════════════════
    # BUSCA DE VÍDEOS
    # ══════════════════════════════════════════

    def _menu_busca(self):
        cabecalho("Buscar Vídeos")
        titulo_secao("Digite o título para buscar")

        termo = input_campo("Título (ou parte do título)")
        videos = dados.buscar_videos_por_nome(termo)

        cabecalho(f"Resultados para: \"{termo}\"")
        if not videos:
            aviso(f"Nenhum vídeo encontrado com \"{termo}\".")
            pressione_enter()
            return

        info(f"{len(videos)} resultado(s) encontrado(s).")
        exibir_lista_videos(videos, self._curtidas_ids())

        print()
        escolha = menu([
            "❤  Curtir / Descurtir um vídeo",
            "📋  Adicionar vídeo a uma playlist",
            "↩  Voltar",
        ])
        if escolha == "1":
            self._acao_curtir_descurtir(videos)
        elif escolha == "2":
            self._acao_adicionar_playlist(videos)

    # ──────────────────────────────────────────
    # Curtir / Descurtir
    # ──────────────────────────────────────────

    def _acao_curtir_descurtir(self, videos: list[dict] = None):
        uid = self.usuario_logado["id"]
        curtidas_ids = self._curtidas_ids()

        vid_id = self._pedir_video_id("ID do vídeo que deseja curtir/descurtir")
        if not vid_id:
            return

        if vid_id in curtidas_ids:
            if dados.descurtir_video(uid, vid_id):
                v = dados.buscar_video_por_id(vid_id)
                sucesso(f"Você descurtiu \"{v['titulo']}\".")
            else:
                erro("Não foi possível descurtir.")
        else:
            if dados.curtir_video(uid, vid_id):
                v = dados.buscar_video_por_id(vid_id)
                sucesso(f"Você curtiu \"{v['titulo']}\"! ❤")
            else:
                erro("Não foi possível curtir.")
        pressione_enter()

    # ──────────────────────────────────────────
    # Vídeos curtidos
    # ──────────────────────────────────────────

    def _menu_curtidos(self):
        cabecalho("Meus Vídeos Curtidos")
        uid = self.usuario_logado["id"]
        videos = dados.curtidas_do_usuario(uid)
        curtidas_ids = self._curtidas_ids()

        if not videos:
            aviso("Você ainda não curtiu nenhum vídeo.")
            pressione_enter()
            return

        info(f"{len(videos)} vídeo(s) curtido(s).")
        exibir_lista_videos(videos, curtidas_ids)

        print()
        escolha = menu(["♡  Descurtir um vídeo", "↩  Voltar"])
        if escolha == "1":
            self._acao_curtir_descurtir(videos)

    # ══════════════════════════════════════════
    # PLAYLISTS
    # ══════════════════════════════════════════

    def _menu_playlists(self):
        while True:
            cabecalho("Minhas Playlists")
            uid = self.usuario_logado["id"]
            playlists = dados.playlists_do_usuario(uid)

            if playlists:
                titulo_secao("Suas playlists")
                for p in playlists:
                    vids = dados.videos_da_playlist(p["id"])
                    exibir_playlist(p, len(vids))
            else:
                aviso("Você ainda não tem playlists.")

            escolha = menu([
                "➕  Criar nova playlist",
                "✏   Editar playlist",
                "🗑   Excluir playlist",
                "🎬  Ver vídeos de uma playlist",
                "➕  Adicionar vídeo à playlist",
                "➖  Remover vídeo da playlist",
                "↩  Voltar",
            ])

            if escolha == "1":
                self._criar_playlist()
            elif escolha == "2":
                self._editar_playlist(playlists)
            elif escolha == "3":
                self._excluir_playlist(playlists)
            elif escolha == "4":
                self._ver_videos_playlist(playlists)
            elif escolha == "5":
                self._acao_adicionar_playlist()
            elif escolha == "6":
                self._remover_video_playlist(playlists)
            elif escolha == "7":
                break
            else:
                erro("Opção inválida.")
                pressione_enter()

    def _criar_playlist(self):
        cabecalho("Criar Nova Playlist")
        titulo_secao("Informações da playlist")

        nome      = input_campo("Nome da playlist")
        descricao = input_campo("Descrição (opcional)", obrigatorio=False)

        p = dados.criar_playlist(self.usuario_logado["id"], nome, descricao)
        sucesso(f"Playlist \"{p['nome']}\" criada com sucesso! (ID: {p['id']})")
        pressione_enter()

    def _editar_playlist(self, playlists: list[dict]):
        if not playlists:
            aviso("Nenhuma playlist para editar.")
            pressione_enter()
            return

        cabecalho("Editar Playlist")
        pid = input_campo("ID da playlist que deseja editar")
        p = dados.buscar_playlist_por_id(pid)
        if not p or p["usuario_id"] != self.usuario_logado["id"]:
            erro("Playlist não encontrada ou não é sua.")
            pressione_enter()
            return

        info(f"Editando: {p['nome']} — deixe em branco para manter o valor atual.")
        novo_nome = input_campo(f"Novo nome [{p['nome']}]", obrigatorio=False)
        nova_desc = input_campo(f"Nova descrição [{p['descricao']}]", obrigatorio=False)

        dados.editar_playlist(pid, self.usuario_logado["id"],
                              novo_nome or None, nova_desc or None)
        sucesso("Playlist atualizada com sucesso!")
        pressione_enter()

    def _excluir_playlist(self, playlists: list[dict]):
        if not playlists:
            aviso("Nenhuma playlist para excluir.")
            pressione_enter()
            return

        cabecalho("Excluir Playlist")
        pid = input_campo("ID da playlist que deseja excluir")
        p = dados.buscar_playlist_por_id(pid)
        if not p or p["usuario_id"] != self.usuario_logado["id"]:
            erro("Playlist não encontrada ou não é sua.")
            pressione_enter()
            return

        confirm = input_campo(f"Confirme excluindo \"{p['nome']}\" (s/N)").lower()
        if confirm == "s":
            dados.excluir_playlist(pid, self.usuario_logado["id"])
            sucesso("Playlist excluída com sucesso.")
        else:
            aviso("Operação cancelada.")
        pressione_enter()

    def _ver_videos_playlist(self, playlists: list[dict]):
        if not playlists:
            aviso("Nenhuma playlist disponível.")
            pressione_enter()
            return

        cabecalho("Vídeos da Playlist")
        pid = input_campo("ID da playlist")
        p = dados.buscar_playlist_por_id(pid)
        if not p or p["usuario_id"] != self.usuario_logado["id"]:
            erro("Playlist não encontrada ou não é sua.")
            pressione_enter()
            return

        videos = dados.videos_da_playlist(pid)
        info(f"Playlist: {p['nome']} — {len(videos)} vídeo(s)")
        exibir_lista_videos(videos, self._curtidas_ids())
        pressione_enter()

    def _acao_adicionar_playlist(self, videos: list[dict] = None):
        uid = self.usuario_logado["id"]
        playlists = dados.playlists_do_usuario(uid)

        if not playlists:
            aviso("Você não tem playlists. Crie uma primeiro.")
            pressione_enter()
            return

        if videos:
            titulo_secao("Adicionar vídeo a uma playlist")
            for v in videos:
                print(c(f"  ID {v['id']}", Cor.CIANO) + f"  {v['titulo']}")

        vid_id = self._pedir_video_id("ID do vídeo a adicionar")
        if not vid_id:
            return

        titulo_secao("Suas playlists")
        for p in playlists:
            exibir_playlist(p, len(dados.videos_da_playlist(p["id"])))

        pid = input_campo("ID da playlist")
        p = dados.buscar_playlist_por_id(pid)
        if not p or p["usuario_id"] != uid:
            erro("Playlist não encontrada ou não é sua.")
            pressione_enter()
            return

        if dados.adicionar_video_playlist(pid, vid_id):
            v = dados.buscar_video_por_id(vid_id)
            sucesso(f"\"{v['titulo']}\" adicionado à playlist \"{p['nome']}\"!")
        else:
            aviso("Esse vídeo já está na playlist.")
        pressione_enter()

    def _remover_video_playlist(self, playlists: list[dict]):
        if not playlists:
            aviso("Nenhuma playlist disponível.")
            pressione_enter()
            return

        cabecalho("Remover Vídeo da Playlist")
        pid = input_campo("ID da playlist")
        p = dados.buscar_playlist_por_id(pid)
        if not p or p["usuario_id"] != self.usuario_logado["id"]:
            erro("Playlist não encontrada ou não é sua.")
            pressione_enter()
            return

        videos = dados.videos_da_playlist(pid)
        if not videos:
            aviso("Essa playlist está vazia.")
            pressione_enter()
            return

        info(f"Vídeos na playlist \"{p['nome']}\":")
        for v in videos:
            print(c(f"  ID {v['id']}", Cor.CIANO) + f"  {v['titulo']}")

        vid_id = self._pedir_video_id("ID do vídeo a remover")
        if not vid_id:
            return

        if dados.remover_video_playlist(pid, vid_id):
            v = dados.buscar_video_por_id(vid_id)
            sucesso(f"\"{v['titulo']}\" removido da playlist.")
        else:
            erro("Vídeo não encontrado na playlist.")
        pressione_enter()
