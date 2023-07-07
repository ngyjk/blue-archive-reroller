import logging
logger = logging.getLogger('ProjectBA')
from paddleocr import PaddleOCR
from PIL import Image
import time

logger.info('Starting OCR.')
ocr = PaddleOCR(show_log = False, use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
logger.info('OCR Model Loaded.')

def listener(image_func, phrases, interval = 5, init_delay = 0, limit = 60, lower = False, remove_whitespace = False, debug = True, mode = 'first'):

    if type(phrases) == str:
        phrases = [adjust_text(phrases)]
    else:
        phrases = [adjust_text(phrase) for phrase in phrases]

    logger.info(f'Identifying: {phrases}')

    times = 0
    if init_delay > 0:
        time.sleep(init_delay)

    while times < limit:
        image = image_func()
        results = get_all_text(image)
        results = [adjust_text(result) for result in results]

        logger.debug(f'Results: {results}')

        if mode == 'first':
            for phrase in phrases:
                if phrase in results:
                    logger.info(f'Identified: {phrase}')
                    return phrase

        if mode in ('all', 'partial_all'):
            found = []
            if mode == 'partial_all':
                results = ''.join(results)
            for phrase in phrases:
                if phrase in results:
                    logger.info(f'Identified: {phrase}')
                    found.append(phrase)
            logger.info(f'List of Identified: {found}')
            return found

        logger.info(f'Reran {times} times - not found')
        time.sleep(interval)
        times += 1

    return 'NA'

def get_all_text(image):

    texts = []
    results = ocr.ocr(image, cls=True)
    for result in results[0]:
        texts.append(result[1][0])
    return [text.strip() for text in texts]

def get_all_text_with_positions(image):
    texts = []
    results = ocr.ocr(image, cls=True)
    for result in results[0]:
        texts.append({'text': result[1][0], 'boxes': result[0]})
    return texts

def crop_image(open_path, save_path, left, top, right, bottom):
    im = Image.open(open_path)
    im = im.crop((left, top, right, bottom))
    im.save(save_path)

def adjust_text(text):
    text = text.lower()
    text = text.translate({ord(i): None for i in "().!? -'"})
    return text

class _ocr():
    
    def __init__(self, temp_path, adjust = True, debug = True):
        self.model = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
        self.temp_path = temp_path
        self.adjust = adjust
        self.debug = debug
        self.current_text = []
        self.current_text_with_positions = []

    def listener(self, phrases, interval = 5, init_delay = 0, limit = 60, mode = 'all'):

        if type(phrases) == str:
            phrases = [self.adjust_text(phrases)]
        else:
            phrases = [self.adjust_text(phrase) for phrase in phrases]
        times = 0

        if init_delay > 0:
            time.sleep(init_delay)

        while times < limit:
            results = self.set_current_text(self.temp_path)
            results = self.get_current_text(self.temp_path)
            results = [self.adjust_text(result) for result in results]

            if self.debug:
                print(f'Looking for {phrases}')
                print(f'Identified {results}')

            if mode == 'first':
                for phrase in phrases:
                    if phrase in results:
                        return phrase

            if mode == 'all':
                found = []
                for phrase in phrases:
                    if phrase in results:
                        found.append(phrase)
                return found

            print(f'Reran {times} times - not found')
            time.sleep(interval)
            times += 1

        return 'NA'

    def adjust_text(self, text):
        if self.adjust == True:
            text = text.lower()
            text = text.translate({ord(i): None for i in "().!? -'"})
        return text

    def get_current_text(self):
        return self.current_text
    
    def get_current_text_with_positions(self):
        return self.get_current_text_with_positions

    def set_current_text(self):
        texts = []
        results = self.model.ocr(self.temp_path, cls=True)
        for result in results[0]:
            texts.append(result[1][0])
        self.current_text = texts
    
    def set_current_text_with_positions(self):
        texts = []
        results = self.model.ocr(self.temp_path, cls=True)
        for result in results[0]:
            texts.append({'text': result[1][0], 'boxes': result[0]})
        self.current_text_with_positions = texts

    def crop_temp_path(self, left, top, right, bottom):
        im = Image.open(self.temp_path)
        im = im.crop((left, top, right, bottom))
        im.save(self.crop_temp_path)