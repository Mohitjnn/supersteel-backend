import os
from uuid import uuid4
from PIL import Image

# Base directory for static files
static = "static"


def save_picture(file, folderName: str = "", fileName: str = None):
    """
    Saves a picture to the specified folder with an optional custom filename.

    Args:
        file (UploadFile): The image file to be saved.
        folderName (str): The folder within the static directory where the image will be saved.
        fileName (str, optional): Custom filename for the image; if not provided, a random UUID is used.

    Returns:
        str: The relative path to the saved image.
    """
    # Generate a random unique ID for the filename or use the provided one
    random_uid = str(uuid4())
    _, f_ext = os.path.splitext(file.filename)

    # Construct the picture name with the correct file extension
    picture_name = (
        fileName.lower().replace(" ", "") if fileName else random_uid
    ) + f_ext

    # Create the full path to the save directory
    path = os.path.join(static, folderName)
    if not os.path.exists(path):
        os.makedirs(path)

    # Complete path for saving the image
    picture_path = os.path.join(path, picture_name)

    # Set the output size and save the image as a thumbnail
    output_size = (125, 125)
    try:
        img = Image.open(file.file)
        img.thumbnail(output_size)
        img.save(picture_path)
    except Exception as e:
        print(f"Error saving picture: {e}")
        return None

    # Return the relative path for database storage or further use
    return f"{static}/{folderName}/{picture_name}"


def delete_picture(image_path: str) -> bool:
    """
    Deletes an image file if the provided path exists.

    Args:
        image_path (str): The path to the image file to be deleted.

    Returns:
        bool: True if the image was successfully deleted, False otherwise.
    """
    # Convert to absolute path for deletion
    abs_image_path = os.path.abspath(image_path)

    try:
        # Check if the image exists and attempt to delete
        if os.path.exists(abs_image_path):
            os.remove(abs_image_path)
            print(f"Deleted: {abs_image_path}")
            return True
        else:
            print(f"File not found: {abs_image_path}")
            return False
    except Exception as e:
        # Log the error if deletion fails
        print(f"Error deleting file: {e}")
        return False
