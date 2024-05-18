from backend.server import app
from dotenv import load_dotenv # dotenv module to load environment variables from a .env file into os.environ
load_dotenv()

if __name__ == "__main__":
    import uvicorn
    """Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server implementation.
    It is designed to run asynchronous web applications using ASGI, which allows for the building of high-performance asyncio applications.
    It's particularly well-suited to running FastAPI applications.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)