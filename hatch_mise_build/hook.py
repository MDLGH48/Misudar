
# # https://github.com/fiftysevendegreesofrad/sdna_plus/blob/Cross_platform/hatch_build.py
# # https://github.com/rmorshea/hatch-build-scripts/blob/main/src/hatch_build_scripts/plugin.py

# import os
# import sh
# from functools import cached_property
# from hatchling.builders.hooks.plugin.interface import BuildHookInterface
# import dataclasses

# # https://github.com/ofek/hatch-containers


# class MiseBuildHook(BuildHookInterface):
#     PLUGIN_NAME = 'mise'

#     @cached_property
#     def mise_config(self):
#         # https://mise.jdx.dev/installing-mise.html#shell-specific-installation-activation
#         defaults = ...
#         # MISE_DEBUG="1"
#         # MISE_QUIET="0"
#         # MISE_INSTALL_PATH="~/.local/bin/mise"
#         # MISE_VERSION="2025.7.32"


#         custom_install_cfg = self.config.get('mise-config', {})

#         cfg = ...

#         return cfg

#     def initialize(self, version, build_data):
#         self.app.display_info("Installing mise with debug flags...")

#         install_env = os.environ.copy()
#         install_env.update({
#             "MISE_DEBUG": "1",
#             "MISE_YES": "1",
#         })

#         # Check for a custom installation path in pyproject.toml
#         install_path = self.config.get("install-path")
#         if install_path:
#             self.app.display(f"Using custom mise install path: {install_path}")
#             install_env["MISE_INSTALL_PATH"] = install_path

#         try:
#             sh.sh(
#                 "-c",
#                 "curl -fsSL https://mise.jdx.dev/install.sh | sh",
#                 _env=install_env,
#             )
#             self.app.display_s("mise installed successfully.")
#             build_data['artifacts'].append(f'/{self.config_version_file}')
#         except sh.CommandNotFound as e:
#             self.app.display(f"Command not found: {e}")
#             raise
#         except sh.ErrorReturnCode as e:
#             self.app.display(f"Failed to install mise. Exit code: {e.exit_code}")
#             self.app.display(f"STDOUT: {e.stdout.decode()}")
#             self.app.display(f"STDERR: {e.stderr.decode()}")
#             raise

