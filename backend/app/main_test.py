from fastapi import FastAPI
import asyncio

print("Creating app")
app = FastAPI()
print("App created")

@app.get("/")
async def root():
    print("Handling request")
    try:
        return {"message": "Go Buhat API"}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

print("App setup complete")