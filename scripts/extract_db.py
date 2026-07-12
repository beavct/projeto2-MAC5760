import pandas as pd
import os

DIR_ORIGEM = '/home/ste_b/projeto_seguranca/db_data/db_data/outras'
DIR_DESTINO = '/home/ste_b/projeto_seguranca/db_data/'
QTD_POSTS = 100000


# Cria pasta de destino limpa
if not os.path.exists(DIR_DESTINO):
    os.makedirs(DIR_DESTINO)

# 1. POSTS (A base do experimento)
print(f"\n1. Extraindo os primeiros {QTD_POSTS} Posts...")
df_posts = pd.read_csv(f"{DIR_ORIGEM}/Posts.csv", nrows=QTD_POSTS)
post_ids_validos = set(df_posts['Id'])
df_posts.to_csv(f"{DIR_DESTINO}/Posts.csv", index=False)

# Coletando IDs de usuários que são donos desses posts (para filtrar a tabela Users depois)
usuarios_validos = set(df_posts['OwnerUserId'].dropna())

# 2. COMMENTS
print("2. Filtrando Comments órfãos...")
df_comments = pd.read_csv(f"{DIR_ORIGEM}/Comments.csv")
# Mantém apenas comentários que pertencem aos 100k posts válidos
df_comments_filtrado = df_comments[df_comments['PostId'].isin(post_ids_validos)]
# Adiciona os autores dos comentários na nossa lista de usuários válidos
usuarios_validos.update(df_comments_filtrado['UserId'].dropna())
df_comments_filtrado.to_csv(f"{DIR_DESTINO}/Comments.csv", index=False)
print(f"   -> Sobraram {len(df_comments_filtrado)} comentários íntegros.")

# 3. VOTES
print("3. Filtrando Votes órfãos...")
df_votes = pd.read_csv(f"{DIR_ORIGEM}/Votes.csv")
df_votes_filtrado = df_votes[df_votes['PostId'].isin(post_ids_validos)]
df_votes_filtrado.to_csv(f"{DIR_DESTINO}/Votes.csv", index=False)
print(f"   -> Sobraram {len(df_votes_filtrado)} votos íntegros.")

# 4. POSTLINKS
print("4. Filtrando PostLinks órfãos...")
if os.path.exists(f"{DIR_ORIGEM}/PostLinks.csv"):
    df_links = pd.read_csv(f"{DIR_ORIGEM}/PostLinks.csv")
    # Ambos os posts (origem e destino do link) precisam existir na nossa amostra
    df_links_filtrado = df_links[
        df_links['PostId'].isin(post_ids_validos) &
        df_links['RelatedPostId'].isin(post_ids_validos)
    ]
    df_links_filtrado.to_csv(f"{DIR_DESTINO}/PostLinks.csv", index=False)
    print(f"   -> Sobraram {len(df_links_filtrado)} links válidos.")

# 5. USERS
print("5. Filtrando Users (mantendo apenas autores de posts e comentários)...")
df_users = pd.read_csv(f"{DIR_ORIGEM}/Users.csv")
df_users_filtrado = df_users[df_users['Id'].isin(usuarios_validos)]
df_users_filtrado.to_csv(f"{DIR_DESTINO}/Users.csv", index=False)
print(f"   -> Sobraram {len(df_users_filtrado)} usuários envolvidos.")

# 6. BADGES
print("6. Filtrando Badges (apenas dos usuários válidos)...")
df_badges = pd.read_csv(f"{DIR_ORIGEM}/Badges.csv")
df_badges_filtrado = df_badges[df_badges['UserId'].isin(usuarios_validos)]
df_badges_filtrado.to_csv(f"{DIR_DESTINO}/Badges.csv", index=False)
print(f"   -> Sobraram {len(df_badges_filtrado)} badges válidas.")

# 7. POSTTYPES (Fixo)
if os.path.exists(f"{DIR_ORIGEM}/PostTypes.csv"):
    df_types = pd.read_csv(f"{DIR_ORIGEM}/PostTypes.csv")
    df_types.to_csv(f"{DIR_DESTINO}/PostTypes.csv", index=False)

print("\n=== SUCESSO! ===")
print("A sua nova pasta 'db_data' agora contém um banco de dados relacionalmente perfeito e leve.")