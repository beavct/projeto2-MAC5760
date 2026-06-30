// ============================================================================
// Query 10 - Remover badges com mais de 5 anos
// ============================================================================

var fiveYearsAgo = new Date();
fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);

db.Badges.deleteMany(
  { Date: { $lt: fiveYearsAgo } }
);
