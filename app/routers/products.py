from fastapi import APIRouter

from app.schemas.product import Product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_id}")
def get_product(product_id: int):
    return {"id": product_id, "name": "Sample Product"}


@router.post("/")
def create_product(product: Product):
    return {"product": product, "message": "Product created successfully"}


@router.put("/{product_id}")
def update_product(product_id: int, product: Product, notify: bool = False):
    return {"product_id": product_id, "product": product, "notify": notify}


@router.delete("/{product_id}")
def delete_product(product_id: int):
    return {"message": f"Product {product_id} deleted", "success": True}
