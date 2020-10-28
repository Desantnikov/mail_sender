import glob


class FilesSequence:
    def __init__(self, folder):
        self.files = glob.glob(f'{folder}/*.xlsx')

    def __str__(self):
        return '\r\n'.join([f'{index}: {file}' for index, file in enumerate(self.files)])

    def __iter__(self):
        return iter(self.files)

    def reorder_files(self, current_index: int, new_index: int):
        file_to_move = self.files.pop(current_index)
        self.files.insert(new_index, file_to_move)

        # print(f'File {file_to_move} was moved from {current_index} to {new_index}')

