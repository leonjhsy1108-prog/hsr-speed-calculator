import math
import tkinter as tk
from tkinter import ttk, messagebox

WIND_PER_TRIGGER = 0.25
VONWACQ_ONCE = 0.40


def total_action_value(mode: str, total_turns: int) -> int:
    if total_turns < 1:
        raise ValueError("Total turns must be at least 1.")

    effective_turns = total_turns - 1

    if mode == "Anomaly Arbitration":
        return 300 + 100 * effective_turns
    return 150 + 100 * effective_turns


def parse_custom_advance(raw: str) -> float:
    """
    Accepts:
      24   -> 0.24
      0.24 -> 0.24
      0    -> 0.0
      blank -> 0.0
    """
    s = (raw or "").strip()
    if s == "":
        return 0.0
    v = float(s)
    if abs(v) >= 1.0:
        v = v / 100.0
    return v


def total_advance_action_value(
    wind_triggers: int,
    vonwacq_present: bool,
    custom_values: list[float],
) -> float:
    wind_total = wind_triggers * WIND_PER_TRIGGER
    von_total = VONWACQ_ONCE if vonwacq_present else 0.0
    return (wind_total + von_total + sum(custom_values)) * 10000.0


def compute_speed_threshold(
    target_actions: int,
    mode: str,
    total_turns: int,
    wind_triggers: int,
    vonwacq_present: bool,
    custom_values: list[float],
) -> int:
    if target_actions < 1:
        raise ValueError("Target actions must be at least 1.")
    if wind_triggers < 0:
        raise ValueError("Wind cannot be negative.")
    if len(custom_values) != 6:
        raise ValueError("Exactly 6 custom advance values are required.")

    action_value = total_action_value(mode, total_turns)
    total_advance = total_advance_action_value(
        wind_triggers, vonwacq_present, custom_values
    )

    return math.ceil((10000.0 * target_actions - total_advance) / action_value)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HSR Speed Threshold Calculator")
        self.resizable(False, False)

        pad = {"padx": 8, "pady": 6}

        # --- Core inputs ---
        core = ttk.LabelFrame(self, text="Core Inputs")
        core.grid(row=0, column=0, sticky="ew", **pad)

        ttk.Label(core, text="Mode:").grid(row=0, column=0, sticky="w", **pad)
        self.mode_var = tk.StringVar(value="Forgotten Hall")
        ttk.Combobox(
            core,
            textvariable=self.mode_var,
            values=["Forgotten Hall", "Anomaly Arbitration"],
            state="readonly",
            width=22,
        ).grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(core, text="Total Turns:").grid(row=1, column=0, sticky="w", **pad)
        self.turns_var = tk.StringVar(value="1")
        ttk.Entry(core, textvariable=self.turns_var, width=10).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(core, text="Target Actions:").grid(row=2, column=0, sticky="w", **pad)
        self.actions_var = tk.StringVar(value="2")
        ttk.Entry(core, textvariable=self.actions_var, width=10).grid(row=2, column=1, sticky="w", **pad)

        # --- Advance inputs ---
        adv = ttk.LabelFrame(self, text="Advance Inputs")
        adv.grid(row=1, column=0, sticky="ew", **pad)

        ttk.Label(adv, text="Wind:").grid(row=0, column=0, sticky="w", **pad)
        self.wind_var = tk.StringVar(value="0")  # DEFAULT = 0
        ttk.Entry(adv, textvariable=self.wind_var, width=10).grid(row=0, column=1, sticky="w", **pad)

        self.von_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(adv, text="Vonwacq", variable=self.von_var).grid(
            row=1, column=0, columnspan=2, sticky="w", **pad
        )

        # --- Custom advances ---
        custom = ttk.LabelFrame(self, text="Custom Advance Options")
        custom.grid(row=2, column=0, sticky="ew", **pad)

        self.custom_value_vars = []
        for i in range(6):
            ttk.Label(custom, text=f"Custom {i+1}:").grid(row=i, column=0, sticky="w", **pad)
            var = tk.StringVar(value="0")
            self.custom_value_vars.append(var)
            ttk.Entry(custom, textvariable=var, width=10).grid(row=i, column=1, sticky="w", **pad)

        # --- Bottom ---
        bottom = ttk.Frame(self)
        bottom.grid(row=3, column=0, sticky="ew", **pad)

        ttk.Button(bottom, text="Calculate", command=self.on_calculate).grid(row=0, column=0, **pad)
        ttk.Button(bottom, text="Reset", command=self.on_reset).grid(row=0, column=1, **pad)

        out = ttk.LabelFrame(self, text="Result")
        out.grid(row=4, column=0, sticky="ew", **pad)

        self.result_var = tk.StringVar(value="")
        ttk.Label(out, textvariable=self.result_var, font=("Segoe UI", 11)).grid(
            row=0, column=0, **pad
        )

    def on_reset(self):
        self.mode_var.set("Forgotten Hall")
        self.turns_var.set("1")
        self.actions_var.set("2")
        self.wind_var.set("0")   # RESET = 0
        self.von_var.set(False)
        for v in self.custom_value_vars:
            v.set("0")
        self.result_var.set("")

    def on_calculate(self):
        try:
            mode = self.mode_var.get()
            total_turns = int(self.turns_var.get())
            target_actions = int(self.actions_var.get())
            wind_triggers = int(self.wind_var.get())
            von_present = self.von_var.get()

            custom_vals = [parse_custom_advance(v.get()) for v in self.custom_value_vars]

            threshold = compute_speed_threshold(
                target_actions=target_actions,
                mode=mode,
                total_turns=total_turns,
                wind_triggers=wind_triggers,
                vonwacq_present=von_present,
                custom_values=custom_vals,
            )

            self.result_var.set(f"Required Speed to achieve the desired actions: {threshold}")


        except Exception as e:
            messagebox.showerror("Input error", str(e))


if __name__ == "__main__":
    App().mainloop()
