
// --- TIPO 1: AGRUPAMENTO E AGREGAÇÃO ANALÍTICA ---
// Baseado em padrões de "group by" e estatística

  // 1. Média de score por tipo de post
  db.Posts.aggregate([{$match:{Score:{$gt:0}}},{$group:{_id:"$PostTypeId",avgScore:{$avg:"$Score"},total:{$sum:1}}}]),
  // 2. Distribuição de badges por usuário (Top 100)
  db.Badges.aggregate([{$group:{_id:"$UserId",totalBadges:{$sum:1}}},{$sort:{totalBadges:-1}},{$limit:100}]),
  // 3. Usuários por localidade com reputação média
  db.Users.aggregate([{$group:{_id:"$Location",avgRep:{$avg:"$Reputation"},count:{$sum:1}}},{$match:{count:{$gt:50}}},{$sort:{avgRep:-1}}]),
  // 4. Volume de comentários por mês (extraído da data)
  db.Comments.aggregate([{$group:{_id:{$dateToString:{format:"%Y-%m",date:"$CreationDate"}},total:{$sum:1}}},{$sort:{_id:1}}]),
  // 5. Posts com maior volume de votos (Cross-collection)
  db.Votes.aggregate([{$group:{_id:"$PostId",count:{$sum:1}}},{$sort:{count:-1}},{$limit:100}]),
  // 6. Contar usuários por localização (= GROUP BY)
  db.Users.aggregate([{$group: {_id: "$Location",total_users: { $sum: 1 }}},{$sort: { total_users: -1 }}]),


// --- TIPO 2: JUNÇÃO (LOOKUP) E AUDITORIA DE GRAFO ---
// Baseado em navegação entre coleções

  // 1. Comentários de usuários BR sobre posts populares (OTIMIZADO)
  // Posts (já filtrando > 10000 views) -> Comentários -> Usuários
  db.Posts.aggregate([{ $match: { ViewCount: { $gt: 10000 } } },{ $lookup: { from: "Comments", localField: "Id", foreignField: "PostId", as: "comment" } },{ $unwind: "$comment" },{ $lookup: { from: "Users", localField: "comment.UserId", foreignField: "Id", as: "autor" } },{ $unwind: "$autor" },{ $match: { "autor.Location": /Brazil/i } },{ $project: { _id: 0, PostTitle: "$Title", CommentText: "$comment.Text", Autor: "$autor.DisplayName" } }]),
  
  // 2. Detalhes de respostas aceitas
  db.Posts.aggregate([{$match:{AcceptedAnswerId:{$exists:true}}},{$lookup:{from:"Posts",localField:"AcceptedAnswerId",foreignField:"Id",as:"respostas"}},{$project:{Title:1,respostas:1}}]),
  
  // 3. Usuários que receberam Badges específicos (OTIMIZADO)
  // Filtro exato no Badge primeiro
  db.Badges.aggregate([{$match:{"Name":"Popular Question"}},{$lookup:{from:"Users",localField:"UserId",foreignField:"Id",as:"user"}},{$unwind:"$user"}]),
  
  // 4. Auditoria de votos em posts de um usuário específico (OTIMIZADO)
  // Post (filtrando o OwnerUserId) -> Votos
  db.Posts.aggregate([{ $match: { OwnerUserId: 1000001 } },{ $lookup: { from: "Votes", localField: "Id", foreignField: "PostId", as: "votos" } },{ $unwind: "$votos" }]),
  
  // 5. Ligação entre posts relacionados
  db.PostLinks.aggregate([{$lookup:{from:"Posts",localField:"PostId",foreignField:"Id",as:"origem"}},{$lookup:{from:"Posts",localField:"RelatedPostId",foreignField:"Id",as:"destino"}}]),
  
  // 6. Posts com score > 100 e dados do autor
  db.Posts.aggregate([{ $match: { PostTypeId: 1, Score: { $gt: 100 } } },{ $lookup: { from: "Users", localField: "OwnerUserId", foreignField: "Id", as: "author" } },{ $unwind: "$author" },{ $project: { _id: 0, post_id: "$Id", Title: 1, CreationDate: 1, autor: "$author.DisplayName" } }]),
  
  // 7. Múltiplos Lookups (= 4 JOINs) (OTIMIZADO)
  // Posts muito visualizados -> Filtrar comentários novos -> Achar os autores
  db.Posts.aggregate([{ $match: { PostTypeId: 1, ViewCount: { $gt: 50000 } } },{ $lookup: { from: "Comments", localField: "Id", foreignField: "PostId", as: "comment" } },{ $unwind: "$comment" },{ $match: { "comment.CreationDate": { $gte: new Date("2010-09-01") } } },{ $lookup: { from: "Users", localField: "comment.UserId", foreignField: "Id", as: "autor_comentario" } },{ $unwind: "$autor_comentario" },{ $lookup: { from: "Users", localField: "OwnerUserId", foreignField: "Id", as: "autor_post" } },{ $unwind: "$autor_post" },{ $project: { _id: 0, comment_id: "$comment.Id", data_comentario: "$comment.CreationDate", autor_comentario: "$autor_comentario.DisplayName", autor_post: "$autor_post.DisplayName", pergunta: "$Title", ViewCount: 1 } }])



