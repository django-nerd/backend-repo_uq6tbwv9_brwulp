"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Product(BaseModel):
    """
    Seafood products available for export
    Collection name: "product"
    """
    name: str = Field(..., description="Product name, e.g., Pacific White Shrimp")
    category: str = Field(..., description="Category, e.g., Shrimp, Fish, Crab, Lobster")
    origin: Optional[str] = Field(None, description="Country/region of origin")
    grade: Optional[str] = Field(None, description="Quality grade or specification")
    processing: Optional[str] = Field(None, description="Processing type, e.g., IQF, HOSO, HLSO, Fillet")
    sizes: Optional[List[str]] = Field(default=None, description="Available sizes, e.g., 16/20, 21/25")
    packaging: Optional[str] = Field(None, description="Packaging details, e.g., 10x1kg, 20kg master carton")
    availability: Optional[str] = Field(None, description="Seasonality or stock status")

class Inquiry(BaseModel):
    """
    Buyer inquiries and RFQs from the website
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Buyer full name")
    company: Optional[str] = Field(None, description="Company name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone or WhatsApp")
    country: Optional[str] = Field(None, description="Buyer country")
    product_interest: Optional[str] = Field(None, description="Product(s) of interest")
    message: str = Field(..., description="Message or specifications")
    quantity_mt: Optional[float] = Field(None, ge=0, description="Estimated quantity in metric tons")
    incoterm: Optional[str] = Field(None, description="Preferred Incoterm, e.g., FOB, CIF")

# Example schema kept for reference
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = None
    is_active: bool = True
