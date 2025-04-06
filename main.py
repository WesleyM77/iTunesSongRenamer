from tinytag import TinyTag
import os
from pathlib import Path
import shutil
from tqdm import tqdm


forbidden_characters = '.?:!*,"<>/\\'
base_dir = os.path.join('Insert path here')


def treat_string(string: str) -> str:
    string = string.strip()
    for char in forbidden_characters:
        string = string.replace(char, '')
    return string


def rename_song(song_path: str):
    tag: TinyTag = TinyTag.get(song_path)
    artist = tag.artist\
        .strip()\
        .rstrip(forbidden_characters)\
        .replace('"', "")
    album = tag.album
    title = tag.title

    if isinstance(album, str):
        album = treat_string(album)
    if album is None or album == '':
        album = 'album unknown'
    if isinstance(title, str):
        title = treat_string(title)
    if title is None or title == '':
        title = 'unknown song ' + Path(song_path).stem

    song_extension = Path(song_path).suffix

    destination = os.path.join(base_dir, 'output', artist)
    destination = os.path.join(destination, album)

    original_filename_only = os.path.basename(song_path)
    original_filename = destination + os.path.sep + original_filename_only
    new_filename = destination + os.path.sep + title + song_extension

    if not os.path.isfile(new_filename):
        Path(destination).mkdir(parents=True, exist_ok=True)
        shutil.copy2(song_path, destination)
        os.rename(original_filename, new_filename)


input_path = os.path.join(base_dir, 'input')
folders = os.listdir(input_path)
file_extensions = []

songs_migrated = 0

for folder in folders:
    folder_path = os.path.join(input_path, folder)
    song_filenames = os.listdir(folder_path)
    for song_filename in tqdm(song_filenames, desc="Migrating folder: " + folder):
        song_path = os.path.join(folder_path, song_filename)
        try:
            rename_song(song_path)
            songs_migrated = songs_migrated + 1
        except Exception as e:
            print('Failed to migrate ' + song_path + ' - ' + e)
            exit()

print(str(songs_migrated) + " songs migrated")