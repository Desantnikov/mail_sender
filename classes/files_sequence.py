import logging
import os
import glob


class FilesSequence:
    def __init__(self, folder, files_template='*', reorder_on_creation=True, logger=logging.getLogger('FilesSequence')):
        self.logger = logger

        self.paths_list = list(map(os.path.abspath, glob.glob(f'{folder}/{files_template}')))
        self.folder = folder

        if reorder_on_creation:
            self.reorder_files()

        self.logger.info(f'FilesSequence created from folder {self.folder}\nFiles: {self}')

    def __str__(self):
        return '\n'.join([f'{index}: {file}' for index, file in enumerate(self.get_basenames())])

    def __len__(self):
        return len(self.paths_list)

    def __iter__(self):
        return iter(self.paths_list)

    def get_basenames(self):
        return list(map(os.path.basename, self.paths_list))

    def reorder_files(self):
        while True:
            print(f'\r\nПоследовательность файлов из папки {self.folder}:\r\n{self}\r\n')
            initial_position = input('Если хотите передвинуть файл - введите его номер и нажмите энтер.\r\n'
                                     'Если текущий порядок устраивает - просто нажмите энтер.\r\n')
            if not initial_position:
                break

            new_position = input('Введите на какую позицию хотите передвинуть файл:\r\n')
            try:
                self._swap_files(current_index=int(initial_position), new_index=int(new_position))
            except IndexError:
                print('Неправильный ввод, повторите снова.\r\n')

    def _swap_files(self, current_index: int, new_index: int):
        file_to_move = self.paths_list.pop(current_index)
        self.paths_list.insert(new_index, file_to_move)

        # print(f'File {file_to_move} was moved from {current_index} to {new_index}')


