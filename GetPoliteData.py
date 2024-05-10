import pandas as pd

df_comments = pd.read_csv('PoliteComments.csv')
df_emails = pd.read_csv('RawPoliteData.csv', encoding = 'latin')

has_comments: pd.Series = df_comments['Comment:'].notna()
df_comments.rename(columns={'Short description': 'Subject',
                            'Comment:':'Comment'},
                   inplace=True)
df_emails.rename(columns={'number': 'Number'},
                   inplace=True)
cleaned_data = df_comments[has_comments][['Number', 'Subject', 'Comment']]
cleaned_data.reindex()

merged = pd.merge(cleaned_data['Number'], df_emails, how='left', on='Number')


