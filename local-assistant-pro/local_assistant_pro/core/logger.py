from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False, enqueue=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>")
