import tkinter
from tkinter import StringVar, messagebox, ttk
from typing import cast

from pyautogui import FailSafeException

from db.add_test import add_test
from db.get_items_problems import get_items
from db.get_overall_results import get_overall_results
from design.Item import Item
from design.Job import Job
from design.Problem import Problem
from design.Script import Script
from design.Test import ScriptError, Test
from gui.actions import complete_test, turn_off_capslock
from pages.Page import Page
from popups.JobPopup import JobPopup
from popups.OptionSelectPopup import OptionSelectPopup
from popups.ScriptSelectionPopup import ScriptSelectionPopup
from popups.Tooltip import Tooltip


class TestPage(Page):
    def setup(self) -> None:
        ttk.Button(self.frame, text="< Problems", command=lambda: self.change_page("PROBLEM")).grid(column=0, row=0, sticky="w")

        ttk.Label(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        item_number = StringVar(value=self.shared.previous_item_number)
        item_entry = ttk.Entry(self.frame, textvariable=item_number)
        item_entry.grid(column=2, row=1, sticky="w", columnspan=2)
        item_entry.focus()
        item_entry.icursor(tkinter.END)
        self.go_button = ttk.Button(self.frame, text="Go", command=lambda: self.get_items(item_number.get(), item_entry))
        item_entry.bind("<Return>", lambda _: self.go_button.invoke())
        self.go_button.grid(column=0, row=2, columnspan=2)
        self.choose_button = ttk.Button(self.frame, text="Choose", command=lambda: self.get_items(item_number.get(), item_entry, choose_script=True))
        self.choose_button.grid(column=2, row=2)
        button_state = "normal" if item_number.get() in self.shared.item_number_to_description else "disabled"
        self.edit_button = ttk.Button(self.frame, text="Edit Test", command=lambda: self.get_items(item_number.get(), item_entry, editing=True), state=button_state)
        self.edit_button.grid(column=3, row=2)

        item_number.trace_add("write", lambda _, __, ___: self.edit_button_reconfigure(item_number))

    def edit_button_reconfigure(self, item_number: StringVar) -> None:
        tested = item_number.get() in self.shared.item_number_to_description
        self.edit_button.configure(state=("normal" if tested else "disabled"))

    def get_items(self, item_number: str, item_entry: ttk.Entry, /, *, choose_script: bool = False, editing: bool = False) -> None:
        item_entry.state(["disabled"])  # pyright: ignore
        self.frame.focus()
        assert self.shared.problem

        if editing and item_number not in self.shared.item_number_to_description:
            return self.item_not_found(item_number)

        items = get_items(item_number)
        if not items:
            return self.item_not_found(item_number)
        self.is_editing = editing
        if len(items) == 1:
            return self.get_test(items[0], choose_script=choose_script)

        popup = OptionSelectPopup(self.frame, items, lambda item: self.get_test(item, choose_script=choose_script))
        popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(item_number))

    def get_test(self, item: Item, *, choose_script: bool = False) -> None:
        self.shared.item_number_to_description[item.number] = item.description
        if self.is_editing:
            assert self.shared.problem
            try:
                test = next(test for test in reversed(self.shared.problem.tests) if test.item.number == item.number)
            except StopIteration:
                return self.item_not_found(item.number)

        else:
            test = Test(item)

        try:
            if choose_script:
                raise ScriptError
            script = test.determine_script()
            return self.display_test(script, test)
        except ScriptError:
            pass

        script_popup = ScriptSelectionPopup(self.frame, lambda s: self.display_test(s, test))
        script_popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(item.number))
        script_popup.mainloop()

    def display_test(self, script: Script, test: Test) -> None:
        assert self.shared.problem
        test.script = script
        self.test = test
        self.choose_button.destroy()
        self.edit_button.destroy()
        self.go_button.configure(text="Cancel", command=lambda: self.reset_page(test.item.number))
        self.go_button.grid(column=0, row=2, columnspan=4)

        # displaying the item and problem
        item_label = ttk.Label(self.frame, text=f"{test.item}")
        item_label.grid(column=0, row=3, columnspan=4)
        Tooltip(item_label, test.item.full_info)
        problem_label = ttk.Label(self.frame, text=f"{self.shared.problem.campus}")
        problem_label.grid(column=0, row=4, columnspan=4)
        Tooltip(problem_label, str(self.shared.problem))
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=5, columnspan=4)

        # displaying the script
        row = 6
        script = self.test.script
        ttk.Label(self.frame, text=f"{script.name}").grid(column=0, row=row, columnspan=4)
        row += 1

        if test.script_answers:
            self.saved_script_answers = test.script_answers
        else:
            stored_answers = self.shared.storage.item_model_to_script_answers.get(self.test.item_model)
            self.saved_script_answers = stored_answers or [stest.selected for stest in script.lines]
        actual_answers = [StringVar(value=ans) for ans in self.saved_script_answers]
        for i, line in enumerate(script.lines):
            label = ttk.Label(self.frame, text=line.text, width=10)
            Tooltip(label, text=line.text)
            label.grid(column=0, row=row, columnspan=1, sticky="w")
            if len(line.options) <= 1:
                ttk.Entry(self.frame, textvariable=actual_answers[i]).grid(column=1, row=row, columnspan=3, sticky="w")
            else:
                for j, option in enumerate(line.options):
                    rb = ttk.Radiobutton(self.frame, text=option, variable=actual_answers[i], value=option)
                    rb.grid(column=1 + j, row=row)
                    if option == self.saved_script_answers[i]:
                        rb.invoke()
            row += 1
        self.frame.rowconfigure(row, minsize=10)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=row, columnspan=4)
        row += 1

        # adding jobs
        self.add_job_button = ttk.Button(self.frame, text="Add Job", command=self.add_job)
        self.delete_job_button = ttk.Button(self.frame, text="X", width=1, command=self.delete_job)
        self.add_job_button.grid(column=0, row=row, columnspan=4)
        if len(self.test.jobs):
            self.add_job_button.configure(text=f"Add Job ({len(self.test.jobs)})")
            self.delete_job_button.grid(column=3, row=self.add_job_button.grid_info()["row"], sticky="e")
        row += 1

        # test comment
        ttk.Label(self.frame, text="Comment").grid(column=0, row=row, columnspan=4)
        row += 1
        self.comment = tkinter.Text(self.frame, height=4, width=100)
        if self.test.comment:
            self.comment.insert(tkinter.END, self.test.comment + "\n\n")
        self.comment.grid(column=0, row=row, columnspan=4)
        row += 1
        self.frame.rowconfigure(row, minsize=10)
        row += 1

        # final results
        ttk.Label(self.frame, text="Result").grid(column=0, row=row, columnspan=4)
        row += 1
        overall_results = get_overall_results(self.shared.problem.customer_number)
        result = tkinter.StringVar(value=self.test.final_result or overall_results[0].fullname)
        for i, (nickname, fullname) in enumerate(overall_results):
            button = ttk.Radiobutton(self.frame, text=nickname, variable=result, value=fullname, width=15)
            Tooltip(button, fullname)
            button.grid(column=i % 4, row=row, columnspan=1)
            row = row + 1 if i % 4 == 3 else row
        row += 1

        save = ttk.Button(self.frame, text="Save", command=lambda: self.save_test([s.get() for s in actual_answers], result.get()))
        save.grid(column=0, row=row, columnspan=4)
        save.focus()
        save.bind("<Return>", lambda _: self.save_test([s.get() for s in actual_answers], result.get()))
        row += 1

    def add_job(self) -> None:
        assert self.shared.problem is not None
        job_popup = JobPopup(self.frame, self.shared.problem.department, self.shared.problem.company, self.save_job)
        job_popup.mainloop()

    def save_job(self, job: Job) -> None:
        self.comment.insert(tkinter.END, job.test_comment + "\n\n")
        self.test.add_job(job)
        self.shared.job_manager.add_job(self.test.item, cast(Problem, self.shared.problem), job)
        self.add_job_button.configure(text=f"Add Job ({len(self.test.jobs)})")
        self.delete_job_button.grid(column=3, row=self.add_job_button.grid_info()["row"], sticky="e")

    def delete_job(self) -> None:
        job = self.test.jobs.pop()
        self.shared.job_manager.delete_job(cast(Problem, self.shared.problem), job)
        current_comment = self.comment.get("1.0", tkinter.END).strip()
        self.comment.delete("1.0", tkinter.END)
        self.comment.insert(tkinter.END, current_comment.replace(job.test_comment, ""))

        add_job_text = "Add Job"
        if not self.test.jobs:
            self.delete_job_button.grid_forget()
        else:
            add_job_text += f" ({len(self.test.jobs)})"
        self.add_job_button.configure(text=add_job_text)

    def save_test(self, script_answers: list[str], result: str) -> None:
        assert self.shared.problem  # must have created a problem by now
        turn_off_capslock()
        comment = self.comment.get("1.0", tkinter.END)
        self.test.complete(comment, result, script_answers)
        if self.is_editing:
            self.shared.problem.remove_test(self.test)
        self.shared.problem.add_test(self.test)

        try:
            add_test(self.test, self.shared.problem)
            complete_test(self.test, self.shared.storage.positions, self.is_editing)
        except FailSafeException:
            test = self.shared.problem.tests.pop()
            self.shared.problem.test_breakdown[test.script.nickname] -= 1
            for _ in test.jobs:
                self.shared.job_manager.problem_to_jobs[self.shared.problem].pop()
            return self.failsafe(self.test.item.number)

        with self.shared.storage.edit() as storage:
            storage.total_tests += 1
            storage.test_breakdown[self.test.script.nickname] = storage.test_breakdown.get(self.test.script.nickname, 0) + 1

        if self.test.item.model not in (".", " ", "", "-", self.test.item.description, self.test.script.nickname):
            self.update_storage(script_answers)

        self.reset_page(self.test.item.number)

    def reset_page(self, item_number: str) -> None:
        self.shared.previous_item_number = item_number
        self.change_page("TEST")

    def update_storage(self, actual_script_answers: list[str]) -> None:
        if self.saved_script_answers == actual_script_answers:
            return

        default = [stest.selected for stest in self.test.script.lines]
        with self.shared.storage.edit() as storage:
            if actual_script_answers == default:
                del storage.item_model_to_script_answers[self.test.item_model]
            else:
                storage.item_model_to_script_answers[self.test.item_model] = actual_script_answers

    def failsafe(self, current_item_number: str) -> None:
        messagebox.showerror("Process Aborted", "Fail safe activated")  # pyright: ignore
        self.reset_page(current_item_number)

    def item_not_found(self, current_item_number: str) -> None:
        messagebox.showerror("Not Found", f"Item number '{current_item_number}'")  # pyright: ignore
        self.reset_page(current_item_number)
