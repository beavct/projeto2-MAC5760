// ============================================================================
// Query 01 - Inserção de um novo usuário na coleção Users
// ============================================================================

db.Users.insertOne({
  Id: 1000001,
  DisplayName: "Ana",
  Location: "Brazil",
  Reputation: 100,
  CreationDate: new Date(),
  LastAccessDate: new Date(),
  DownVotes: 0,
  UpVotes: 0,
  Views: 0
});
