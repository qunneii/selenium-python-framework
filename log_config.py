import logging
import os
from datetime import datetime

class LogConfig:
    
    @staticmethod
    def setup_logger(name="TestAutomation"):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if logger.handlers:
            logger.handlers.clear()

        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s',
            datefmt='%H:%M:%S'
        )

        log_filename = f"{log_dir}/test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.info("=" * 80)
        logger.info("Logger initialized successfully")
        logger.info(f"Log file: {log_filename}")
        logger.info("=" * 80)
        
        return logger