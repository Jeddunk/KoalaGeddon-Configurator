import sys  # Even if my IDE tells me otherwise, this import is, in fact, used, just once, but it is used :D
import os
import winreg
import pathlib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk as themed
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import json

version = 1.0
# Different classes used by the GUI, these are for calling what their titles suggest #
class frames:  # Collection of frames packed to root #
    @staticmethod
    def left(anchor):
        global left_frame
        left_frame = ttk.Frame(root)
        left_frame.pack(side=LEFT, anchor=anchor)

    @staticmethod
    def right(anchor):
        global right_frame
        right_frame = ttk.Frame(root)
        right_frame.pack(side=RIGHT, anchor=anchor)

    @staticmethod
    def low(anchor):
        global low_frame
        low_frame = ttk.Frame(root)
        low_frame.pack(side=BOTTOM, anchor=anchor)

    @staticmethod
    def center():
        global frame
        frame = ttk.Frame(root)
        frame.pack()


# Default global values
var_en_steam = None
var_en_epic = None
var_en_origin = None
var_rep_steam = None
var_rep_epic = None
var_rep_origin = None
# Some variables for id and blacklist values, they are all lists #
appid = []
dlc_id = []
item_id = []
var_blacklist_steam = []
var_blacklist_epic = []
var_blacklist_origin = []


class steam_values:
    @staticmethod
    def enable(en_or_dis):  # Enabled or disable injection.
        global var_en_steam
        var_en_steam = en_or_dis  # Singular value allowed
        print(var_en_steam)

    @staticmethod
    def replicate(rep_or_not):  # Replicate or not.
        global var_rep_steam
        var_rep_steam = rep_or_not  # Singular value allowed
        print(var_rep_steam)

    @staticmethod
    def app_id():  # Id of DLC
        id_steam = appid_enter.get()
        appid.append(id_steam)  # Appends to list with id values.
    @staticmethod
    def blacklist(yes_or_no):  # Blacklist or not
        var_blacklist_steam.append(yes_or_no)  # Appends to list of blacklists in the same order as the id's
        steam_values.app_id()  # Need to add checks later
        print(var_blacklist_steam)
        print(appid)


class epic_values:
    @staticmethod
    def enable(en_or_dis):
        global var_en_epic
        var_en_epic = en_or_dis
        print(var_en_epic)

    @staticmethod
    def replicate(rep_or_not):
        global var_rep_epic
        var_rep_epic = rep_or_not
        print(var_rep_epic)

    @staticmethod
    def dlc_id():
        id_epic = DLC_id_enter.get()
        dlc_id.append(id_epic)

    @staticmethod
    def blacklist(yes_or_no):
        var_blacklist_epic.append(yes_or_no)
        print(var_blacklist_epic)
        epic_values.dlc_id()
        print(dlc_id)


class origin_values:
    @staticmethod
    def enable(en_or_dis):
        global var_en_origin
        var_en_origin = en_or_dis
        print(var_en_origin)

    @staticmethod
    def replicate(rep_or_not):
        global var_rep_origin
        var_rep_origin = rep_or_not
        print(var_rep_origin)

    @staticmethod
    def item_id():
        id_origin = item_id_enter.get()
        item_id.append(id_origin)

    @staticmethod
    def blacklist(yes_or_no):
        var_blacklist_origin.append(yes_or_no)
        origin_values.item_id()
        print(var_blacklist_origin)
        print(item_id)


class paths:
    @staticmethod
    def get_path():  # Gets path from current running script.
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = str(os.path.dirname(sys.argv[0]))

        return pathlib.Path(base_path)

    @staticmethod
    def get_json_path():
        try:
            access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            access_key = winreg.OpenKey(access_registry, r"SOFTWARE\acidicoala\Koalageddon")
            # accessing the key to open the registry directories under
            (working_dir, _) = winreg.QueryValueEx(access_key, "WORKING_DIR")
            config_path = pathlib.Path(working_dir) / "Config.jsonc"
            return str(config_path)

        except FileNotFoundError:
            try:  # Prior line will be deleted on next Koalageddon version
                access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                access_key = winreg.OpenKey(access_registry, r"SOFTWARE\acidicoala\Koalageddon")
                # accessing the key to open the registry directories under
                (working_dir, _) = winreg.QueryValueEx(access_key, "WORKING_DIR")
                config_path = pathlib.Path(working_dir) / "Config.jsonc"
                return str(config_path)
            except FileNotFoundError:
                if os.path.exists(paths.get_path() + "/json_path.txt"):  # If already specified by user
                    with open(paths.get_path() + "/json_path.txt", "r") as p:
                        json_path_txt = str(p.readline())
                        if os.path.isfile(json_path_txt):
                            return json_path_txt

                else:
                    # If none of the prior ones return it will ask the user #
                    messagebox.showinfo("Config.jsonc not found", "Please select the Koalageddon Config file")
                    path = str(askopenfilename())
                    if "Config.json" in path:
                        with open("json_path.txt",
                                  'w') as p:  # Saves itself as json_path.txt, will overwrite if it already exists
                            p.write(path)
                        return path
                    else:
                        messagebox.showerror("Error", "Please select a valid config file")
                        return 0  # The user will have to pick the option again to select a valid config file #
