from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from utils.cross_functions import CrossFunctions
import pandas as pd

import unicodedata


class ReadCV:

    def __init__(self, resume_path=""):

        if resume_path != "":
            self.resume_df = self._processing_resume_from_path(resume_path)

    def _processing_resume_from_path(self, resume_path):
        processed_resume_txt = []
        for page_layout in extract_pages(resume_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    section = element.get_text()
                    processed_resume_txt.append(
                        unicodedata.normalize('NFKD', section).encode('ascii', 'ignore').decode('utf-8').replace(
                            '\n', ' '))
        processed_resume_txt_stripped = [sentence.strip() for sentence in processed_resume_txt if
                                         sentence.strip() != ""]
        resume_txt = " ".join(processed_resume_txt_stripped)
        resume_txt_clean = CrossFunctions.normalize(resume_txt, lowercase=True, remove_stopwords=True)

        resume_dict = {'text': [resume_txt_clean]}
        df_resume = pd.DataFrame(data=resume_dict)

        return df_resume
