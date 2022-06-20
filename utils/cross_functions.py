import pandas as pd
import spacy
from nltk.corpus import stopwords
import numpy as np
import re
class CrossFunctions:
    nlp = spacy.load("it_core_news_lg", disable=['parser', 'tagger', 'ner'])
    stops = stopwords.words("italian")

    @staticmethod
    def get_recommendation(top, df_all, scores, jobtitle, scoresd, scoress, list_score_time):
        recommendation = pd.DataFrame(
            columns=['job user', 'jobID', 'jobCompany', 'jobTitle', 'scoreFinal', 'scoreDom', 'scoreSkills',
                     'scoreTime'])
        # ['job user','jobID', 'jobTitle', 'jobLocation', 'jobDescription', 'jobSalary', 'jobIndustry', 'jobSector', 'score']
        count = 0
        df_all['jobTitle'] = df_all['jobTitle'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip().lower())
        for i in top:
            recommendation.at[count, 'job user'] = ";".join(jobtitle)
            recommendation.at[count, 'jobID'] = i
            recommendation.at[count, 'jobCompany'] = df_all.iloc[i]['company']
            recommendation.at[count, 'jobTitle'] = df_all.iloc[i]['jobTitle']
            recommendation.at[count, 'scoreFinal'] = scores[count]
            recommendation.at[count, 'scoreDom'] = scoresd[count]
            recommendation.at[count, 'scoreSkills'] = scoress[count]
            recommendation.at[count, 'scoreTime'] = list_score_time[count]
            # recommendation.at[count, 'jobLocation'] = df_all.iloc[i]['location']
            # recommendation.at[count, 'jobDescription'] = df_all.iloc[i]['jobDescription']
            # recommendation.at[count, 'jobSalary'] = df_all.iloc[i]['salary']
            # recommendation.at[count, 'jobIndustry'] = df_all.iloc[i]['Domain']

            count += 1
        # recommendation= recommendation.reset_index(drop=True, inplace=True)
        # recommendation['scoreFinal']= recommendation['scoreFinal'].apply(lambda   x:np.ceil(x)*100)
        # recommendation['scoreDom']= recommendation['scoreDom'].apply(lambda   x:np.ceil(x)*100)
        # recommendation['scoreSkills']= recommendation['scoreSkills'].apply(lambda   x:np.ceil(x)*100)
        # recommendation['scoreTime']= recommendation['scoreTime'].apply(lambda   x:np.ceil(x)*100)
        return recommendation

    @staticmethod
    def normalize(comment, lowercase, remove_stopwords):
        if lowercase:
            comment = comment.lower()
        comment = CrossFunctions.nlp(comment)
        lemmatized = list()
        for word in comment:
            if not word.is_punct:
                lemma = word.lemma_.strip()
                if lemma:
                    if not remove_stopwords or (remove_stopwords and lemma not in CrossFunctions.stops):
                        lemmatized.append(lemma)
        return " ".join(lemmatized)