class json_file:  # This is the config file itself, it's handling, backup, etc.
    @staticmethod
    def error_handling():  # To deal with comments if they exist, because while the nlohmann JSON library can parse
        # them, the common JSON libraries for Python cannot.
        with open(paths.get_json_path(), "r") as f:
            data_raw = f.read()
            # This is some really ugly code, it just removes all comments, there's probably a better way to do this :(
            data = data_raw.replace("// DO NOT EDIT THIS VALUE", "").replace("// Get App ID from SteamDB", "").replace(
                "// Alien Breed: Impact - PL Check [Do not force polish language]", "").replace("// Darkness II Low "
                                                                                                "Violence [Do not "
                                                                                                "censor violence]",
                                                                                                "").replace(
                "// Get DLC ID from ScreamDB", "").replace("// A "
                                                           "Total War Sage: TROY [It actually asks this ID...]",
                                                           "").replace("// Use ItemId from Unlocker32.Origin"
                                                                       ".log", "").replace(
                '// "SIMS4.OFF.SOLP.0x0000000000030553" // Sims 4: Get Famous [Better stay '
                'anonymous]', "").replace("// Ubisoft games unload the Unlocker DLL :(", "").replace("// Unreal Engine",
                                                                                                     "").replace(
                "// Origin integration with other stores", "").replace("// Ubisoft integration with "
                                                                       "other stores", "").replace("// Steam",
                                                                                                   "").replace(
                "// Origin", "").replace("// Ubisoft", "")
            return data

    @staticmethod
    def fixed_json():  # Called by error handler
        data_raw = json_file.error_handling()
        data = json.loads(data_raw)
        return data

    @staticmethod
    def get_data():  # A basic way to get the json data
        try:
            with open(paths.get_json_path(), "rt") as f:
                data_raw = f.read()
                data = json.loads(data_raw)
        except json.decoder.JSONDecodeError:  # Comments were found.
            data = json_file.fixed_json()
        return data

    @staticmethod
    def backup():  # Backs it up! Also checks for itself, maybe i'll add the option of multiple backups in the future
        if paths.get_json_path() == 0:
            return 0  # To not get the user stuck on a loop if they cancel the operation
        data = json_file.get_data()

        if os.path.exists(paths.get_json_path().replace("Config.jsonc", "Config_o.jsonc")):
            ask = messagebox.askyesno("Backup file found", "Do you wish to overwrite your previous backup?")
            if ask:
                try:
                    with open(paths.get_json_path().replace("Config.jsonc", "Config_o.jsonc"), "w") as outfile:
                        json.dump(data, outfile, indent=1)
                        messagebox.showinfo("Success", "A backup of the original configuration file has been created")
                except EXCEPTION:  # It shouldn't fail if you're able to use Koalageddon at all.
                    messagebox.showerror("Error",
                                         "Something went wrong, please make sure you have the necessary permissions\n"
                                         "and try again.")
        else:
            try:
                with open(paths.get_json_path().replace("Config.jsonc", "Config_o.jsonc"), "w") as outfile:
                    json.dump(data, outfile, indent=1)
                messagebox.showinfo("Success", "A backup of the original configuration file has been created")
            except EXCEPTION:
                messagebox.showerror("Error",
                                     "Something went wrong, please make sure you have the necessary permissions\n"
                                     "and try again.")

    @staticmethod
    def commit(platform):
        if platform == "steam":
            commit = json_file.get_data()
            skip_value = 0
            print(enable_steam)
            print(replicate_steam)
            if "Skip" in str(enable_steam):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Steam"]["enabled"] = enable_steam

            if "Skip" in str(replicate_steam):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Steam"]["replicate"] = replicate_steam
            to_add = []
            index = 0
            if blacklist_steam is False:
                print("Skip")
                skip_value = skip_value + 1
            else:
                for _ in blacklist_steam:  # This will *in theory* recursively check for each appid and blacklist
                    # value for each index and resolve if it should add or remove it.
                    if "remove" in blacklist_steam[index]:
                        print("Removing")
                        self_appid = appid[index]
                        self_index = commit["platforms"]["Steam"]["blacklist"].index(self_appid)
                        del commit["platforms"]["Steam"]["blacklist"][self_index]

                    elif "remove" not in blacklist_steam[index]:
                        to_add.append(appid[index])
                    index = index + 1
                if to_add:
                    commit["platforms"]["Steam"]["blacklist"].extend(to_add)

            if skip_value == 3:
                print("No change")
            else:
                with open(paths.get_json_path(), "w") as outfile:
                    json.dump(commit, outfile, indent=1)
                    messagebox.showinfo("Success", "The file has been modified")
            callback_to.widgets2()
        elif platform == "epic":
            commit = json_file.get_data()
            skip_value = 0
            print(enable_epic)
            print(replicate_epic)
            if "Skip" in str(enable_epic):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Epic Games"]["enabled"] = enable_epic

            if "Skip" in str(replicate_epic):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Epic Games"]["replicate"] = replicate_epic
            to_add = []
            index = 0
            if blacklist_epic is False:
                print("Skip")
                skip_value = skip_value + 1
            else:
                for _ in blacklist_epic:  # This will *in theory* recursively check for each appid and blacklist
                    # value for each index and resolve if it should add or remove it.
                    if "remove" in blacklist_epic[index]:
                        print("Removing")
                        self_dlc_id = dlc_id[index]
                        self_index = commit["platforms"]["Epic Games"]["blacklist"].index(self_dlc_id)
                        del commit["platforms"]["Epic Games"]["blacklist"][self_index]

                    elif "remove" not in blacklist_epic[index]:
                        to_add.append(dlc_id[index])
                    index = index + 1
                if to_add:
                    commit["platforms"]["Epic Games"]["blacklist"].extend(to_add)

            if skip_value == 3:
                print("No change")
            else:
                with open(paths.get_json_path(), "w") as outfile:
                    json.dump(commit, outfile, indent=1)
                    messagebox.showinfo("Success", "The file has been modified")
                    print(commit["platforms"]["Epic Games"])
            callback_to.widgets2()
        elif platform == "origin":
            commit = json_file.get_data()
            skip_value = 0
            print(enable_origin)
            print(replicate_origin)
            if "Skip" in str(enable_origin):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Origin"]["enabled"] = enable_origin

            if "Skip" in str(replicate_origin):
                print("Skip")
                skip_value = skip_value + 1
            else:
                commit["platforms"]["Origin"]["replicate"] = replicate_origin
            to_add = []
            index = 0
            if blacklist_origin is False:
                print("Skip")
                skip_value = skip_value + 1
            else:
                for _ in blacklist_origin:  # This will *in theory* recursively check for each appid and blacklist
                    # value for each index and resolve if it should add or remove it.
                    if "remove" in blacklist_origin[index]:
                        print("Removing")
                        self_item_id = item_id[index]
                        self_index = commit["platforms"]["Origin"]["blacklist"].index(self_item_id)
                        del commit["platforms"]["Origin"]["blacklist"][self_index]

                    elif "remove" not in blacklist_origin[index]:
                        to_add.append(item_id[index])
                    index = index + 1
                if to_add:
                    commit["platforms"]["Origin"]["blacklist"].extend(to_add)

            if skip_value == 3:
                print("No change")
            else:
                with open(paths.get_json_path(), "w") as outfile:
                    json.dump(commit, outfile, indent=1)
                    messagebox.showinfo("Success", "The file has been modified")
                    print(commit["platforms"]["Origin"])
            callback_to.widgets2()


