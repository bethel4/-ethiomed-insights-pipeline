from fastapi import FastAPI, HTTPException
from typing import List
from . import crud
from .schemas import TopProductsResponse, ChannelActivity, MessageSearch

app = FastAPI(
    title="Ethiomed Insights API",
    description="Analytical API for Ethiopian medical business data from Telegram",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Ethiomed Insights API - Welcome!"}

@app.get("/api/reports/top-products", response_model=TopProductsResponse)
def get_top_products(limit: int = 10):
    """
    Get the most frequently mentioned medical products across all channels.
    """
    try:
        products = crud.get_top_products(limit)
        return TopProductsResponse(
            products=products,
            total_count=len(products)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
def get_channel_activity(channel_name: str):
    """
    Get posting activity for a specific channel.
    """
    try:
        return crud.get_channel_activity(channel_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/messages", response_model=List[MessageSearch])
def search_messages(query: str, limit: int = 10):
    """
    Search for messages containing a specific keyword.
    """
    try:
        return crud.search_messages(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "Ethiomed Insights API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 