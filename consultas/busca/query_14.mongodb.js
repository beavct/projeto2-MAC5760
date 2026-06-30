// ============================================================================
// Query 14 - Lookup/Join: posts com score > 100 e dados do autor
// ============================================================================

db.Posts.aggregate([
  {
    $match: {
      PostTypeId: 1,
      Score: { $gt: 100 }
    }
  },
  {
    $lookup: {
      from: "Users",
      localField: "OwnerUserId",
      foreignField: "Id",
      as: "author"
    }
  },
  {
    $unwind: "$author"
  },
  {
    $project: {
      _id: 0,
      post_id: "$Id",
      Title: 1,
      CreationDate: 1,
      autor: "$author.DisplayName"
    }
  }
]);