# Logo preload, done for performance #
self_path = str(paths.get_path())  # Path of current script
steam_logo = Image.open(self_path + "/logos/steam.png")
epic_logo = Image.open(self_path + "/logos/epic.png")
origin_logo = Image.open(self_path + "/logos/origin.png")

# Resize to adequate size, if High DPI is to be added, this will have to be changed accordingly.
steam_logo_resize = steam_logo.resize((160, 50), Image.ANTIALIAS)
epic_logo_resize = epic_logo.resize((120, 100), Image.ANTIALIAS)
origin_logo_resize = origin_logo.resize((150, 58), Image.ANTIALIAS)


class logo:  # These are the logos for the supported platforms, it automatically packs them :D}
    @staticmethod
    def steam(frame_self, x, y):  # Frame, padx and pady values.
        logo_itself = ImageTk.PhotoImage(steam_logo_resize)
        steam_string = Label(frame_self, image=logo_itself)
        steam_string.image = logo_itself
        steam_string.pack(padx=x, pady=y)

    @staticmethod
    def epic(frame_self, x, y):
        logo_itself = ImageTk.PhotoImage(epic_logo_resize)
        epic_string = Label(frame_self, image=logo_itself)
        epic_string.image = logo_itself
        epic_string.pack(padx=x, pady=y)

    @staticmethod
    def origin(frame_self, x, y):
        logo_itself = ImageTk.PhotoImage(origin_logo_resize)
        origin_string = Label(frame_self, image=logo_itself)
        origin_string.image = logo_itself
        origin_string.pack(padx=x, pady=y)


