import pandas as pd

from classes.files_sequence import FilesSequence


class EmailFilesSequence(FilesSequence):
    EMAIL_REGEXP = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    EMAIL_COLUMN_NAME = 'Email'
    SKIP_ROWS = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.emails_df = self._get_emails_df()

    def _get_emails_df(self):
        excel_df_list = [pd.read_excel(file, skiprows=self.SKIP_ROWS,
                                       usecols=[self.EMAIL_COLUMN_NAME]).dropna() for file in self.paths_list]

        emails_df = pd.concat(excel_df_list).drop_duplicates().reset_index(drop=True)

        emails_df['Email'] = emails_df['Email'][emails_df['Email'].str.contains(self.EMAIL_REGEXP)]

        self.logger.info(f'Number of unique emails in all {len(self)} files: {len(emails_df)}')

        return emails_df