// --- TIPO 3: SUBCONSULTAS CORRELACIONADAS E FILTROS COMPLEXOS ---
// Baseado em $expr e pipelines internos

  // 1. Usuários que comentaram em seus próprios posts
  db.Posts.aggregate([{$lookup:{from:"Comments",let:{o:"$OwnerUserId",p:"$Id"},pipeline:[{$match:{$expr:{$and:[{$eq:["$PostId","$$p"]},{$eq:["$UserId","$$o"]}]}}}],as:"self"}}]),
  // 2. Posts com score maior que a média de sua categoria (uso de $expr)
  db.Posts.aggregate([{$group:{_id:"$PostTypeId",avgS:{$avg:"$Score"}}},{$lookup:{from:"Posts",localField:"_id",foreignField:"PostTypeId",as:"p"}},{$unwind:"$p"},{$match:{$expr:{$gt:["$p.Score","$avgS"]}}} ]),
  // 3. Usuários com reputação maior que a média de sua região
  db.Users.aggregate([{$group:{_id:"$Location",avgR:{$avg:"$Reputation"}}},{$lookup:{from:"Users",localField:"_id",foreignField:"Location",as:"u"}},{$unwind:"$u"},{$match:{$expr:{$gt:["$u.Reputation","$avgR"]}}} ]),
  // 4. Comentários em posts criados no mesmo dia que o usuário
  db.Comments.aggregate([{$lookup:{from:"Posts",localField:"PostId",foreignField:"Id",as:"p"}},{$lookup:{from:"Users",localField:"UserId",foreignField:"Id",as:"u"}},{$match:{$expr:{$eq:["$p.0.CreationDate","$u.0.CreationDate"]}}} ]),
  // 5. Badges ganhos por usuários com Reputação > 50000
  db.Badges.aggregate([{$lookup:{from:"Users",localField:"UserId",foreignField:"Id",as:"u"}},{$match:{"u.Reputation":{$gt:50000}}}]),


// --- TIPO 4: BUSCA POR CHAVE E TEXTUAL
// 1. Busca por chave primária (Id)
db.Posts.find({ Id: 1000 }),
// 2. Busca com regex (LIKE '%Brazil%')
db.Users.find({ Location: { $regex: /Brazil/i } },{ DisplayName: 1, AccountId: 1, Location: 1, _id: 0 }),



// --- TIPO 5: INSERÇÃO
// 1. Inserção de um novo usuário na coleção Users
db.Users.insertOne({Id: 1000001,DisplayName: "Ana",Location: "Brazil",Reputation: 100,CreationDate: new Date(),LastAccessDate: new Date(),DownVotes: 0,UpVotes: 0,Views: 0}),
// 2. Inserção de um novo post (Question) na coleção Posts
db.Posts.insertOne({Id: 2000001,PostTypeId: 1,CreationDate: new Date(),Score: 0,Title: "How to use SQL indexes?",OwnerUserId: 1000001,Body: "Example body content",LastActivityDate: new Date(),ViewCount: 0}),
// 3. Inserção de um novo comentário na coleção Comments
db.Comments.insertOne({Id: 12345676,PostId: 2000001,Score: 0,Text: "Great question!",CreationDate: new Date()}),
// 4. Inserção em lote de múltiplos usuários
db.Users.insertMany([
  {
    Id: 1000002,
    DisplayName: "Carlos",
    Location: "Portugal",
    Reputation: 200,
    CreationDate: new Date(),
    LastAccessDate: new Date(),
    DownVotes: 0,
    UpVotes: 5,
    Views: 10
  },
  {
    Id: 1000003,
    DisplayName: "Maria",
    Location: "Spain",
    Reputation: 350,
    CreationDate: new Date(),
    LastAccessDate: new Date(),
    DownVotes: 1,
    UpVotes: 20,
    Views: 50
  },
  {
    Id: 1000004,
    DisplayName: "João",
    Location: "Brazil",
    Reputation: 500,
    CreationDate: new Date(),
    LastAccessDate: new Date(),
    DownVotes: 2,
    UpVotes: 45,
    Views: 120
  }
]),
// 5. Inserção em lote de múltiplos posts
db.Posts.insertMany([
  {
    Id: 2000002,
    PostTypeId: 1,
    CreationDate: new Date(),
    Score: 5,
    Title: "Melhores práticas de indexação no MongoDB",
    OwnerUserId: 1000002,
    Body: "Quais são as melhores práticas no momento da criação de índices no MongoDB?",
    LastActivityDate: new Date(),
    ViewCount: 0
  },
  {
    Id: 2000003,
    PostTypeId: 2,
    CreationDate: new Date(),
    Score: 3,
    Title: null,
    OwnerUserId: 1000003,
    Body: "Como funciona o TLS no MongoDB?",
    LastActivityDate: new Date(),
    ViewCount: 0,
    ParentId: 2000002
  },
  {
    Id: 2000004,
    PostTypeId: 1,
    CreationDate: new Date(),
    Score: 10,
    Title: "How does MongoDB TLS works?",
    OwnerUserId: 1000004,
    Body: "I want to enable TLS encryption in my MongoDB cluster.",
    LastActivityDate: new Date(),
    ViewCount: 15
  }
]),


// --- TIPO 6: MODIFICAÇÃO
// 1. Atualizar localização de usuários
db.Users.updateMany({ Location: "Brazil" },{ $set: { Location: "Brasil" } }),
// 2. Incrementar reputação de usuários com reputação baixa
db.Users.updateMany({ Reputation: { $lt: 100 } },{ $inc: { Reputation: 50 } }),
// 3. Atualizar título de um post específico
db.Posts.updateOne({ Id: 2000001 },{ $set: { Title: "How to use indexes in SQL databases?" } }),
// 4. Remover comentários com score negativo
db.Comments.deleteMany({ Score: { $lt: 0 } }),
// 5. Remover badges com mais de 5 anos
db.Badges.deleteMany({ Date: { $lt: new Date(new Date().setFullYear(new Date().getFullYear() - 5)) } })