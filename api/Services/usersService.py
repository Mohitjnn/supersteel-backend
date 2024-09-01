from bson import ObjectId
from api.config.db import db
from api.models.products import CreateProduct  # Adjusted to match the product model
from api.Schemas.serializeObjects import serializeDict, serializeList
from api.helpers.save_picture import delete_picture
import shutil
import os


async def getAllProducts() -> list:
    # Fetches all products from the database
    return serializeList(db.products.find())


async def getById(id) -> dict:
    # Fetches a single product by ID
    return serializeDict(db.products.find_one({"_id": ObjectId(id)}))


async def insertProduct(data: CreateProduct) -> dict:
    # Convert the data to a dictionary including nested models
    product_data = dict(data)
    product_data["colors"] = [dict(color) for color in data.colors]
    product_data["images"] = [dict(image) for image in data.images]

    # Inserts a new product into the database
    result = db.products.insert_one(product_data)
    return serializeDict(db.products.find_one({"_id": ObjectId(result.inserted_id)}))


async def updateProduct(id, data: CreateProduct) -> bool:
    # Updates an existing product in the database
    db.products.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
    return True


async def saveProductImage(id, color: str, imageUrl: str) -> bool:
    # Save image to the product's color-specific images
    product = db.products.find_one({"_id": ObjectId(id)})

    # If the product is found
    if product:
        # Add or update the image for the specified color
        images = product.get("images", [])
        # Check if the color already exists in images
        existing_image = next((img for img in images if img["color"] == color), None)

        if existing_image:
            # Update the existing image
            existing_image["imageSrc"] = imageUrl
        else:
            # Add a new image entry
            images.append({"color": color, "imageSrc": imageUrl})

        # Update the product in the database
        db.products.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {"images": images}}
        )
        return True

    return False


async def deleteProduct(id) -> bool:
    # Find the product by id and retrieve associated image paths
    product = db.products.find_one({"_id": ObjectId(id)})

    if product:
        # Get the folder path
        folder_path = f"static/products/{id}"

        # Iterate through images and delete each one using delete_picture
        images = product.get("images", [])
        for image in images:
            image_path = image.get("imageSrc")
            if image_path:
                delete_picture(image_path)

        # Delete the entire folder
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Delete the product from the database
        db.products.find_one_and_delete({"_id": ObjectId(id)})
        return True

    # If product not found, return False
    return False
