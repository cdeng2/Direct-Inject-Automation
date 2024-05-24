import pandas as pd
# Given the two csv's below, this generates a new csv of the task num, subject line, email body, and comment

# PoliteComments contants emails with the short summarized comments
# RawPoliteData contains the description body of each email
df_comments = pd.read_csv('PoliteComments.csv')
df_emails = pd.read_csv('RawPoliteData.csv', encoding = 'latin')

# Cleaning: Removes Nan, renames columns
has_comments: pd.Series = df_comments['Comment:'].notna()
df_comments.rename(columns={'Short description': 'Subject', 
                            'Comment:': 'Comment'}, inplace=True)
cleaned_data = df_comments[has_comments][['Number', 'Subject', 'Comment']]
df_emails.rename(columns={'number': 'Number', 'description': 'Description'}, 
                 inplace=True)

# Cleaning: Removes \n from des., remove Subject prefix and suffix
df_emails['description'] = df_emails['description'].apply(
    lambda x: x.replace('\n', ' '))
# IMPLEMENT SUBJECT REMOVAL

# Merges the descriptions to cleaned_data
merged = pd.merge(cleaned_data, df_emails[['Number', 'description']], how='left', 
                  on='Number')
merged.to_csv('CleanedPolite.csv', index=False)


