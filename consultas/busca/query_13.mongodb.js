// ============================================================================
// Query 13 - Agregação: contar usuários por localização (= GROUP BY)
// ============================================================================

db.Users.aggregate([
  {
    $group: {
      _id: "$Location",
      total_users: { $sum: 1 }
    }
  },
  {
    $sort: { total_users: -1 }
  }
]);