class common_widgets:
    @staticmethod
    def label(frame_self, text, padx, pady, anchor, *justify):
        if anchor != 0 and not justify:
            lbl = ttk.Label(frame_self, text=text)
            lbl.pack(padx=padx, pady=pady, anchor=anchor)
        elif anchor and justify:
            lbl = ttk.Label(frame_self, text=text, justify=justify)
            lbl.pack(padx=padx, pady=pady, anchor=anchor)
        elif anchor == 0 and justify:
            lbl = ttk.Label(frame_self, text=text, justify=justify)
            lbl.pack(padx=padx, pady=pady, )
        else:
            lbl = ttk.Label(frame_self, text=text)
            lbl.pack(padx=padx, pady=pady)

    @staticmethod
    def button(frame_self, text, command, padx, pady, *anchor):
        bttn = ttk.Button(frame_self, text=text, command=command)
        if anchor:
            bttn.pack(padx=padx, pady=pady, anchor=anchor)
        else:
            bttn.pack(padx=padx, pady=pady)

    @staticmethod  # Well, aren't you a big piece o' code?
    def image_button(frame_self, text, image_path, image_size_x, image_size_y, compound, command, padx, pady, *anchor):
        image = Image.open(image_path)
        image_resize = image.resize((image_size_x, image_size_y), Image.ANTIALIAS)
        image_usable = ImageTk.PhotoImage(image_resize)
        button_image = ttk.Button(frame_self, image=image_usable, text=text, command=command,
                                  compound=compound)
        button_image.image = image_usable
        if anchor:
            button_image.pack(pady=pady, padx=padx, anchor=anchor)
        else:
            button_image.pack(pady=pady, padx=padx)

    @staticmethod
    def separator(frame_self, orient, fill, *pady, **padx):
        separator = ttk.Separator(frame_self, orient=orient)
        if pady != 0 and not None:
            separator.pack(fill=fill, pady=pady)
        elif padx != 0 and pady == 0:
            separator.pack(fill=fill, pady=padx)
        elif pady and padx:
            separator.pack(fill=fill, pady=pady, padx=padx)
        else:
            separator.pack(fill=fill)

    @staticmethod
    def new_window(text):
        new_wndw = Toplevel(root)
        center(new_wndw)
        common_widgets.label(new_wndw, text, 5, 5, 0)

    @staticmethod
    def change_size(width, height):
        root.minsize(width, height)
        size = str(width) + "x" + str(height)
        root.geometry(size)
        center(root)


class destroy_rebuild:  # This function will delete or reset stuff
    @staticmethod
    def reset_values(*show):  # Every value stored will be reset unless it is needed
        global appid, dlc_id, item_id, var_blacklist_steam, var_blacklist_epic, var_blacklist_origin

        appid = []
        dlc_id = []
        item_id = []
        var_blacklist_steam = []
        var_blacklist_epic = []
        var_blacklist_origin = []
        if show:
            messagebox.showinfo("Success", "The values have been reset")

    def widget_destroy(*widget):  # This function destroys any widgets specified on call
        for widget in widget:
            widget.destroy()  # Is it just me or has the word widget lost it's meaning with this function?
    @staticmethod
    def frame_rebuild(*self):  # Function that destroys all frames and child widgets, this effectively lets me change
        # the widgets displayed, it will also reset values if self is true
        left_frame.destroy()
        right_frame.destroy()
        frame.destroy()
        low_frame.destroy()
        # Places them again #
        frames.left(SW)
        frames.right(SE)
        frames.low(S)
        frames.center()
        if self:
            destroy_rebuild.reset_values()


