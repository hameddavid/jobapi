key = b'tIhLBaAgcxcrAKJmNNDdzOfXcQvUAbIEWg7eLweK3MQ='   #will later read this off from a db
def image_to_base64(image_path):
    try:
        from PIL import Image
        import base64
        from io import BytesIO
        from django.conf import settings
        import os
		# Construct the absolute path to the folder
        image_path = os.path.join(settings.BASE_DIR, image_path)
        # Open the image file
        with open(image_path, 'rb') as image_file:
            # Read the image file
            image_data = image_file.read()
            # Encode the image data to base64
            base64_encoded = base64.b64encode(image_data).decode('utf-8')          
            return f"data:image/jpeg;base64,{base64_encoded}"
    except Exception as e:
        # Handle exceptions (e.g., file not found, etc.) based on your project's requirements
        print(f"Error: {e}")
        return None
# Example usage:
image_path = 'images/product_image_default.jpg' 
