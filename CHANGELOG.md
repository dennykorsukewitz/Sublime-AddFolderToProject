# Changelog

All notable changes to the "AddFolderToProject" package will be documented in this file.

## [2.1.0]

### Changed

- Refactored `AddFolderToProject.py` for readability (formatting, removed unused class-level folder lists).
- `CreateProjectFromFile.run` uses `paths=None` instead of a mutable default argument.
- Readme icon includes `alt` text.
- Dependabot GitHub Actions updates run monthly with a 7-day cooldown.
- Default `add_folder_to_project_folders` is an empty list instead of `/Users`, so extra macOS paths no longer appear on Windows.

### Fixed

- **Remove Folder from Project** resolves project folder paths against the project file directory before comparing, so relative entries (for example `sub` or `.`) remove correctly without `FileNotFoundError`. Thanks to @dpc00 ([#1](https://github.com/dennykorsukewitz/Sublime-AddFolderToProject/issues/1)).
- **Add Folder to Project** parent-folder list walks paths with `os.path.dirname()` so Windows ends at the drive root (`C:\`) instead of bare `C:`, and Unix paths list all ancestors. Thanks to @dpc00 ([#2](https://github.com/dennykorsukewitz/Sublime-AddFolderToProject/issues/2)).

## [2.0.0]

### Breaking

- Renamed Sublime commands (see [RELEASE.md](RELEASE.md) for the old → new mapping).

### Added

- Add Folder to Project: searchable list of folders (absolute and recursive paths) to add to the current project.
- Remove Folder from Project: list of active project folders that can be removed.
- Add Custom Folder to Project: add a folder by absolute path.
- Add this Folder to Project: add the folder of the current open file.
- Remove this Folder from Project: remove the folder of the current open file.
- Create Project from File: new Sublime window with a project for the current file’s folder.
- Copy File Path and Copy Dir Path for the current open file.

### Changed

- Updated README.md.
- Rewrite of [AddFolderToProject-SublimePlugin](https://github.com/DavidGerva/AddFolderToProject-SublimePlugin) with refactored and revised functions.

### Fixed

- Captions conflict.

## [1.1.1]

### Fixed

- Corrected behavior when no project is already opened.

## [1.1.0]

### Added

- Command **Create Project from File** (new project window with the file’s directory).

### Changed

- Fixed menu item visibility for files without a physical path; prompts for a custom path when needed.
- Directories already in the project are omitted from the add list.
- Context menu shows **Remove this Folder from Project** when the file’s directory is already in the project.

## [1.0.0]

### Added

- First release.
