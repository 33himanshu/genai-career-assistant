import os
from datetime import datetime
from app.config import OUTPUT_FOLDER

def save_file(content: str, filename: str, extension: str = "md") -> str:
    """Save content to a file and return the file path.
    
    Args:
        content: The content to save
        filename: The base filename
        extension: The file extension (default: md)
        
    Returns:
        The path to the saved file
    """
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{filename}_{timestamp}.{extension}"
    file_path = os.path.join(OUTPUT_FOLDER, safe_filename)
    
    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path


