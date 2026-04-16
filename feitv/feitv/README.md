# 🎬 FEItv — Plataforma de Informações de Vídeos

Plataforma de compartilhamento de informações sobre filmes e séries,
desenvolvida em Python com persistência em arquivos de texto (.txt).

---

## ▶ Como executar

```bash
python3 main.py
```

> Requer **Python 3.10+** (utiliza `dict | None` como type hint).
> Nenhuma biblioteca externa necessária — apenas a biblioteca padrão.

---

## 📁 Estrutura de arquivos

```
feitv/
├── main.py          ← Ponto de entrada
├── app.py           ← Controlador / menus
├── dados.py         ← Persistência (leitura/escrita nos .txt)
├── ui.py            ← Interface de terminal (cores, cards)
└── data/            ← Arquivos de dados (criados automaticamente)
    ├── usuarios.txt
    ├── videos.txt
    ├── curtidas.txt
    ├── playlists.txt
    └── playlist_videos.txt
```

---

## ✅ Funcionalidades implementadas

| Funcionalidade                            | Status |
|-------------------------------------------|--------|
| Cadastrar novo usuário                    | ✔      |
| Login de usuário (senha com hash SHA-256) | ✔      |
| Buscar vídeo por nome                     | ✔      |
| Listar informações detalhadas dos vídeos  | ✔      |
| Curtir vídeos                             | ✔      |
| Descurtir vídeos                          | ✔      |
| Criar lista de reprodução (playlist)      | ✔      |
| Editar playlist                           | ✔      |
| Excluir playlist                          | ✔      |
| Adicionar vídeo à playlist                | ✔      |
| Remover vídeo da playlist                 | ✔      |
| Persistência total em arquivos .txt       | ✔      |

---

## 🗄 Formato dos arquivos de dados

Todos os arquivos usam formato **CSV com cabeçalho**, extensão `.txt`.

### usuarios.txt
```
id,nome,email,senha_hash,criado_em
```

### videos.txt
```
id,titulo,tipo,genero,ano,sinopse,elenco,diretor,nota,total_curtidas
```

### curtidas.txt
```
usuario_id,video_id,curtido_em
```

### playlists.txt
```
id,usuario_id,nome,descricao,criado_em
```

### playlist_videos.txt
```
playlist_id,video_id,adicionado_em
```

---

## 🎬 Vídeos pré-cadastrados

O sistema já vem com **10 vídeos de demonstração**:
- Interestelar, Breaking Bad, Parasita, Stranger Things,
  O Poderoso Chefão, Dark, Cidade de Deus, The Last of Us,
  Clube da Luta, La Casa de Papel.

---

## 🔒 Segurança

As senhas são armazenadas como **hash SHA-256** — nunca em texto puro.
