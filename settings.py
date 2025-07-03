from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
ROOT = ROOT.relative_to(Path.cwd())

# Source
IMAGE = 'Image'
WEBCAM = 'Webcam'
SOURCES_LIST = [IMAGE, WEBCAM]

# Images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'tomat11.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'tomat22.jpg'

# Model
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'mytomat.pt'

# Webcam
WEBCAM_PATH = 0
