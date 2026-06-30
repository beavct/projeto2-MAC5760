// ============================================================================
// Query 08 - Atualizar título de um post específico
// ============================================================================

db.Posts.updateOne(
  { Id: 2000001 },
  { $set: { Title: "How to use indexes in SQL databases?" } }
);
