from PIL import Image

def split_image(image_path, num_chunks):
    """Split an image into smaller chunks."""
    image = Image.open(image_path)
    width, height = image.size
    chunk_width = width // num_chunks
    chunks = [image.crop((i*chunk_width, 0, (i+1)*chunk_width, height)) for i in range(num_chunks)]
    return chunks

def merge_image(chunks):
    """Merge processed image chunks back into the final image."""
    widths, heights = zip(*(i.size for i in chunks))
    total_width = sum(widths)
    max_height = max(heights)

    final_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for chunk in chunks:
        final_image.paste(chunk, (x_offset, 0))
        x_offset += chunk.width
    return final_image
