from fastapi import FastAPI

app = FastAPI(title="Authentication Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth_service"}

@app.get("/")
async def root():
    return {"message": "Auth service is running"}
