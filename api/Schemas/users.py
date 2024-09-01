# serializers.py

from api.models.products import Color  # Adjust as per your models


def colorEntity(color: Color) -> dict:
    return {
        "name": color.name,
        "hexCode": color.hexCode,
        "material": color.material,
        "weight": color.weight,
        "details": color.details,
    }


def productEntity(item) -> dict:
    # Assuming 'colors' is a list of Color objects
    colors = item.get("colors", [])
    if colors and isinstance(colors[0], Color):
        colors = [colorEntity(color) for color in colors]

    return {
        "id": str(item["_id"]),
        "name": item.get("name"),
        "description": item.get("description"),
        "price": item.get("price"),
        "quantity": item.get("quantity"),
        "category": item.get("category"),
        "imageUrl": item.get("imageUrl"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "isActive": item.get("isActive", False),
        "colors": colors,  # Including serialized colors
    }


def productsEntity(entities) -> list:
    return [productEntity(item) for item in entities]
