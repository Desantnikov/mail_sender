import os
import glob


class FilesSequence:
    def __init__(self, folder, files_template='*'):
        self.files = list(map(os.path.abspath, glob.glob(f'{folder}/{files_template}')))
        self.folder = folder

    def __str__(self):
        return '\r\n'.join([f'{index}: {file}' for index, file in enumerate(self.get_basenames())])

    def __len__(self):
        return len(self.files)

    def __iter__(self):
        return iter(self.files)

    def get_basenames(self):
        return map(os.path.basename, self.files)

    def reorder_files(self, current_index: int, new_index: int):
        file_to_move = self.files.pop(current_index)
        self.files.insert(new_index, file_to_move)

        # print(f'File {file_to_move} was moved from {current_index} to {new_index}')

