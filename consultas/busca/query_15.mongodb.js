// ============================================================================
// Query 15 - Múltiplos Lookups (= 4 JOINs)
// ============================================================================

db.Comments.aggregate([
  {
    $match: {
      CreationDate: { $gte: new Date("2010-09-01") }
    }
  },
  {
    $lookup: {
      from: "Posts",
      localField: "PostId",
      foreignField: "Id",
      as: "post"
    }
  },
  { $unwind: "$post" },
  {
    $match: {
      "post.PostTypeId": 1,
      "post.ViewCount": { $gt: 50000 }
    }
  },
  {
    $lookup: {
      from: "Users",
      localField: "UserId",
      foreignField: "Id",
      as: "autor_comentario"
    }
  },
  { $unwind: "$autor_comentario" },
  {
    $lookup: {
      from: "Users",
      localField: "post.OwnerUserId",
      foreignField: "Id",
      as: "autor_post"
    }
  },
  { $unwind: "$autor_post" },
  {
    $project: {
      _id: 0,
      comment_id: "$Id",
      data_comentario: "$CreationDate",
      autor_comentario: "$autor_comentario.DisplayName",
      autor_post: "$autor_post.DisplayName",
      pergunta: "$post.Title",
      ViewCount: "$post.ViewCount"
    }
  }
]);
