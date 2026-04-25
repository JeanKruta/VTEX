import pandas as pd


class PreprocessingPipeline:
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.select_relevant_columns(df)
        df = self.filter_valid_categories(df)
        df = self.drop_nulls(df)
        df = self.normalize_text(df)
        df = self.remove_duplicates(df)
        return df

    def select_relevant_columns(self, df):
        return df[['question', 'content', 'data_category_QA']]

    def filter_valid_categories(self, df):
        return df[df['data_category_QA'].isin(['positivo', 'negativo'])]

    def drop_nulls(self, df):
        return df.dropna(subset=['question', 'content'])

    def normalize_text(self, df):
        df = df.copy()
        df['question'] = df['question'].str.strip()
        df['content'] = df['content'].str.strip()
        return df

    def create_normalized_keys(self, df):
        df = df.copy()
        df['question_norm'] = df['question'].str.lower()
        df['content_norm'] = df['content'].str.lower()
        return df

    def remove_duplicates(self, df):
        df = self.create_normalized_keys(df)
        df = df.drop_duplicates(subset=['question_norm', 'content_norm'])
        df = df.drop(columns=['question_norm', 'content_norm'])
        return df.reset_index(drop=True)