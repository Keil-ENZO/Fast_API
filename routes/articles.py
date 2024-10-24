from fastapi import APIRouter, HTTPException
from http.client import responses
from models.Article import Article
import sqlite3

connection = sqlite3.connect('database.db')
router = APIRouter()

@router.get("/articles", status_code=200)
async def root():
    cursor = connection.execute("SELECT * FROM Article")
    articles = cursor.fetchall()
    cursor.close()

    obj = []
    for article in articles:
        obj.append(Article(
            article_id=article[0],
            title=article[1],
            slug=article[2],
            content=article[3],
            author=article[4]
        ))

    return {"status": responses[200], "articles": obj}

@router.get("/articles/{article_id}", status_code=200)
async def getArticle(article_id: int):
    cursor = connection.execute("SELECT * FROM Article WHERE article_id = ?", (article_id,))
    article = cursor.fetchone()

    if article is not None:
        return article
    else:
        raise HTTPException(status_code=404, detail="Article not found")

    cursor.close()

    return {"status": responses[200], "article": article}

@router.post("/articles", status_code=201)
async def postArticle(article: Article):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Article (title, slug, content, author) VALUES (?, ?, ?, ?)",
        (article.title, article.slug, article.content, article.author)
    )

    article_id = cursor.lastrowid
    cursor.close()

    connection.commit()
    article.article_id = article_id

    return {"status": responses[201], "message": "Article created successfully", "article": article}

@router.delete("/articles/{article_id}", status_code=204)
async def deleteArticle(article_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Article WHERE article_id = ?", (article_id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Article not found")

    cursor.close()
    connection.commit()

    return {"status": responses[204], "message": "Article deleted successfully"}

@router.put("/articles/{article_id}", status_code=200)
async def updateArticle(article_id: int, article: Article):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Article SET title = ?, slug = ?, content = ?, author = ? WHERE article_id = ?",
        (article.title, article.slug, article.content, article.author, article_id)
    )

    if cursor.rowcount > 0:
        article.article_id = article_id
        return article
    else:
        raise HTTPException(status_code=404, detail="Article not found")

    cursor.close()
    connection.commit()

    return {"status": responses[200], "message": "Article updated successfully", "article": article}