import json
import os
import pygame


def keybind_tracker() -> list[tuple[str, str]]:
    """Tracks keybind inputs while active. Escape tracking with esc.

    Returns
    -------
    list
        The tracked keys.
    """
    pygame.init()
    key_identifier: dict = {"up": "up", "down": "down"}
    used_keys: list = []
    tracking: bool = True
    while tracking:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        tracking = False
                        continue
                    identifier = key_identifier["down"]
                elif event.type == pygame.KEYUP:
                    print(event)
                    identifier = key_identifier["up"]
                used_keys.append((identifier, pygame.key.name(event.key), event.key))
    return used_keys


def insert_list_at_index(index: int, dest_list: list, tar_list: list) -> list:
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
    for item in tar_list[::-1]:
        dest_list.insert(index, item)
    return dest_list


class KeybindReplicator:
    """Class to generate scripts replicating recorded keybinds"""

    def __init__(self):
        self._dir_pth = os.path.dirname(os.path.abspath(__file__))
        self._pyblock_pth = os.path.join(self._dir_pth, "pyblocks.json")
        self._trascriber_pth = os.path.join(
            self._dir_pth, "pygame2pyau_transcription.json"
        )
        self._insertion_index: int = 2
        self._code_blocks: list = self._load_from_json(self._pyblock_pth)
        self._transcription_table: dict = self._load_from_json(self._trascriber_pth)
        self._target_keys: list = keybind_tracker()
        self._generate_code()

    def __repr__(self) -> str:
        return f"Keybindreplicator Object: {self._code_blocks}"

    def _load_from_json(self, _path: str):
        with open(_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _generate_code(self) -> None:
        _key_code: list = []
        if len(self._target_keys) == 0:
            raise ValueError('No keys detected, aborting.')
        self._target_keys = self._pygame2pyautogui(self._target_keys)
        for _key_event in self._target_keys:
            _key_code.append(self._key_event_handler(_key_event))
        self._code_blocks = insert_list_at_index(
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
        return f"pyautogui.keydown('{_key_down_event[1]}')"

    def _key_up_event_code(self, _key_up_event) -> str:
        return f"pyautogui.keyup('{_key_up_event[1]}')"

    def _pygame2pyautogui(self, pygame_keynames: list) -> list:
        print(pygame_keynames)
        return [(key_name[0],self._transcription_table.get(key_name[1]),key_name[2]) for key_name in pygame_keynames]

    def _block2codes_str(self) -> str:
        _code_str = "\n"
        return _code_str.join(self._code_blocks)

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

        _code_str = self._block2codes_str()
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(_code_str)
        return _code_str


a = KeybindReplicator()
a.dump_to_file("f4+r.pyw")
