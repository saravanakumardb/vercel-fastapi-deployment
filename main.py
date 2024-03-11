from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from strawberry.fastapi import GraphQLRouter
import strawberry

# Define your GraphQL schema using Strawberry
@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "World") -> str:
        return f"Hello {name}"

schema = strawberry.Schema(query=Query)

# Create a GraphQL router
graphql_app = GraphQLRouter(schema)

# Initialize your FastAPI application
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

# Include the GraphQL router in your FastAPI application
app.include_router(graphql_app, prefix="/graphql")

# Your existing FastAPI route
@app.get("/")
def read_root():
    return {"Hello": "Seattle!"}

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}