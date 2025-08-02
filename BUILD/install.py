import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from dataclasses import dataclass, asdict
from pathlib import Path
import warnings
import sh


class SystemCompatWarning(UserWarning):
    pass


def echo_append(line: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    return sh.echo(line, _out=str(dest), _append=True)


def default_shell():
    shenv = os.environ("SHELL")
    if shenv:
        return Path(shenv).name


def get_current_commit() -> str:
    return sh.git("rev-parse --short HEAD")


@dataclass
class MiseInstaller:
    install_path: Path = Path("~/.local/bin/mise").expanduser()
    version: str = "v2025.8.1"
    install_src: str = Path(__file__).parent / "setup_mise.sh"
    debug: int = 1
    quiet: int = 0

    def __post_init__(self):
        self.install_src = Path(self.install_src).expanduser()

    @property
    def install_params(self):
        return {f"MISE_{k.upper()}": str(v) for k, v in asdict(self).items()}

    def model_dump(self):
        return asdict(self)

    def build(self):
        install_params = self.install_params
        src = install_params.pop("MISE_INSTALL_SRC")
        return sh.sh.bake(src, _env=install_params)

    @property
    def get_py_pkg_version(self):
        return "{mise_vs}+py.{git_commit}".format(
            mise_vs=self.version, git_commit=get_current_commit()
        )

    def activate(self, sh_: str = None):
        shell = sh_ or default_shell()
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


class MiseInstallHook(BuildHookInterface):

    @property
    def _mise_installer(self) -> MiseInstaller:
        return MiseInstaller(**self.config.get("mise", {}))

    def initialize(self, version, build_data):
        build_cmd = self._mise_installer.build()
        for line in build_cmd(_iter=True):
            self.app.display(line)
        build_data["artifacts"].append(str(self._mise_installer.install_path))

    # def finalize(self, version, build_data, artifact_path):
    #     return super().finalize(version, build_data, artifact_path)
