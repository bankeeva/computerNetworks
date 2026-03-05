import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from task4.pars import parse_url_to_df
from task4.bd import to_sql, from_sql


app = FastAPI()

@app.get("/parse")
async def parse(url="https://habr.com/ru/feed/"):
    try:
        df = await parse_url_to_df(url)
        to_sql(df)
        return {"message": "The data is recorded in the DB"}
    except Exception as error:
        print(error)

@app.get("/articles")
def get_articles():
    data = from_sql()
    return JSONResponse( content=json.loads(json.dumps(data, ensure_ascii=False)),
        media_type="application/json; charset=utf-8")
