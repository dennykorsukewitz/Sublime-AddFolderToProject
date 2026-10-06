# [2.1.0]

## Changed

- Refactored `AddFolderToProject.py` for readability (formatting, removed unused class-level folder lists).
- `CreateProjectFromFile.run` uses `paths=None` instead of a mutable default argument.
- README icon includes `alt` text.
- Dependabot GitHub Actions updates run monthly with a 7-day cooldown.

## Fixed

- **Remove Folder from Project** resolves project folder paths against the project file directory before comparing, so relative entries (for example `sub` or `.`) remove correctly without `FileNotFoundError`. Thanks to @dpc00 ([#1](https://github.com/dennykorsukewitz/Sublime-AddFolderToProject/issues/1)).
- **Add Folder to Project** parent-folder list walks paths with `os.path.dirname()` so Windows ends at the drive root (`C:\`) instead of bare `C:`, and Unix paths list all ancestors. Thanks to @dpc00 ([#2](https://github.com/dennykorsukewitz/Sublime-AddFolderToProject/issues/2)).
