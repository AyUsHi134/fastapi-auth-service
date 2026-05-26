from typing import Optional
from fastapi import FastAPI , HTTPException , status , Response  
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres', 
                                    password='*****', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful")
        break
    except Exception as error:
            print("Connection to database failed")
            print("Error:", error)
            time.sleep(2)

my_posts = [{"title": "movies to watch", "content": "dhurandhar", "id":1 },
            {"title":"favourite food","content":"i love pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "welcome to my api"}  

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return{"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
          
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
