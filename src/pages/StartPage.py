from tkinter import ttk
from typing import Literal

from automations import get_click_position
from pages.Page import Page


class StartPage(Page):
    def setup(self):
        ttk.Label(self.frame, text="Start Page").grid(column=0, row=0)
        self.test_button = ttk.Button(self.frame, text="Click here then on Testing tab", command=lambda: self.click_position("TESTING"))
        self.test_button.grid(column=0, row=1)

        self.assets_button = ttk.Button(self.frame, text="Click here then on Assets tab", command=lambda: self.click_position("ASSETS"))
        self.assets_button.grid(column=0, row=2)

        self.area_button = ttk.Button(self.frame, text="Click here then on Area Script", command=lambda: self.click_position("AREA"))
        self.area_button.grid(column=0, row=3)

        self.comments_button = ttk.Button(self.frame, text="Click here then on Comments box", command=lambda: self.click_position("COMMENTS"))
        self.comments_button.grid(column=0, row=4)

    def click_position(self, tab: Literal["ASSETS", "TESTING", "AREA", "COMMENTS"]) -> None:
        return self.change_page("TEST", assets_position=(0, 0), testing_position=(0, 0), area_position=(0, 0), comments_position=(0, 0))

        position = get_click_position()
        if tab == "ASSETS":
            self.assets_position = position
            self.assets_button.configure(text="Done", state="disabled")
        elif tab == "TESTING":
            self.testing_position = position
            self.test_button.configure(text="Done", state="disabled")
        elif tab == "AREA":
            self.area_position = position
            self.area_button.configure(text="Done", state="disabled")
        elif tab == "COMMENTS":
            self.comments_position = position
            self.comments_button.configure(text="Done", state="disabled")

        if all(hasattr(self, f"{tab.lower()}_position") for tab in ["ASSETS", "TESTING", "AREA", "COMMENTS"]):
            self.change_page("TEST", assets_position=self.assets_position, testing_position=self.testing_position, area_position=self.area_position, comments_position=self.comments_position)


