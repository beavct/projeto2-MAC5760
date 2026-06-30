// ============================================================================
// Query 12 - Busca com regex (LIKE '%Brazil%')
// ============================================================================

db.Users.find(
  { Location: { $regex: /Brazil/i } },
  { DisplayName: 1, AccountId: 1, Location: 1, _id: 0 }
);
