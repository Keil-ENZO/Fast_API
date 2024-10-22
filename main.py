from http.client import responses

from fastapi import FastAPI
from models.Article import Article

import sqlite3

app = FastAPI()
connection = sqlite3.connect('database.db')

@app.get("/articles")
async def root():
    cursor = connection.execute("SELECT * FROM Article")
    articles = cursor.fetchall()

    obj = []
    for article in articles:
        obj.append(Article(
            article_id=article[0],
            title=article[1],
            slug=article[2],
            content=article[3],
            author=article[4]

        ))

    return {"articles": obj}

@app.get("/articles/{article_id}")
async def getArticle(article_id: int):
    cursor = connection.execute(f"SELECT * FROM Article WHERE article_id = {article_id}")
    article = cursor.fetchone()
    return {"article": article}

@app.post("/articles", status_code=201)
async def postArticle(article: Article):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Article (title, slug, content, author) VALUES (?, ?, ?, ?)", (article.title, article.slug, article.content, article.author))

    article_id = cursor.lastrowid
    cursor.close()

    connection.commit()
    article.article_id = article_id

    return {"status": responses[201], "message": "Article created successfully", "article": article}


@app.delete("/articles/{article_id}", status_code=204)
async def deleteArticle(article_id: int):
    connection.execute(f"DELETE FROM Article WHERE article_id = {article_id}")
    connection.commit()
    return {"status": responses[204], "message": "Article deleted successfully"}