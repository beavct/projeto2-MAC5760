// ============================================================================
// Query 03 - Inserção de um novo comentário na coleção Comments
// ============================================================================

db.Comments.insertOne({
  Id: 12345676,
  PostId: 2000001,
  Score: 0,
  Text: "Great question!",
  CreationDate: new Date()
});
