import os
import warnings
warnings.filterwarnings("ignore")
from extraction_skills import skills_extraction


def main(pdfnamepath, folder):
    print("folder....", folder)
    Clss_skills = skills_extraction(pdfnamepath, os.path.join(os.getcwd(), "model", 'cc.it.300.bin'), folder)

    rs = Clss_skills.pdf_to_html()
    # rs=Clss_skills.raccomandetion(job,test)

    return rs
