import uvicorn
import os
import sys
sys.path.append(os.path.dirname(__file__))
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)