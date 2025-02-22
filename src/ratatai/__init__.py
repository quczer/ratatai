import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(levelname)-7s: %(message)s", datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
