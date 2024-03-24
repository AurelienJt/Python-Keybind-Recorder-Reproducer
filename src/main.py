# pylint: disable=no-member
# pylint: disable=missing-module-docstring
import json
import sys
import os
from datetime import datetime
import pygame



class KeybindReplicator:
    """Class to generate scripts replicating recorded keybinds"""

    def __init__(self):
        self._dir_pth = os.path.dirname(os.path.abspath(__file__))
        self._pyblock_pth = os.path.join(self._dir_pth, "Data", "pyblocks.json")
        self._trascriber_pth = os.path.join(
            self._dir_pth, "Data", "pygame2pyau_transcription.json"
        )
        self._window_dimensions: tuple[int, int] = (300, 200)
        self._window_title: str = "Recording..."
        self._window_screen: pygame.Surface = pygame.display.set_mode(
            self._window_dimensions
        )
        pygame.display.set_caption(self._window_title)
        self._destination_path: str = self._handle_cli_args()
        self._insertion_index: int = 10
        self._code_blocks: list = self._load_from_json(self._pyblock_pth)
        self._transcription_table: dict = self._load_from_json(self._trascriber_pth)
        self._target_keys: list = self._keybind_tracker()
        self._generate_code()
        self.dump_to_file(self._handle_cli_args())

    def __repr__(self) -> str:
        _newline = "\n"
        return f"Current code:\n{_newline.join(self._code_blocks)}"

    def _load_from_json(self, _path: str):
        with open(_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _handle_cli_args(self) -> str:
        if len(sys.argv) == 1:
            return ""
        if sys.argv[1] == "help":
            print("Run with: python main.py <filepath>")
            sys.exit()
        return sys.argv[1]

    def _keybind_tracker(self) -> list[tuple[str, str]]:
        """Tracks key inputs while active. Stop recording with esc or by closing the pygame window.

        Returns
        -------
        list
            The tracked keys.
        """
        pygame.init()
        key_identifier: dict = {"up": "up", "down": "down"}
        _used_keys: list = []
        _tracking: bool = True
        print(
            (
                "Tracking...please make sure pygame window is selected. "
                "Press escape or close the window to stop recording."
            )
        )
        while _tracking:
            self._window_handler()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _tracking = False
                    self._window_closer()
                    continue

                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            _tracking = False
                            self._window_closer()
                            continue
                        identifier = key_identifier["down"]
                    elif event.type == pygame.KEYUP:
                        identifier = key_identifier["up"]
                    _used_keys.append(
                        (identifier, pygame.key.name(event.key), event.key)
                    )
        return _used_keys

    def _window_handler(self) -> None:
        pygame.display.flip()

    def _window_closer(self) -> None:
        pygame.display.quit()
        pygame.quit()

    def _insert_list_at_index(
        self, index: int, _dest_list: list, _tar_list: list
    ) -> list:
        """Joins and flattens two lists at a specific index.

        Parameters
        ----------
        index : int
            The desired index for the merge.
        dest_list : list
            Destination list.
        tar_list : list
            Targeted list.

        Returns
        -------
        list
            The merged list.
        """
        for item in _tar_list[::-1]:
            _dest_list.insert(index, item)
        return _dest_list

    def _generate_code(self) -> None:
        _key_code: list = []
        if len(self._target_keys) == 0:
            raise ValueError("No keys detected, aborting.")
        self._target_keys = self._pygame2pyautogui(self._target_keys)
        for _key_event in self._target_keys:
            _key_code.append(self._key_event_handler(_key_event))
        self._code_blocks = self._insert_list_at_index(
            self._insertion_index, self._code_blocks, _key_code
        )

    def _key_event_handler(self, _key_event) -> str:
        match _key_event[0]:
            case "down":
                return self._key_down_event_code(_key_event)
            case "up":
                return self._key_up_event_code(_key_event)
        raise ValueError(f"Unsupported key_event: {_key_event}")

    def _key_down_event_code(self, _key_down_event) -> str:
        return f"pydirectinput.keyDown('{_key_down_event[1]}')"

    def _key_up_event_code(self, _key_up_event) -> str:
        return f"pydirectinput.keyUp('{_key_up_event[1]}')"

    def _pygame2pyautogui(self, pygame_keynames: list) -> list:
        _translated_keys: list = []
        for key_name in pygame_keynames:
            if self._transcription_table.get(key_name[1]) is not None:
                _translated_keys.append((key_name[0], self._transcription_table.get(key_name[1]), key_name[2]))
            else:
                raise ValueError(f"Missing translation for: {key_name}")
        return _translated_keys


    def _block2codes_str(self) -> str:
        _code_str = "\n"
        return _code_str.join(self._code_blocks)

    def _handle_file_path(self, file_path: str) -> str:
        if file_path == "abort":
            raise ValueError("Aborting.")
        if file_path == "":
            file_path = os.path.join("Recordings", datetime.now().strftime("%d_%m_%d-%H_%M_%S"))
        elif not file_path.startswith("Recordings"):
            file_path = os.path.join("Recordings", file_path)
        if "." not in file_path:
            file_path += ".pyw"
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except FileNotFoundError:
                pass
        return file_path

    def dump_to_file(self, file_path) -> str:
        """Generates a file with the code corresponding to the object.

        Parameters
        ----------
        file_path : str
            The path of file. If a file exists at this location, it will be surpressed.

        Returns
        -------
        str
            A str version of the code.
        """
        _file_path: str = self._handle_file_path(file_path)
        _code_str: str = self._block2codes_str()
        with open(_file_path, "w", encoding="utf-8") as file:
            file.write(_code_str)
        print(f"Created recordings file at: {_file_path}")
        return _code_str



if __name__ == "__main__":
    keybind_rep = KeybindReplicator()
