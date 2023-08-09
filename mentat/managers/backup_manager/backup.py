import os
import shutil
from typing import Optional
from termcolor import cprint


class CodeBackupManager:
    def __init__(self, backup_dir: Optional[str] = ".mentat_backups"):
        self.backup_dir = backup_dir

        if self.backup_dir:
            try:
                os.makedirs(self.backup_dir, exist_ok=True)
            except OSError as e:
                cprint(
                    f"Error occurred while creating backup directory '{self.backup_dir}': {str(e)}",
                    color="red",
                )
            except Exception as e:
                cprint(
                    f"An unexpected error occurred while creating backup directory: {str(e)}",
                    color="red",
                )

    def backup_files(self, code_file_manager: "CodeFileManager"):
        cprint("Creating backups...", color="yellow")
        for file_path in code_file_manager.get_all_file_paths():
            if self.backup_dir:
                relative_path = os.path.relpath(file_path)
                if os.path.sep in relative_path:
                    parent_folder, file_name = os.path.split(relative_path)
                    backup_folder = os.path.join(self.backup_dir, parent_folder)
                    os.makedirs(backup_folder, exist_ok=True)
                    backup_file_path = os.path.join(backup_folder, file_name + ".backup")
                else:
                    backup_file_path = os.path.join(self.backup_dir, os.path.basename(file_path) + ".backup")
            else:
                backup_file_path = file_path + ".backup"

            if not os.path.exists(backup_file_path):
                try:
                    shutil.copy2(file_path, backup_file_path)
                    cprint(f"Backup created successfully for the file {file_path}.", color="green")
                except PermissionError:
                    cprint(
                        f"Permission denied when trying to create backup for {file_path}.",
                        color="red",
                    )
                    continue
                except Exception as e:
                    cprint(
                        f"An error occurred while trying to create backup for {file_path}: {str(e)}",
                        color="red",
                    )
                    continue

        cprint("Backup process exited...", color="green")
