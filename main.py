from fastapi import FastAPI
from app import database, models, auth, shorten, analytics
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])


app.include_router(shorten.router, tags=["Shorten"])
