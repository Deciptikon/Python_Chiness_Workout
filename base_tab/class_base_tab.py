class BaseTab:
    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str], nameTab: str = ' *** '):
        self.window = window
        self.notebook = notebook
        self.russ_words = russ_dict
        self.chin_words = chin_dict
        self.nameTab = nameTab
        self.selected_tab = 0
        self.window.bind('<Return>', self.enter_event)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def set_dicts(self, russ_dict: list[str], chin_dict: list[str]):
        self.russ_words = russ_dict
        self.chin_words = chin_dict

    # Действие нажатия на Enter
    def enter_event(self, event):
        pass

    # Действие при смене вкладки
    def on_tab_changed(self, event):
        self.selected_tab = self.notebook.index(self.notebook.select())
        print(f"Активная вкладка: {self.selected_tab}")
        self.window.focus_set()