class callback_to:  # Function to call a different widget set, I tried to turn this into a single function but it kept
    # giving me a NoneType :(
    @staticmethod
    def origin():
        destroy_rebuild.frame_rebuild(1)
        origin_widget()

    @staticmethod
    def epic():
        destroy_rebuild.frame_rebuild(1)
        epic_widget()

    @staticmethod
    def steam():
        destroy_rebuild.frame_rebuild(1)
        steam_widget()

    @staticmethod
    def widgets():
        destroy_rebuild.frame_rebuild(1)
        widgets()

    @staticmethod
    def widgets2():
        destroy_rebuild.frame_rebuild(1)
        widgets2()

    @staticmethod
    def widgets2_1():
        destroy_rebuild.frame_rebuild(1)
        widgets2_1()

    @staticmethod
    def commit(platform):
        destroy_rebuild.frame_rebuild()
        commit_changes(platform)


class preview_window:
    @staticmethod
    def show(platform):
        global callback, var_en_show, var_rep_show, var_blacklist_show, id_show
        if platform == "steam":
            var_en_show = var_en_steam
            var_rep_show = var_rep_steam
            var_blacklist_show = var_blacklist_steam
            id_show = appid
        elif platform == "epic":
            var_en_show = var_en_epic
            var_rep_show = var_rep_epic
            var_blacklist_show = var_blacklist_epic
            id_show = dlc_id
        elif platform == "origin":
            var_en_show = var_en_origin
            var_rep_show = var_rep_origin
            var_blacklist_show = var_blacklist_origin
            id_show = item_id

        common_widgets.change_size(1000, 200)

        enable = "No changes were made"
        replicate = "No changes were made"
        blacklist = "No changes were made"
        ids = "No changes were made"
        if var_en_show:
            enable = var_en_show
        if var_rep_show:
            replicate = var_rep_show
        if var_blacklist_show:
            blacklist = var_blacklist_show
        if id_show or "AppID" or "Item ID" or "DLC ID" not in id_show:
            ids = id_show

        enable_lbl = "Enable DLL injection: " + enable
        replicate_lbl = "Enable replication: " + replicate
        blacklist_lbl = "List of removals from or additions to the blacklist: " + str(blacklist).replace("remove_"
                                                                                                         "blacklist",
                                                                                                         "Removal").replace(
            "blacklist", "Addition").replace("[", "").replace("]", "")
        ids_lbl = "List of ID's to remove or add to the blacklist: " + str(ids).replace("[", "").replace("]", "")

        if not ids:  # Patch for bad coding skill :(
            ids_lbl = "List of ID's to remove or add to the blacklist: No changes were made"
        common_widgets.label(frame, enable_lbl, 5, 15, 0)
        common_widgets.label(frame, replicate_lbl, 5, 5, 0)
        common_widgets.separator(frame, "horizontal", "x", 5, 5)
        common_widgets.label(frame, "The following lists are ordered in relation to each other", 5, 5, 0)
        common_widgets.separator(frame, "horizontal", "x", 5, 5)
        common_widgets.label(frame, blacklist_lbl, 5, 5, 0)
        common_widgets.label(frame, ids_lbl, 5, 5, 0)
        common_widgets.button(right_frame, "Commit", lambda *args: json_file.commit(platform), 5, 5, N)

        if platform == "steam":
            common_widgets.button(left_frame, "Return", callback_to.steam, 5, 5, N)
        elif platform == "epic":
            common_widgets.button(left_frame, "Return", callback_to.epic, 5, 5, N)
        elif platform == "origin":
            common_widgets.button(left_frame, "Return", callback_to.origin, 5, 5, N)


# The way this GUI is coded is, in essence, the calling collections of widgets, they are enumerated mainly because
# my IDE wouldn't stop bothering me about their names, as such, they will be defined in a annexed comment.
def main_window():  # Ttk root and TtkThemes definitions
    # Begin window #
    global root
    root = themed(theme='breeze')  # You can change the theme to one of your liking if you so wish :D
    # Tested on 720p resolution, if you wish to add high dpi support you may fork it and push a PR, as I have no means
    # to properly test such a feature.
    root.resizable(height=False, width=False)
    root.title(f'KG-GUI Version {version}')
    root.iconbitmap(default=str(paths.get_path()) + "/logos/acidi.ico")
    # Set frames #
    frames.left(SW)
    frames.right(SE)
    frames.low(S)
    frames.center()
    # Call first widget collection #
    widgets()
    # Center and loop #
    center(root)
    root.mainloop()


