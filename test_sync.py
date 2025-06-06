import tempfile
from pathlib import Path
import shutil
from sync import synchronize_directories, determine_actions


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


class TestE2E:
    @staticmethod
    def test_when_a_file_exists_in_the_source_but_not_in_the_destination_fake_file_system():
        source = {"sha1": "my-file"}
        destination = {}
        file_system = FakeFileSystem()
        read_files_and_hashes_func = {
            "/source": source,
            "/destination": destination,
        }.pop

        synchronize_directories(
            "/source", "/destination", read_files_and_hashes_func, file_system
        )

        assert file_system.list == [
            ("COPY", Path("/source/my-file"), Path("/destination/my-file"))
        ]

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source_fake_file_system():
        source = {"sha1": "my-file-renamed"}
        destination = {"sha1": "my-file"}
        file_system = FakeFileSystem()
        read_files_and_hashes_func = {
            "/source": source,
            "/destination": destination,
        }.pop

        synchronize_directories(
            "/source", "/destination", read_files_and_hashes_func, file_system
        )

        assert file_system.list == [
            ("MOVE", Path("/destination/my-file"), Path("/destination/my-file-renamed"))
        ]

    @staticmethod
    def test_when_a_file_exists_in_the_source_but_not_in_the_destination():
        source = tempfile.mkdtemp()
        destination = tempfile.mkdtemp()
        try:
            content = "I am a very important file."
            (Path(source) / "file1.txt").write_text(content)

            synchronize_directories(source, destination)

            expected_path = Path(destination) / "file1.txt"
            assert expected_path.exists()
            assert expected_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(destination)

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source():
        source = tempfile.mkdtemp()
        destination = tempfile.mkdtemp()
        try:
            content = "I am a file that has been renamed."
            source_path = Path(source) / "my-file-renamed.txt"
            old_destination_path = Path(destination) / "file1.txt"
            expected_destination_path = Path(destination) / "my-file-renamed.txt"
            source_path.write_text(content)
            old_destination_path.write_text(content)

            synchronize_directories(source, destination)

            assert old_destination_path.exists() is False
            assert expected_destination_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(destination)


def test_when_a_file_exists_in_the_source_but_not_in_the_destination():
    src_hashes = {"hash1": "file1.txt"}
    dest_hashes = {}

    actions = determine_actions(
        src_hashes, dest_hashes, Path("/source"), Path("/destination")
    )

    assert list(actions) == [
        ("COPY", Path("/source/file1.txt"), Path("/destination/file1.txt"))
    ]


def test_when_a_file_exists_in_the_destination_but_not_in_the_source():
    src_hashes = {}
    dest_hashes = {"hash1": "file1.txt"}

    actions = determine_actions(
        src_hashes, dest_hashes, Path("/source"), Path("/destination")
    )

    assert list(actions) == [("DELETE", Path("/destination/file1.txt"))]


def test_when_a_file_has_been_renamed_in_the_source():
    src_hashes = {"hash1": "file_1.txt"}
    dest_hashes = {"hash1": "file1.txt"}

    actions = determine_actions(
        src_hashes, dest_hashes, Path("/source"), Path("/destination")
    )

    assert list(actions) == [
        ("MOVE", Path("/destination/file1.txt"), Path("/destination/file_1.txt"))
    ]
