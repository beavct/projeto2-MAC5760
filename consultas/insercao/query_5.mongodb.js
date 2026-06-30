// ============================================================================
// Query 05 - Inserção em lote de múltiplos posts
// ============================================================================

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
]);
