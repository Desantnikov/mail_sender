import glob


class FilesSequence:
    def __init__(self, folder):
        self.excel_files = glob.glob(f'{folder}/*.xlsx')

        # print(f'Найдены файлы: {"; ".join(self.excel_files)}')

    def __str__(self):
        return '\r\n'.join([f'{index}: {file}' for index, file in enumerate(self.excel_files)])

    def reorder_files(self, current_index: int, new_index: int):
        file_to_move = self.excel_files.pop(current_index)
        self.excel_files.insert(new_index, file_to_move)

        print(f'File {file_to_move} was moved from {current_index} to {new_index}')