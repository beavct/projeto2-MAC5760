// ============================================================================
// Query 06 - Atualizar localização de usuários
// ============================================================================

db.Users.updateMany(
  { Location: "Brazil" },
  { $set: { Location: "Brasil" } }
);
