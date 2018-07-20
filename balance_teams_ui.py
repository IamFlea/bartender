# "Bug": when players have the same rating, premade teams are possibly assigned wrong in the ui

"""Provide a user interface for the balance_teams module."""
from argparse import ArgumentParser
from sys import platform
from tkinter import StringVar, Tk, ttk
from win32gui import FindWindow, GetForegroundWindow, GetWindowText, SetActiveWindow  # noqa: E501 flake8 to ignore too long line (only here because needs:) pylint: disable=no-name-in-module

from balance_teams import balance_teams
from aoc_lobby import Lobby
from pymemory import NullAddress
from pymemory import pymemory as pm


class BalanceTeamsUi:
    """Provide functions and data for the user interface and run it."""

    def __init__(self):
        """Initialize and run user interface."""
        self.size = [300, 0]
        # Parse arguments https://docs.python.org/3/library/argparse.html#module-argparse
        parser = ArgumentParser(
            description='Show an interface to sort players into two teams based on rating.')
        parser.add_argument('-autofill', action='store_true',
                            help='Update when players join or leave the lobby (HD Edition only)')
        parser.add_argument('-hide', action='store_true',
                            help='hide the window when AoE2 is not active (Windows only)')
        parser.add_argument('-toolwindow', action='store_true',
                            help='use a toolwindow (Windows only)')
        args = parser.parse_args()
        hide_when_aoe2_inactive = args.hide
        self.root = Tk()
        if args.toolwindow and platform == 'win32':
            self.root.attributes("-toolwindow", 1)
        self.root.attributes("-topmost", 1)
        self.root.title("Balance Teams")

        self.output = StringVar()
        self.mainframe = ttk.Frame(self.root, padding="5")
        self.draw_gui(args.autofill)

        self.root.bind("<Configure>", lambda e: BalanceTeamsUi.configure(self))

        BalanceTeamsUi.resize_win(self, 1)
        if hide_when_aoe2_inactive and platform == 'win32':
            self.root.after(0, BalanceTeamsUi.check_active_win, self, False)
        self.root.mainloop()

    def call_balance_teams(self, rating_var, team_var, output, team_output):
        """Calculate team balance and update the UI."""
        ratings = []
        premade_teams = []
        for i in range(8):
            rating = rating_var[i].get()
            if rating:
                ratings.append(int(rating))
                team_val = team_var[i].get()
                if not team_val:
                    team_val = 0
                premade_teams.append(int(team_val))
        try:
            team = balance_teams(ratings, premade_teams)
            output.set(f"Teams: {''.join(str(e) for e in team[0])}    Difference: {team[1]}")
            for i in range(8):
                if rating_var[i].get():
                    team_output[i].set(team[0].pop(0))
        except (TypeError, ValueError) as err:
            output.set(err)
            for i in range(8):
                team_output[i].set("")
        BalanceTeamsUi.resize_win(self)

    def check_active_win(self, hidden):
        """Hide window when AoE2 is not active, else restore it."""
        win = self.root
        fg_win = GetWindowText(GetForegroundWindow())
        if not (is_aoe2_win_text(fg_win) or fg_win == win.title()):
            if not hidden:  # and hide_when_aoe2_inactive:
                hidden = True
                win.withdraw()
        elif hidden:  # Restore
            hidden = False
            win.deiconify()
            aoe2_win_hwnd = find_aoe2_win()
            if aoe2_win_hwnd:
                SetActiveWindow(aoe2_win_hwnd)
        win.after(100, BalanceTeamsUi.check_active_win, self, hidden)

    def configure(self):
        """Save resizeing values of the window."""
        self.size = [self.root.winfo_width(), self.root.winfo_height()]

    def draw_gui(self, autofill):
        """Draw the balance_teams user interface."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=8)
        self.root.rowconfigure(1, weight=1)

        # style
        # style = ttk.Style()
        # style.configure("color.TLabelframe.Label", background="blue")
        # style.configure("Bold.TLabel", font=("TkDefaultFont", 9, "bold"))
        # print(s.theme_names())  # print available strings to use in theme_use()
        # ttk.Style().theme_use("xpnative")

        mainframe = self.mainframe
        mainframe.grid(column=0, row=0, sticky="nswe")
        self.draw_ui_elements(autofill)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=2, pady=2)
        for col in range(mainframe.grid_size()[0]):
            mainframe.columnconfigure(col, weight=0)
        for row in range(mainframe.grid_size()[1]):
            mainframe.rowconfigure(row, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(4, weight=1)

        outputframe = ttk.Frame(self.root, padding="7 0 7 7")
        outputframe.grid(column=0, row=1)
        self.output.set("Please provide ratings.")
        ttk.Label(outputframe, textvariable=self.output, anchor="center").grid(column=0, row=0)
        # ttk.Label(outputframe, textvariable=output, anchor="center",
        #           style="color.TLabelframe.Label").grid(column=0, row=0, sticky="nswe")

    def draw_ui_elements(self, autofill):
        """Create and assign ui elements."""
        heading = ["Player:", "Rating:", "Team:", "Premade:"]
        for i, elem in enumerate(heading):
            ttk.Label(self.mainframe, text=elem).grid(column=i, row=0, sticky="e")

        player_var = []
        player_label = []
        rating_var = []
        rating_entry = []
        team_output = []
        team_label = []
        team_var = []
        team_entry = []

        for i in range(8):
            row = i + 1
            player_var.append(StringVar())
            player_var[i].set("Player " + str(i + 1) + ":")
            player_label.append(ttk.Label(self.mainframe))
            player_label[i]['textvariable'] = player_var[i]
            player_label[i].grid(column=0, row=row, sticky="e")

            rating_var.append(StringVar())
            rating_var[i].trace("w", lambda name, index, mode:
                                BalanceTeamsUi.call_balance_teams(
                                    self, rating_var, team_var, self.output, team_output))
            rating_entry.append(ttk.Entry(self.mainframe, width=5, validate='key'))
            rating_entry[i]['textvariable'] = rating_var[i]
            rating_entry[i]['validatecommand'] = (rating_entry[i].register(is_digit), '%P')
            rating_entry[i].grid(column=1, row=row, sticky="we")

            team_output.append(StringVar())
            team_label.append(ttk.Label(self.mainframe))
            team_label[i]['textvariable'] = team_output[i]
            team_label[i].grid(column=2, row=row)

            team_var.append(StringVar())
            team_var[i].trace("w", lambda name, index, mode:
                              BalanceTeamsUi.call_balance_teams(
                                  self, rating_var, team_var, self.output, team_output))
            team_entry.append(ttk.Entry(self.mainframe, width=1, validate='key'))
            team_entry[i]['textvariable'] = team_var[i]
            team_entry[i]['validatecommand'] = (team_entry[i].register(is_team), '%P')
            team_entry[i].grid(column=3, row=row)

        rating_entry[0].focus()
        if autofill:
            BalanceTeamsUi.parse_lobby(self, player_var, rating_var, team_var, lobby=Lobby())

    def parse_lobby(self, player_var, rating_var, team_var, lobby):
        """Fill the ui with info about the players in an AoE2 lobby."""
        try:
            pm.load_process("AoK HD.exe")
        except ProcessLookupError as err:
            print(err)
            print("Autoparsing was disabled. Try restarting when AoE2HD is running.")
        else:
            try:
                lobby.update()
            except NullAddress:
                print("nulladdy")
            else:
                for i, player in enumerate(lobby.players):
                    if player.name is None:
                        if player_var[i-1].get():
                            player_var[i-1].set("")
                        if rating_var[i-1].get():
                            rating_var[i-1].set("")
                        if team_var[i-1].get():
                            team_var[i-1].set("")
                        continue
                    name = player.name.decode(encoding="utf-8", errors="replace")
                    # try:
                        # name = player.name.decode("utf-8")
                    # except UnicodeDecodeError:
                        # name = f"Player {player.number}"
                    player_var[player.number-1].set(name)
            self.root.after(1000, BalanceTeamsUi.parse_lobby, self, player_var, rating_var, team_var, lobby)

    def resize_win(self, center=None):
        """Resize the window to fit everything, centering optional."""
        win = self.root
        # Determine window size to fit all content
        win.update_idletasks()  # Update "requested size" from geometry manager
        req_w = win.winfo_reqwidth()
        req_h = win.winfo_reqheight()
        tmp_w = max(req_w, self.size[0])
        tmp_h = max(req_h, self.size[1])
        if center:  # Center window
            tmp_x = (win.winfo_screenwidth() - tmp_w) / 2
            tmp_y = (win.winfo_screenheight() - tmp_h) / 2
            geometry_str = f"{tmp_w}x{tmp_h}+{int(tmp_x)}+{int(tmp_y)}"
        else:
            geometry_str = f"{tmp_w}x{tmp_h}"
        win.geometry(geometry_str)
        win.minsize(req_w, req_h)


def find_aoe2_win():
    """Return the AoE2 window handle or 0 if it is not found."""
    win = FindWindow(None, "Age of Empires II: HD Edition")
    if not win:
        win = FindWindow(None, "Age of Empires II Expansion")
    return win


def is_aoe2_win_text(text):
    """Return True if text is usually used by AoE2 as a window title."""
    if (text == "Age of Empires II: HD Edition" or text == "Age of Empires II Expansion"):
        return True
    return False


def is_digit(content):
    """Validate entered rating is only digits."""
    if content.isdigit() or not content:
        return True
    return False


def is_team(team):
    """Validate entered team (needs to be 1-2 or empty)."""
    if not str(team) or (team.isdigit() and int(team) in range(1, 3)):
        return True
    return False


BalanceTeamsUi()
