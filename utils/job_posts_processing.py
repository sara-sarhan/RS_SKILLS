import os
import pandas as pd
from utils.constants import Constants
import re
import unidecode
from utils.cross_functions import CrossFunctions

import warnings

warnings.filterwarnings("ignore")


class JobPostsProcessing:

    def __init__(self, filename=""):
        if filename == "":
            if "ita_job_posts_processed.csv" in os.listdir(os.path.join(os.getcwd(), "dataset")):
                self.processed_dataset = pd.read_csv(os.path.join(os.getcwd(), "dataset", "ita_job_posts.csv"), sep=";")
            else:
                self.processed_dataset = self.processing_text(self.load_dataset(
                    os.path.join(os.path.join(os.getcwd(), "dataset"), Constants.ita_job_posts_filename)))
        else:
            self.processed_dataset = self.processing_text(self.add_dataset(filename))

    def load_dataset(self, internal_filename_path):
        dataset_internal_folder = os.listdir(os.path.join(os.getcwd(), "dataset"))
        if Constants.ita_job_posts_filename in dataset_internal_folder:
            dataset = pd.read_csv(
                internal_filename_path, sep=";",
                encoding="utf-8")

            return dataset
        else:
            return None

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def add_dataset(self, filename_path) -> pd.DataFrame:
        dataset_internal_folder = os.path.join(os.getcwd(), "dataset")
        if isinstance(filename_path, str) and filename_path != "":

            os.rename(filename_path, os.path.join(dataset_internal_folder, Constants.ita_job_posts_filename))

            ita_job_posts_dataset = pd.read_csv(os.path.join(dataset_internal_folder, Constants.ita_job_posts_filename),
                                                sep=";",
                                                encoding="utf-8")

            if JobPostsProcessing.__check_dataset_fields(ita_job_posts_dataset):
                return ita_job_posts_dataset

            else:
                return pd.DataFrame()

        else:
            return pd.DataFrame()

    @staticmethod
    def __check_dataset_fields(ita_job_posts_dataset) -> bool:
        dataset_columns = ita_job_posts_dataset.columns
        n_columns_contained = set(dataset_columns).intersection(Constants.ita_job_posts_needed_columns)
        if len(n_columns_contained) < 2:
            return False
        return True

    @staticmethod
    def _change_html_chars(text):
        html_chars = pd.read_csv(os.path.join(os.getcwd(), "utils", "html_chars.csv"), sep=";")
        html_chars['Symbol'] = html_chars['Symbol'].apply(lambda x: x.strip())
        for i, row in html_chars.iterrows():
            text = text.replace(row['HTML'], row['Symbol'])
        return text

    @staticmethod
    def _replace_html(text):
        re_expression = '(<\w+>|</\w+>|\\n|<\w+/>|&quot;|http\S+|[-|0-9]|\*|,|;)'
        clean_text = re.sub(re_expression, ' ', text)
        ready_text = unidecode.unidecode(clean_text.lower())
        return ready_text

    def processing_text(self, dataset):
        dataset_txt = dataset[['jobTitle', 'jobDescription']]
        dataset_txt['jobDescription'] = dataset_txt['jobDescription'].map(JobPostsProcessing._replace_html)
        dataset_txt['jobDescription'] = dataset_txt['jobDescription'].map(JobPostsProcessing._change_html_chars)
        dataset_txt['All'] = dataset_txt['jobTitle'] + ' ' + dataset_txt['jobDescription']
        dataset_txt['All_Clean'] = dataset_txt['All'].apply(CrossFunctions.normalize, lowercase=True,
                                                            remove_stopwords=True)
        dataset_txt.to_csv(os.path.join(os.getcwd(), "dataset", "ita_job_posts_processed.csv"), sep=";", encoding = "utf-8")
        return dataset_txt['All_Clean']