def center(self):  # Function to center itself #
    self.update_idletasks()

    w = self.winfo_screenwidth()
    h = self.winfo_screenheight()

    size_x, size_y = self.geometry().split('+')[0].split('x')
    x = int(w / 2 - int(size_x) / 2)
    y = int(h / 2 - int(size_y) / 2)

    self.geometry(f'{size_x}x{size_y}+{x}+{y}')


def widgets():  # Initial window's widgets
    common_widgets.change_size(896, 150)
    common_widgets.label(frame, "Welcome to the Koalageddon configurator! \n In this GUI you may configure the"
                                " application by modifying the parameters and the activation or deactivation of \n"
                                "the injection itself, it\'s replication, and DLC Blacklisting", 5, 40, N, "center")

    common_widgets.button(left_frame, "Exit", lambda: sys.exit(), 15, 5)
    common_widgets.button(right_frame, "Continue", callback_to.widgets2, 15, 5)


def steam_widget():
    logo.steam(frame, 15, 15)
    common_widgets.change_size(1000, 300)  # Top left and top right for more options if need be ;)
    # Enable or Disable injection
    common_widgets.label(left_frame, "Enable or disable DDL injection", 5, 5, N)
    common_widgets.button(left_frame, "Enable", lambda *args: steam_values.enable("enable"), 5, 5)
    common_widgets.button(left_frame, "Disable", lambda *args: steam_values.enable("disable"), 5, 5)

    # Replicate or not
    common_widgets.label(right_frame, "Enable or disable replication", 5, 5, N)
    common_widgets.button(right_frame, "Enable", lambda *args: steam_values.replicate("enable"), 5, 5, N)
    common_widgets.button(right_frame, "Disable", lambda *args: steam_values.replicate("disable"), 5, 5)

    # Blacklist or remove from same, and AppID
    common_widgets.label(frame, "AppID to blacklist or remove from blacklist", 5, 5, 0)
    common_widgets.button(low_frame, "Blacklist", lambda *args: steam_values.blacklist("blacklist"), 5, 5)

    global appid_enter  # Needs to be declared here, otherwise I can't get the contents #
    appid_enter = ttk.Entry(frame, width=15, justify="center")
    appid_enter.insert(0, "AppID")
    appid_enter.pack(padx=5, pady=5)

    common_widgets.button(low_frame, "Remove from blacklist", lambda *args: steam_values.blacklist("remove_blacklist"),
                          5, 5)

    # Previous, revert and next widgets
    common_widgets.separator(low_frame, "horizontal", "x", 10)
    common_widgets.button(low_frame, "Revert changes", lambda *args: destroy_rebuild.reset_values(1), 5, 5, S)

    common_widgets.separator(left_frame, "horizontal", "x", 10)
    common_widgets.button(left_frame, "Back", lambda: callback_to.widgets2(), 5, 5, S)

    common_widgets.separator(right_frame, "horizontal", "x", 10)

    common_widgets.button(right_frame, "Commit changes", lambda *args: callback_to.commit("steam"), 5, 5, S)


def epic_widget():
    logo.epic(frame, 1, 1)
    common_widgets.change_size(1000, 315)

    # Enable or Disable injection
    common_widgets.label(left_frame, "Enable or disable DDL injection", 5, 5, N)
    common_widgets.button(left_frame, "Enable", lambda *args: epic_values.enable("enable"), 5, 5)
    common_widgets.button(left_frame, "Disable", lambda *args: epic_values.enable("disable"), 5, 5)

    # Replicate or not
    common_widgets.label(right_frame, "Enable or disable replication", 5, 5, N)
    common_widgets.button(right_frame, "Enable", lambda *args: epic_values.replicate("enable"), 5, 5)
    common_widgets.button(right_frame, "Disable", lambda *args: epic_values.replicate("disable"), 5, 5)

    # Blacklist or remove from same, and AppID
    common_widgets.label(frame, "DLC ID to blacklist or remove from blacklist", 5, 5, 0)
    common_widgets.button(low_frame, "Blacklist", lambda *args: epic_values.blacklist("blacklist"), 5, 5)

    global DLC_id_enter  # Needs to be declared here, otherwise I can't get the contents #
    DLC_id_enter = ttk.Entry(frame, width=15, justify="center")
    DLC_id_enter.insert(0, "DLC ID")
    DLC_id_enter.pack(padx=5, pady=5)

    common_widgets.button(low_frame, "Remove from blacklist", lambda *args: epic_values.blacklist("remove_blacklist"),
                          5, 5)

    # Previous, revert and next widgets
    common_widgets.separator(low_frame, "horizontal", "x", 10)
    common_widgets.button(low_frame, "Revert changes", lambda *args: destroy_rebuild.reset_values(1), 5, 5, S)

    common_widgets.separator(left_frame, "horizontal", "x", 10)
    common_widgets.button(left_frame, "Back", lambda: callback_to.widgets2(), 5, 5, S)

    common_widgets.separator(right_frame, "horizontal", "x", 10)

    common_widgets.button(right_frame, "Commit changes", lambda *args: callback_to.commit("epic"), 5, 5, S)


