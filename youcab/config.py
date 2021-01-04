import subprocess
from pathlib import Path
from typing import List

from youcab.errors import MecabConfigError


def _mecab_config_dicdir(mecab_config_path: str = "mecab-config") -> Path:
    """Get the result of executing ``mecab-config --dicdir``.

    Parameters
    ----------
    mecab_config_path : str, optional
        Executable path of mecab-config, by default "mecab-config".

    Returns
    -------
    Path
        The path where MeCab dictionary directories are stored.
    """
    try:
        result = subprocess.run(
            [mecab_config_path, "--dicdir"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        path = result.stdout.decode("utf-8").splitlines()[0]
        return Path(path)
    except FileNotFoundError:
        raise MecabConfigError("`mecab-config` is not found.")


def get_dicdirs() -> List[Path]:
    """Get MeCab dictionary directories.

    Returns
    -------
    List[Path]
        MeCab dictionary directories.
    """
    dicdirs = []
    for path in _mecab_config_dicdir().glob("**/dicrc"):
        dicdirs.append(path.parent.resolve())
    return dicdirs
