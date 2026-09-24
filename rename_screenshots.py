#!/usr/bin/env python3

import os
import random
import time

DESKTOP = os.path.expanduser("~/Desktop")

def get_screenshot_files():
    files = []

    for filename in os.listdir(DESKTOP):
        if filename.startswith("Screenshot") and filename.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
            files.append(filename)

    return files


def get_used_numbers():
    used = set()

    for filename in os.listdir(DESKTOP):
        name, _ = os.path.splitext(filename)

        if len(name) == 5 and name.isdigit():
            used.add(name)

    return used


def generate_filename(used):
    if len(used) >= 100000:
        raise RuntimeError("All 100,000 five-digit filenames are already used.")

    while True:
        number = f"{random.randint(0, 99999):05d}"

        if number not in used:
            return number


known_files = set(get_screenshot_files())

print("renamer is running...")
print("Press Ctrl+C to stop.")

while True:
    time.sleep(0.5)

    current_files = set(get_screenshot_files())
    new_files = current_files - known_files

    for filename in new_files:
        old_path = os.path.join(DESKTOP, filename)

        # Wait until macOS has finished writing the screenshot
        time.sleep(0.5)

        used = get_used_numbers()
        new_name = generate_filename(used)

        extension = os.path.splitext(filename)[1]
        new_path = os.path.join(DESKTOP, new_name + extension)

        os.rename(old_path, new_path)

        print(f"{filename} -> {new_name}{extension}")

    known_files = current_files
