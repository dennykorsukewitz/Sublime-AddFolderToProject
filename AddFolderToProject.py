import os  # Added import statement for "os"

import sublime
import sublime_plugin


def plugin_loaded():
    """
    Function called when the plugin is loaded.
    It initializes the global settings variable by
    loading the "AddFolderToProject.sublime-settings" file.
    """
    global settings
    settings = sublime.load_settings("AddFolderToProject.sublime-settings")


class Folder:
    """
    Class representing a folder in the project.
    """

    def __init__(self, window):
        self.window = window

    def add(self, dir_path):
        """
        Add a folder to the project.

        Args:
            dir_path (str): The path of the folder to add.
        """
        project_data = self.window.project_data()

        folder = {
            "follow_symlinks": True,
            "path": dir_path,
        }

        try:
            folders = project_data["folders"]
            for current_folder in folders:
                if current_folder["path"] == dir_path:
                    return
            folders.append(folder)
        except:  # noqa: E722
            folders = [folder]
            if project_data is None:
                project_data = {}
            project_data["folders"] = folders

        self.window.set_project_data(project_data)

        folders = settings.get("add_folder_to_project_folders")

        if dir_path not in folders:
            SaveFolderInSettings.run(self, dir_path)

    def remove(self, dirPath):
        """
        Remove a folder from the project.

        Args:
            dirPath (str): The path of the folder to remove.

        Returns:
            bool: True if the folder was successfully removed, False otherwise.
        """
        project_data = self.window.project_data()

        index = 0
        for folder in project_data["folders"]:
            if folder["path"]:
                if os.path.samefile(dirPath, folder["path"]):
                    del project_data["folders"][index]
                    self.window.set_project_data(project_data)
                    return True
                index = index + 1

    def exists(self, dirPath):
        """
        Check if a folder exists in the project.

        Args:
            dirPath (str): The path of the folder to check.

        Returns:
            bool: True if the folder exists in the project, False otherwise.
        """
        project_data = self.window.project_data()

        if project_data:
            for folder in project_data["folders"]:
                if folder["path"] and os.path.samefile(
                    dirPath, folder["path"]
                ):  # noqa: E501
                    return True

        return False

    def list(self):
        """
        Get a list of folders in the project.

        Returns:
            list: A list of folder paths.
        """
        folders = []
        folders.append("-- Add manually a directory --")

        active_folders = Folder.active_list(self)

        file_path = self.window.active_view().file_name()
        if file_path:
            dir_path = os.path.dirname(file_path)
            while os.path.isdir(dir_path):
                folders.append(dir_path)
                position = dir_path.rfind("\\")
                dir_path = dir_path[:position]

        absolute_folders = settings.get("add_folder_to_project_folders")
        recursive_folders = settings.get(
            "add_folder_to_project_recursive_folders"
        )  # noqa: E501

        if absolute_folders is not None:
            folders += [
                folder for folder in absolute_folders if folder not in folders
            ]  # noqa: E501

        if recursive_folders is not None:
            for folder in recursive_folders:
                if not folder.endswith("/"):
                    folder += "/"
                folders += [
                    folder + name
                    for name in os.listdir(folder)
                    if os.path.isdir(os.path.join(folder, name))
                    and (folder + name) not in folders
                ]

        folders = [
            folder for folder in folders if folder not in active_folders
        ]  # noqa: E501

        return folders

    def active_list(self):
        """
        Get a list of active folders in the project.

        Returns:
            list: A list of active folder paths.
        """
        folders = []
        project_data = self.window.project_data()

        try:
            for folder in project_data["folders"]:
                folders.append(folder["path"])
        except:  # noqa: E722
            folders = []

        return folders


class AddFolderToProject(sublime_plugin.WindowCommand):
    """
    "Add Folder to Project"
    Command to add a folder to the project. "Add Folder to Project"
    """

    folders = []

    def run(self):
        """
        Run the command.
        """
        self.folders = Folder.list(self)

        if not self.folders:
            AddCustomFolderToProject.run(self)
            return

        global my_self
        my_self = self

        self.window.show_quick_panel(
            items=self.folders,
            on_select=AddFolderToProject.on_select,
            on_highlight=None,
            flags=32,
            selected_index=-1,
            placeholder="AddFolderToProject: Select a folder to add...",
        )

    @staticmethod
    def on_select(index):
        """
        Callback function when a folder is selected.

        Args:
            index (int): The index of the selected folder.
        """
        if index == -1:
            return

        dir_path = my_self.folders[index]

        if dir_path == "-- Add manually a directory --":
            AddCustomFolderToProject.run(my_self)
            return

        Folder.add(my_self, dir_path)


