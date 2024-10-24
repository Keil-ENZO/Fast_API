from fastapi import APIRouter, HTTPException
from http.client import responses
from models.Comment import Comment
import sqlite3

connection = sqlite3.connect('database.db')
router = APIRouter()


@router.get("/articles/{article_id}/comments", status_code=200)
async def root(article_id: int):
    cursor = connection.execute("SELECT * FROM Comment WHERE article_id = ?", (article_id,))
    comments = cursor.fetchall()
    cursor.close()

    obj = []
    for comment in comments:
        obj.append(Comment(
            comment_id=comment[0],
            author=comment[1],
            content=comment[2],
            article_id=comment[3]
        ))

    if len(obj) == 0:
        raise HTTPException(status_code=404, detail="No comments found")

    links = {
        "self": f"/v1/articles/{article_id}/comments",
        "parent": f"/v1/articles/{article_id}"
    }

    return {"status": responses[200], "comments": obj, "links": links}


@router.get("/articles/{article_id}/comments/{comment_id}", status_code=200)
async def getComment(article_id: int, comment_id: int):
    cursor = connection.execute("SELECT * FROM Comment WHERE article_id = ? AND comment_id = ?", (article_id, comment_id))
    comment = cursor.fetchone()

    if comment is not None:
        return comment
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

    cursor.close()

    return {"status": responses[200], "comment": comment}



@router.post("/articles/{article_id}/comments", status_code=201)
async def postComment(comment: Comment, article_id: int):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Comment (author, content, article_id) VALUES (?, ?, ?)",
        (comment.author, comment.content, article_id)
    )

    comment_id = cursor.lastrowid
    cursor.close()

    connection.commit()
    comment.comment_id = comment_id


    return {"status": responses[201], "message": "Comment created successfully", "comment": comment}


@router.delete("/articles/{article_id}/comments/{comment_id}", status_code=204)
async def deleteComment(article_id: int, comment_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Comment WHERE article_id = ? AND comment_id = ?", (article_id, comment_id))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comment not found")

    connection.commit()

    return {"status": responses[204], "message": "Comment deleted successfully"}


@router.put("/articles/{article_id}/comments/{comment_id}", status_code=200)
async def updateComment(article_id: int, comment_id: int, comment: Comment):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Comment SET author = ?, content = ? WHERE article_id = ? AND comment_id = ?",
        (comment.author, comment.content, article_id, comment_id)
    )

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Comment not found")

    connection.commit()

    return {"status": responses[200], "message": "Comment updated successfully", "comment": comment}