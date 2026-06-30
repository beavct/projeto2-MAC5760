// ============================================================================
// Query 07 - Incrementar reputação de usuários com reputação baixa
// ============================================================================

db.Users.updateMany(
  { Reputation: { $lt: 100 } },
  { $inc: { Reputation: 50 } }
);
