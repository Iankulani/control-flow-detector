# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  1 11:42:47 2025

@author: IAN CARTER KULANI
"""
from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("CONTROL FLOW DETECTOR")
print(Fore.GREEN+font)

import re

def parse_assembly(file_path):
    """
    Parse the given assembly file to extract instructions and their locations.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        instructions = []
        labels = []

        for line in lines:
            line = line.strip()

            # Detect labels in the assembly (usually ends with a colon, e.g., "loop_start:")
            label_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:$", line)
            if label_match:
                labels.append(label_match.group(1))

            # Store instruction with its line number
            instructions.append(line)

        return instructions, labels

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return [], []

def analyze_control_flow(instructions):
    """
    Analyze the control flow of the program by identifying key instructions.
    """
    control_flow_instructions = {
        "unconditional_jumps": [],
        "conditional_jumps": [],
        "function_calls": [],
        "function_returns": [],
        "loops": []
    }

    # Regular expressions for detecting control flow instructions
    unconditional_jump_pattern = re.compile(r"^\s*jmp\b", re.IGNORECASE)
    conditional_jump_pattern = re.compile(r"^\s*j(e|ne|g|l|ge|le|b|a|ae|be|c|z|nz)\b", re.IGNORECASE)
    function_call_pattern = re.compile(r"^\s*call\b", re.IGNORECASE)
    function_return_pattern = re.compile(r"^\s*ret\b", re.IGNORECASE)
    
    # Detect control flow instructions in the assembly code
    for line_number, line in enumerate(instructions, 1):
        if unconditional_jump_pattern.match(line):
            control_flow_instructions["unconditional_jumps"].append((line_number, line))
        elif conditional_jump_pattern.match(line):
            control_flow_instructions["conditional_jumps"].append((line_number, line))
        elif function_call_pattern.match(line):
            control_flow_instructions["function_calls"].append((line_number, line))
        elif function_return_pattern.match(line):
            control_flow_instructions["function_returns"].append((line_number, line))

    # Identify loops (typically characterized by labels and jumps)
    for line_number, line in enumerate(instructions, 1):
        if unconditional_jump_pattern.match(line) or conditional_jump_pattern.match(line):
            # Check if there is a corresponding label that indicates a loop (heuristic approach)
            for label in labels:
                if label in line:
                    control_flow_instructions["loops"].append((line_number, line, label))

    return control_flow_instructions

def print_control_flow_report(control_flow_instructions):
    """
    Print the control flow report with detected instructions.
    """
    print("\nControl Flow Analysis Report:")

    # Unconditional jumps
    print("\nUnconditional Jumps:")
    for line_number, instruction in control_flow_instructions["unconditional_jumps"]:
        print(f"Line {line_number}: {instruction}")

    # Conditional jumps
    print("\nConditional Jumps:")
    for line_number, instruction in control_flow_instructions["conditional_jumps"]:
        print(f"Line {line_number}: {instruction}")

    # Function calls
    print("\nFunction Calls:")
    for line_number, instruction in control_flow_instructions["function_calls"]:
        print(f"Line {line_number}: {instruction}")

    # Function returns
    print("\nFunction Returns:")
    for line_number, instruction in control_flow_instructions["function_returns"]:
        print(f"Line {line_number}: {instruction}")

    # Loops
    print("\nLoops (Jumps with associated labels):")
    for line_number, instruction, label in control_flow_instructions["loops"]:
        print(f"Line {line_number}: {instruction} (Looping to label {label})")

def main():
    # Ask the user for the assembly file path
    file_path = input("Enter the path of the assembly file:").strip()

    # Parse the assembly file to extract instructions and labels
    instructions, labels = parse_assembly(file_path)

    if not instructions:
        print("Failed to parse the assembly file.")
        return

    # Analyze the control flow of the program
    control_flow_instructions = analyze_control_flow(instructions)

    # Print the control flow analysis report
    print_control_flow_report(control_flow_instructions)

if __name__ == "__main__":
    main()