class RemoveFolderFromProject(sublime_plugin.WindowCommand):
    """
    "Remove Folder from Project"
    Command to remove a folder from the project.
    """

    folders = []

    def run(self):
        """
        Run the command.
        """
        self.folders = Folder.active_list(self)

        if not self.folders:
            return

        global my_self
        my_self = self

        self.window.show_quick_panel(
            items=self.folders,
            on_select=RemoveFolderFromProject.on_select,
            on_highlight=None,
            flags=32,
            selected_index=-1,
            placeholder="AddFolderToProject: Select a folder to remove...",
        )

    @staticmethod
    def on_select(index):
        """
        Callback function when a folder is selected.

        Args:
            index (int): The index of the selected folder.
        """
        if index == -1:
            return

        dir_path = my_self.folders[index]

        Folder.remove(my_self, dir_path)


class AddCustomFolderToProject(sublime_plugin.WindowCommand):
    """
    "Add Custom Folder To Project"
    Command to add a custom folder to the project.
    """

    def run(self):
        """
        Run the command.
        """
        file_path = self.window.active_view().file_name()

        if not file_path:
            dir_path = ""
        else:
            dir_path = os.path.dirname(file_path)

        global my_self
        my_self = self

        self.window.show_input_panel(
            caption="Add Folder:",
            initial_text=dir_path,
            on_done=AddCustomFolderToProject.on_done,
            on_change=None,
            on_cancel=None,
        )

    @staticmethod
    def on_done(dir_path):
        """
        Callback function when the folder path is entered.

        Args:
            dir_path (str): The path of the folder to add.
        """
        Folder.add(my_self, dir_path)


class AddCurrentFolderToProject(sublime_plugin.WindowCommand):
    """
    "Add this Folder to Project"
    Command to add the current folder to the project.
    """

    def run(self):
        """
        Run the command.
        """
        file_path = self.window.active_view().file_name()

        if not file_path:
            return

        dir_path = os.path.dirname(file_path)
        if dir_path:
            Folder.add(self, dir_path)


class RemoveCurrentFolderFromProject(sublime_plugin.WindowCommand):
    """
    "Remove this Folder from Project"
    Command to remove the current folder from the project.
    """

    def run(self):
        """
        Run the command.
        """
        file_path = self.window.active_view().file_name()

        if not file_path:
            return

        dir_path = os.path.dirname(file_path)
        if dir_path:
            Folder.remove(self, dir_path)


class SaveFolderInSettings(sublime_plugin.WindowCommand):
    """
    Command to save a folder in the settings.
    """

    dir_path = ""

    def run(self, dir_path):
        """
        Run the command.

        Args:
            dir_path (str): The path of the folder to save.
        """
        self.dir_path = dir_path

        global my_self
        my_self = self

        self.window.show_quick_panel(
            items=["yes", "no"],
            on_select=SaveFolderInSettings.on_select,
            flags=32,
            selected_index=-1,
            on_highlight=None,
            placeholder="AddFolderToProject: Should I save the new folder in the settings?",  # noqa: E501
        )

    @staticmethod
    def on_select(index):
        """
        Callback function when an option is selected.

        Args:
            index (int): The index of the selected option.
        """
        if index == -1:
            return

        if index == 1:
            return

        folders = settings.get("add_folder_to_project_folders")
        folders.append(my_self.dir_path)

        settings.set("add_folder_to_project_folders", folders)
        sublime.save_settings("AddFolderToProject.sublime-settings")


class CopyFilePath(sublime_plugin.WindowCommand):
    """
    "Copy File Path"
    Command to copy the file path to the clipboard.
    """

    def run(self):
        """
        Run the command.
        """
        file_path = self.window.active_view().file_name()
        sublime.set_clipboard(file_path)


class CopyDirPath(sublime_plugin.WindowCommand):
    """
    "Copy Dir Path"
    Command to copy the directory path to the clipboard.
    """

    def run(self):
        """
        Run the command.
        """
        file_path = self.window.active_view().file_name()
        dir_path = os.path.dirname(file_path)
        if dir_path:
            sublime.set_clipboard(dir_path)


class CreateProjectFromFile(sublime_plugin.WindowCommand):
    """
    "Create Project From File"
    Command to create a project from a file.
    """

    def run(self, paths=[]):
        """
        Run the command.

        Args:
            paths (list): List of file paths.
        """
        import subprocess

        items = []
        executable_path = sublime.executable_path()

        if sublime.platform() == "osx":
            app_path = executable_path[: executable_path.rfind(".app/") + 5]
            executable_path = app_path + "Contents/SharedSupport/bin/subl"

        items.append(executable_path)

        file_path = self.window.active_view().file_name()
        dir_path = os.path.dirname(file_path)

        items.append(dir_path)
        items.append(file_path)

        subprocess.Popen(items)
