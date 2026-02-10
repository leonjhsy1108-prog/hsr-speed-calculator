# hsr-speed-calculator

HSR Speed Threshold Calculator

A lightweight GUI tool for Honkai: Star Rail that calculates the minimum Speed required for a character to achieve a desired number of actions within a given number of turns, under different game modes and advance effects.

The calculator is designed to be simple, fast, and transparent, with all inputs visible at once.

Features

Supports Forgotten Hall and Anomaly Arbitration

Calculates minimum required Speed (ceiling)

Handles common advance sources:

Wind (integer trigger count, 0.25 per trigger)

Vonwacq (present / not present, triggers once)

6 custom advance slots (e.g. Dance Dance Dance at any Superimpose)

Custom advance inputs accept percent-style input

Example: entering 24 is automatically interpreted as 0.24

Clean GUI (no console input, no clutter)

No external dependencies beyond standard Python

How It Works (High-Level)

The first turn uses a base action value

Additional turns add incremental action value

Advance effects are converted into action value internally

The tool computes the minimum Speed such that:

Speed × total_action_value + total_advance ≥ required_action_value


The final output is always a single number:

Minimum required Speed

Installation & Usage
Requirements

Python 3.9+ recommended

No additional libraries required (uses built-in tkinter)

Run the program
python hsr_speed_gui.py


A small window will open with all inputs available at once.

Input Guide
Core Inputs

Mode

Forgotten Hall

Anomaly Arbitration

Total Turns

Total number of turns considered

Target Actions

Number of actions you want the character to take

Advance Inputs

Wind

Integer count of how many times Wind triggers

Vonwacq

Check if present (can only trigger once)

Custom 1–6

Enter advance values

You may enter:

24 → interpreted as 0.24

0.24 → interpreted as 0.24

0 or blank → no advance

Output

The calculator displays only:

Minimum required Speed: XXX


This value already accounts for:

Mode

Turn structure

All advance effects

Ceiling behavior

Project Structure
hsr-speed-calculator/
│
├── hsr_speed_gui.py
├── README.md
└── .gitattributes

Notes

This tool does not validate in-game feasibility (e.g. relic limits)

It focuses purely on turn math and advance mechanics

Intended as a planning and theorycrafting aid

License

This project is provided for personal and educational use.
Not affiliated with or endorsed by HoYoverse.