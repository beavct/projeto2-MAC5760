// ============================================================================
// Query 04 - Inserção em lote de múltiplos usuários
// ============================================================================

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
]);
