// ============================================================================
// Query 02 - Inserção de um novo post (Question) na coleção Posts
// ============================================================================

db.Posts.insertOne({
  Id: 2000001,
  PostTypeId: 1,
  CreationDate: new Date(),
  Score: 0,
  Title: "How to use SQL indexes?",
  OwnerUserId: 1000001,
  Body: "Example body content",
  LastActivityDate: new Date(),
  ViewCount: 0
});
