import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pars import parse_url_to_df
from bd import to_sql, from_sql


app = FastAPI()

@app.get("/parse")
async def parse(url="https://habr.com/ru/feed/"):
    try:
        data = await parse_url_to_df(url)
        to_sql(data)
        return {"message": "The data is recorded in the DB"}
    except Exception as error:
        print(error)
        return {"error": str(error)}

@app.get("/articles")
def get_articles():
    try:
        data = from_sql()
        return JSONResponse( content=json.loads(json.dumps(data, ensure_ascii=False)),
            media_type="application/json; charset=utf-8")
    except Exception as error:
        print(error)
        return {"error": str(error)}
