# HSR Speed Threshold Calculator

A lightweight GUI tool for Honkai: Star Rail that calculates the minimum Speed required for a character to achieve a desired number of actions within a given number of turns, under different game modes and advance effects.

The calculator is designed to be simple, fast, and transparent, with all inputs visible at once.

# How It Works 

- The first turn uses a base action value

- Additional turns add incremental action value

- Advance effects are converted into action value internally

- The tool computes the minimum Speed such that:

```
Speed × total_action_value + total_advance ≥ required_action_value
```

- The final output is the minimum required Speed (rounding up)

# Installation & Usage
**Requirements**

- Python 3.9+ recommended

- No additional libraries required (uses built-in tkinter)

Run the program
```
python hsr_speed_calculator.py

```

A small window will open with all inputs available at once.

# Input Guide
- Mode:
  - Forgotten Hall: The first turn has an action value of 150, and each subsequent turn adds 100.
  - Anomaly Arbitration: The first turn has an action value of 300, and each subsequent turn adds 100.

- Total Turns: The total number of turns being considered.

  For example:
  - 2 actions in 1 turn

  - 4 actions in 2 turns

  - 3 actions in 1 turn
 
  - The second number in each example corresponds to Total Turns.
    
  Note: the first turn is counted as 1 (there is no turn 0).

- Target Actions: The total number of actions you want the character to perform within the specified number of turns.


- Wind: The number of times your Wind relic can trigger. Enter this as an integer.

- Vonwacq: Whether the character has Vonwacq equipped. If present, it is applied once.

- Custom 1–6: Custom advance sources other than Wind and Vonwacq. These can be used for effects such as Dance Dance Dance, with values adjusted based on Superimposition.

```
24 → interpreted as 0.24

0.24 → interpreted as 0.24

0 or blank → no advance
```

# Output

- The calculator displays only:
  - Minimum required Speed: XXX


- This value already accounts for:
  - Mode

  - Turn structure
    
  - All advance effects
    
  - Ceiling behavior

# Project Structure
```
hsr-speed-calculator/
│
├── hsr_speed_gui.py
├── README.md
└── .gitattributes
```
# Notes

- This tool does not validate in-game feasibility (e.g. relic limits)

- It focuses purely on turn math and advance mechanics

- Intended as a planning and theorycrafting aid

# License

- This project is provided for personal and educational use.
  
- Not affiliated with or endorsed by HoYoverse.
