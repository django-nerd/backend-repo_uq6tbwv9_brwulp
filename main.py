import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Product, Inquiry

app = FastAPI(title="Seafood Exporter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Seafood Exporter Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Public catalog endpoints
@app.get("/api/products", response_model=List[Product])
def list_products(category: Optional[str] = None):
    """List seafood products, optionally filtered by category"""
    filter_q = {"category": category} if category else {}
    try:
        docs = get_documents("product", filter_q)
        # Remove Mongo-specific fields
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception:
        # Return sample data if DB not configured
        sample = [
            Product(name="Pacific White Shrimp", category="Shrimp", origin="Ecuador", grade="A", processing="HOSO", sizes=["16/20", "21/25"], packaging="10x1kg", availability="Year-round").model_dump(),
            Product(name="Yellowfin Tuna", category="Fish", origin="Sri Lanka", grade="Sashimi", processing="Loins", sizes=["2-5kg", "5-8kg"], packaging="Vacuum packed", availability="Seasonal").model_dump(),
        ]
        return sample

class InquiryResponse(BaseModel):
    id: str
    status: str

@app.post("/api/inquiries", response_model=InquiryResponse)
def create_inquiry(inquiry: Inquiry):
    """Create a buyer inquiry (RFQ)"""
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"id": inserted_id, "status": "received"}
    except Exception:
        # Fallback when DB is not configured: acknowledge receipt without storing
        return {"id": "temp", "status": "received"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
