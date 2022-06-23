import pandas as pd
import spacy
from nltk.corpus import stopwords
import re

class CrossFunctions:
    nlp = spacy.load("it_core_news_lg", disable=['parser', 'tagger', 'ner'])
    stops = stopwords.words("italian")

    @staticmethod
    def get_recommendation(top, df_all, scores, jobtitle, scoresd, scoress, list_score_time,company):
        recommendation = pd.DataFrame(
            columns=['job user','company user', 'jobID', 'jobCompany', 'jobTitle', 'jobDescription', 'scoreFinal', 'scoreDom', 'scoreSkills',
                     'scoreTime'])
        # ['job user','jobID', 'jobTitle', 'jobLocation', 'jobDescription', 'jobSalary', 'jobIndustry', 'jobSector', 'score']
        count = 0
        df_all['jobTitle'] = df_all['jobTitle'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip().lower())
        for i in top:
            recommendation.at[count, 'job user'] = ";".join(jobtitle)
            recommendation.at[count, 'company user'] = company
            recommendation.at[count, 'jobID'] = i
            recommendation.at[count, 'jobCompany'] = df_all.iloc[i]['company']
            recommendation.at[count, 'jobTitle'] = df_all.iloc[i]['jobTitle']
            recommendation.at[count, 'jobDescription'] = df_all.iloc[i]['jobDescription']
            recommendation.at[count, 'scoreFinal'] = scores[count]
            recommendation.at[count, 'scoreDom'] = scoresd[count]
            recommendation.at[count, 'scoreSkills'] = scoress[count]
            recommendation.at[count, 'scoreTime'] = list_score_time[count]
            # recommendation.at[count, 'jobLocation'] = df_all.iloc[i]['location']

            # recommendation.at[count, 'jobSalary'] = df_all.iloc[i]['salary']
            # recommendation.at[count, 'jobIndustry'] = df_all.iloc[i]['Domain']

            count += 1

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
