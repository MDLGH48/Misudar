# https://github.com/fiftysevendegreesofrad/sdna_plus/blob/Cross_platform/hatch_build.py
# https://github.com/rmorshea/hatch-build-scripts/blob/main/src/hatch_build_scripts/plugin.py
# https://github.com/ofek/hatch-containers
# https://mise.jdx.dev/tips-and-tricks.html#bootstrap-script

import sh
from functools import cached_property
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from dataclasses import dataclass, field, asdict
from pathlib import Path
import typing
import sys
import os
import platform
import warnings


class SystemCompatWarning(UserWarning):
    pass


def echo_append(line: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    sh.echo(line, _out=str(dest), _append=True)


@dataclass
class MiseInstaller:
    INSTALL_SRC: str = Path(__file__).parent / "setup-mise.sh"
    DEBUG: int = 1
    QUIET: int = 0
    INSTALL_PATH: Path = Path("~/.local/bin/mise").expanduser()
    VERSION: str = "v2025.8.1"

    @property
    def default_shell(self):
        return os.getenv("SHELL")

    def install(self):
        install_args = {f"MISE_{k}": str(v) for k, v in asdict(self).items()}
        src = install_args.pop("MISE_INSTALL_SRC")
        return sh.sh.bake(src, **install_args)

    def activate(self, shell: str):
        match shell:
            case "bash":
                bashrc = Path("~/.bashrc").expanduser()
                return echo_append(r'eval "$(mise activate bash)"', bashrc)

            case "zsh":
                zshrc = (Path(os.environ.get("ZDOTDIR", "~")) / ".zshrc").expanduser()
                return echo_append(r'eval "$(mise activate zsh)"', zshrc)

            case "fish":
                fish_cfg = Path("~/.config/fish/config.fish").expanduser()
                return echo_append(r"mise activate fish | source", fish_cfg)
            case _:
                return warnings.warn(
                    "unknown shell - not activated", SystemCompatWarning
                )
