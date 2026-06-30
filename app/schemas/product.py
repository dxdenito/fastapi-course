from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Product name",
        examples=["Laptop", "Phone"],
    )
    price: float = Field(
        ..., gt=0, description="Price of the product", examples=[35000, 50000]
    )
    stock: int = Field(
        ..., ge=0, description="Number of units in stock", examples=[10, 20]
    )
    description: str | None = Field(
        None, max_length=300, description="Optional product description"
    )
    active: bool = Field(
        True, description="Whether the product is active", examples=[True, False]
    )