def origin_widget():
    logo.origin(frame, 15, 15)
    common_widgets.change_size(1000, 300)

    # Enable or Disable injection
    common_widgets.label(left_frame, "Enable or disable DDL injection", 5, 5, N)
    common_widgets.button(left_frame, "Enable", lambda *args: origin_values.enable("enable"), 5, 5)
    common_widgets.button(left_frame, "Disable", lambda *args: origin_values.enable("disable"), 5, 5)

    # Replicate or not
    common_widgets.label(right_frame, "Enable or disable replication", 5, 5, N)
    common_widgets.button(right_frame, "Enable", lambda *args: origin_values.replicate("enable"), 5, 5)
    common_widgets.button(right_frame, "Disable", lambda *args: origin_values.replicate("disable"), 5, 5)

    # Blacklist or remove from same, and AppID
    common_widgets.label(frame, "Item ID to blacklist or remove from blacklist", 5, 5, 0)
    common_widgets.button(low_frame, "Blacklist", lambda *args: origin_values.blacklist("blacklist"), 5, 5)

    global item_id_enter  # Needs to be declared here, otherwise I can't get the contents #
    item_id_enter = ttk.Entry(frame, width=15, justify="center")
    item_id_enter.insert(0, "Item ID")
    item_id_enter.pack(padx=5, pady=5)

    common_widgets.button(low_frame, "Remove from blacklist", lambda *args: origin_values.blacklist("remove_blacklist"),
                          5, 5)

    # Previous, revert and next widgets
    common_widgets.separator(low_frame, "horizontal", "x", 10)
    common_widgets.button(low_frame, "Revert changes", lambda *args: destroy_rebuild.reset_values(1), 5, 5, S)

    common_widgets.separator(left_frame, "horizontal", "x", 10)
    common_widgets.button(left_frame, "Back", lambda: callback_to.widgets2(), 5, 5, S)

    common_widgets.separator(right_frame, "horizontal", "x", 10)

    common_widgets.button(right_frame, "Commit changes", lambda *args: callback_to.commit("origin"), 5, 5, S)


def widgets2():  # Logos need to be preloaded, but that'll be done on a later release
    common_widgets.change_size(896, 175)
    common_widgets.label(frame, "Please select a platform for modification, you may also\n backup your current "
                                "configuration file or learn what these options do in more detail.", 5, 15, N, "center")

    common_widgets.image_button(right_frame, "Origin", self_path + "/logos/origin_logo.png", 22, 27, LEFT,
                                callback_to.origin, 5, 5, N)
    common_widgets.separator(right_frame, "horizontal", "x", 10)
    common_widgets.button(right_frame, "Options info", callback_to.widgets2_1, 5, 5)
    common_widgets.image_button(left_frame, "Epic", self_path + "/logos/epic.png", 35, 30, LEFT, callback_to.epic,
                                5, 5, N)
    common_widgets.separator(left_frame, "horizontal", "x", 10)
    common_widgets.button(left_frame, "Back", callback_to.widgets, 5, 5, S)
    common_widgets.image_button(frame, "Steam", self_path + "/logos/steam_logo.png", 25, 25, LEFT,
                                callback_to.steam, 5, 5, N)
    common_widgets.separator(frame, "horizontal", "x", 8)
    common_widgets.button(frame, "Backup current configuration", json_file.backup, 5, 5, S)


