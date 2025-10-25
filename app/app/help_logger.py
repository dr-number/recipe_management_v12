import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(funcName)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("info.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

