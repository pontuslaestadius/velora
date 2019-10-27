import pytesseract

from PIL import Image

def get_text(image):
  """Retrieves possible text from IMAGE."""

  try:
    return pytesseract.image_to_string(image, lang='eng')
  except Exception as e:
    pass
