from typing import Literal


class StepperBar:
    """
    A stepper bar component for Streamlit.

    The code is based on https://malik-sunny18.medium.com/stepper-bar-in-snowflake-streamlit-82041f1f275a
    """

    def __init__(
        self,
        steps: list[str],
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        active_color: str = "red",
        completed_color: str = "blue",
        inactive_color: str = "gray",
    ) -> None:
        self.current_step: int = 0
        self.orientation: str = orientation
        self.active_color: str = active_color
        self.completed_color: str = completed_color
        self.inactive_color: str = inactive_color
        self.steps: list[str] = steps

    def set_current_step(self, step: int) -> None:
        if 0 <= step < len(self.steps):
            self.current_step = step
        else:
            raise ValueError("Step index out of range")  # noqa: EM101

    def display(self) -> str:
        if self.orientation == "horizontal":
            return self._display_horizontal()
        if self.orientation == "vertical":
            return self._display_vertical()
        raise ValueError("Orientation must be either 'horizontal' or 'vertical'")  # noqa: EM101

    def _display_horizontal(self) -> str:
        stepper_html = "<div style='display:flex; justify-content:space-between; align-items:center;'>"
        for i, step in enumerate(self.steps):
            color = self.completed_color if i < self.current_step else self.inactive_color
            current_color = self.active_color if i == self.current_step else color
            stepper_html += f"""
            <div style='text-align:center;'>
                <div style='width:30px; height:30px; border-radius:50%; background-color:{current_color}; display:inline-block;'></div>
                <div>{step}</div>
            </div>"""
            if i < len(self.steps) - 1:
                stepper_html += f"<div style='flex-grow:1; height:2px; background-color:{self.inactive_color};'></div>"
        stepper_html += "</div>"
        return stepper_html

    def _display_vertical(self) -> str:
        stepper_html = "<div style='display:flex; flex-direction:column; align-items:flex-start;'>"
        for i, step in enumerate(self.steps):
            color = self.completed_color if i < self.current_step else self.inactive_color
            current_color = self.active_color if i == self.current_step else color
            stepper_html += f"""
            <div style='display:flex; align-items:center; margin-bottom:10px;'>
                <div style='width:30px; height:30px; border-radius:50%; background-color:{current_color}; margin-right:10px;'></div>
                <div>{step}</div>
            </div>"""
            if i < len(self.steps) - 1:
                stepper_html += f"<div style='width:2px; height:20px; background-color:{self.inactive_color}; margin-left:14px;'></div>"
        stepper_html += "</div>"
        return stepper_html
