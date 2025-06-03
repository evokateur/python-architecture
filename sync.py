import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE = 65536


class RealFileSystem:
    def copy(self, source, destination):
        shutil.copyfile(source, destination)

    def move(self, source, destination):
        shutil.move(source, destination)

    def delete(self, path):
        os.remove(path)


class FakeFileSystem:
    def __init__(self):
        self._list = []

    def copy(self, source, destination):
        self._list.append(("COPY", source, destination))

    def move(self, source, destination):
        self._list.append(("MOVE", source, destination))

    def delete(self, path):
        self._list.append(("DELETE", path))

    @property
    def list(self):
        return self._list


def hash_file(file_path):
    hasher = hashlib.sha1()
    with Path.open(file_path, "rb") as f:
        buffer = f.read(BLOCKSIZE)
        while buffer:
            hasher.update(buffer)
            buffer = f.read(BLOCKSIZE)

    return hasher.hexdigest()


def read_files_and_hashes(directory):
    source_hashes = {}
    for folder, _, files in os.walk(directory):
        for file in files:
            source_hashes[hash_file(Path(folder) / file)] = file

    return source_hashes


def determine_actions(
    source_hashes, destination_hashes, source_directory, destination_directory
):
    for sha, file_name in source_hashes.items():
        if sha not in destination_hashes:
            source_path = Path(source_directory) / file_name
            destination_path = Path(destination_directory) / file_name
            yield "COPY", source_path, destination_path

        elif destination_hashes.get(sha) != file_name:
            old_destination_path = Path(destination_directory) / destination_hashes[sha]
            new_destination_path = Path(destination_directory) / file_name
            yield "MOVE", old_destination_path, new_destination_path

    for sha, file_name in destination_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", Path(destination_directory) / file_name


def synchronize_directories(
    source_directory,
    destination_directory,
    read_files_and_hashes_func=read_files_and_hashes,
    file_system=None,
):
    source_hashes = read_files_and_hashes_func(source_directory)
    destination_hashes = read_files_and_hashes_func(destination_directory)
    actions = determine_actions(
        source_hashes, destination_hashes, source_directory, destination_directory
    )

    if file_system is None:
        file_system = RealFileSystem()

    for action, *paths in actions:
        if action == "COPY":
            file_system.copy(*paths)
        elif action == "MOVE":
            file_system.move(*paths)
        elif action == "DELETE":
            file_system.delete(paths[0])
        else:
            raise ValueError(f"Unknown action: {action}")
