from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter
from .. import models,schemas, oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func



router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def abcd(db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user), Limit:int=5, skip:int=0, search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=curs or.fetchall()
    
    """posts=db.query(models.Post).filter(
         models.Post.title.contains(search)).limit(Limit).offset(skip).all()"""
    posts=db.query(models.Post, func.count(models.Vote.post_id.label("voting"))).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
         models.Post.title.contains(search)).limit(Limit).offset(skip).all()
   
    return posts


"""@router.get("/{id}", response_model=schemas.PostOut)
#@router.get("/{id}")
def get_post(id:int, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    #posts=db.query(models.Post).filter(models.Post.id==id).first()
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("vot")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with this id does not found")
    return posts"""


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.My_data)
def create_posts(mydata:schemas.PostCreate,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    #cursor.execute("""insert into posts (content,title,published) values(%s,%s,%s) returning*""", (mydata.content, mydata.title, mydata.published))
    #new_post=cursor.fetchone()
    #conn.commit()

    new_post=models.Post(owner_id=current_user.id,**mydata.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM POSTS whered=%s RETURNING *""", (str(id)))
    #delete_one = cursor.fetchone()
    #conn.commit()
    deletee = db.query(models.Post).filter(models.Post.id==id)
    delete =  deletee.first()
    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"not authorized to perform requested action")
    deletee.delete(synchronize_session= False)
    db.commit()
     
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.My_data)
def update_post(id:str , updated_post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    #update_one = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    var = post_query.first()
    if var == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    
    if var.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
    
 