def widgets2_1():  # Options info
    common_widgets.change_size(900, 230)

    def print_injection():
        lbl_var.set("Injection is, in essence, a way to force a program to run custom code by loading a custom DLL onto"
                    " it.\n  Disabling this will effectively \"turn off\" Koalageddon for the selected platform. \n"
                    "-\nYou may enable or disable this behaviour")

    def print_replication():
        lbl_var.set("Replication is the method by which Koalageddon injects itself onto the child processes\n"
                    "(the programs that the selected platform creates) of the main injection target.\n"
                    "This can be useful if a certain child process requires injection for effective DLC unlocking.\n"
                    "-\nYou may enable or disable this behaviour.")

    def print_blacklist():
        lbl_var.set("Blacklisting is the method by which certain DLC\'s are blocked, this can be useful\n"
                    " if a certain DLC activates a low violence mode, another language, a certain difficulty, etc.\n"
                    "The GUI makes use of an ordered list to deal with blacklisting or removal from same,\n as such, "
                    "every single order given will be recorded and executed on commit, please bare that in mind\n"
                    "-\nYou may input the desired DLC, Item or App IDs and remove them from or include them in the "
                    "Blacklist")

    common_widgets.button(frame, "Return", callback_to.widgets2, 5, 10, N)
    common_widgets.separator(frame, "horizontal", "x", 5)
    lbl_var = StringVar()
    lbl_var.set("Please select an option")  # Default value
    lbl = ttk.Label(frame, textvariable=lbl_var, justify="center")
    lbl.pack(padx=5, pady=5)
    common_widgets.separator(left_frame, "horizontal", "x", 5)
    common_widgets.button(left_frame, "Injection", print_injection, 5, 5, SW)
    common_widgets.separator(low_frame, "horizontal", "x", 5)
    common_widgets.button(low_frame, "Replication", print_replication, 5, 5, S)
    common_widgets.separator(right_frame, "horizontal", "x", 5)
    common_widgets.button(right_frame, "Blacklisting", print_blacklist, 5, 5, SE)


def commit_changes(platform):
    if platform == "steam":
        # Not very pretty now is it?
        global enable_steam, replicate_steam, blacklist_steam, ids_steam

        if not var_en_steam:
            enable_steam = "Skip"
        else:
            if var_en_steam == "enable":
                enable_steam = True
            else:
                enable_steam = False
        if not var_rep_steam:
            replicate_steam = "Skip"
        else:
            if var_rep_steam == "enable":
                replicate_steam = True
            elif var_rep_steam == "disable":
                replicate_steam = False
        if not var_blacklist_steam:
            blacklist_steam = False
        else:
            blacklist_steam = var_blacklist_steam

        if not appid or appid == "AppID":
            ids_steam = False
        else:
            ids_steam = appid

        preview_ask = messagebox.askyesnocancel("Preview", "Do you wish to preview the changes?")

        if preview_ask is True:  # Buggy if many IDs have been added.
            preview_window.show("steam")
        if preview_ask is False:
            json_file.commit("steam")
        if preview_ask is None:
            callback_to.steam()

    elif platform == "epic":
        global enable_epic, replicate_epic, blacklist_epic, ids_epic

        if not var_en_epic:
            enable_epic = "Skip"
        else:
            if var_en_epic == "enable":
                enable_epic = True
            else:
                enable_epic = False
        if not var_rep_epic:
            replicate_epic = "Skip"
        else:
            if var_rep_epic == "enable":
                replicate_epic = True
            elif var_rep_epic == "disable":
                replicate_epic = False
        if not var_blacklist_epic:
            blacklist_epic = False
        else:
            blacklist_epic = var_blacklist_epic

        if not dlc_id or dlc_id == "DLC ID":
            ids_epic = False
        else:
            ids_epic = dlc_id

        preview_ask = messagebox.askyesnocancel("Preview", "Do you wish to preview the changes?")

        if preview_ask is True:  # Buggy if many IDs have been added.
            preview_window.show("epic")
        if preview_ask is False:
            json_file.commit("epic")
        if preview_ask is None:
            callback_to.epic()

    elif platform == "origin":
        global enable_origin, replicate_origin, blacklist_origin, ids_origin

        if not var_en_origin:
            enable_origin = "Skip"
        else:
            if var_en_origin == "enable":
                enable_origin = True
            else:
                enable_origin = False
        if not var_rep_origin:
            replicate_origin = "Skip"
        else:
            if var_rep_origin == "enable":
                replicate_origin = True
            elif var_rep_origin == "disable":
                replicate_origin = False
        if not var_blacklist_origin:
            blacklist_origin = False
        else:
            blacklist_origin = var_blacklist_origin

        if not item_id or item_id == "Item ID":
            ids_origin = False
        else:
            ids_origin = item_id

        preview_ask = messagebox.askyesnocancel("Preview", "Do you wish to preview the changes?")

        if preview_ask is True:  # Buggy if many IDs have been added.
            preview_window.show("origin")
        if preview_ask is False:
            json_file.commit("origin")
        if preview_ask is None:
            callback_to.origin()


# Start #
if __name__ == '__main__':
    main_window()
