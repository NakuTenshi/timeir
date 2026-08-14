#!/bin/python3
import datetime
import jdatetime
import json
import subprocess

# ANSI escape codes for terminal coloring
COLOR_CYAN = "\033[96m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

print("")
def print_colored_jcal():
    try:
        # Run the local jcal -3 command and capture its original English text
        result = subprocess.run(["jcal", "-3"], capture_output=True, text=True)
        output = result.stdout

        # Print the original calendar output in Cyan text
        print(f"{COLOR_CYAN}{output}{COLOR_RESET}")
    except FileNotFoundError:
        print(
            f"{COLOR_YELLOW}Warning: 'jcal' command not found. Please install libjalali.{COLOR_RESET}\n"
        )


def colorize_values(data):
    """Recursively walks through a dict/list to wrap dictionary values in Red color codes."""
    if isinstance(data, dict):
        # We manually build the JSON string structure for dict keys to avoid color string pollution
        items = []
        for key, val in data.items():
            formatted_key = f'"{key}"'
            formatted_val = colorize_values(val)
            items.append(f"{formatted_key}: {formatted_val}")
        return "{\n  " + ",\n  ".join(items).replace("\n", "\n  ") + "\n}"
    elif isinstance(data, list):
        items = [colorize_values(item) for item in data]
        return "[\n  " + ",\n  ".join(items).replace("\n", "\n  ") + "\n]"
    elif isinstance(data, str):
        # Wrap string values in quotes and apply red color
        return f'{COLOR_RED}"{data}"{COLOR_RESET}'
    else:
        # Fallback for numbers or booleans if any are added later
        return f"{COLOR_RED}{data}{COLOR_RESET}"


def print_colored_json():
    now = datetime.datetime.now()
    jnow = jdatetime.datetime.fromgregorian(datetime=now)

    weekdays = [
        "شنبه",
        "یکشنبه",
        "دوشنبه",
        "سه‌شنبه",
        "چهارشنبه",
        "پنج‌شنبه",
        "جمعه",
    ]
    months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "امرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]

    data = {
        "time": now.strftime("%H:%M:%S"),
        "dates": [
            {
                "title": "تاریخ خورشیدی",
                "date": jnow.strftime("%Y/%m/%d"),
                "date_text": f"{weekdays[jnow.weekday()]} - {jnow.day} {months[jnow.month-1]} {jnow.year}",
            },
            {
                "title": "تاریخ میلادی",
                "date": now.strftime("%Y-%m-%d"),
                "date_text": now.strftime("%A - %B %d, %Y"),
            },
        ],
    }

    # Generate custom JSON with red values only
    json_output = colorize_values(data)
    print(json_output)


if __name__ == "__main__":
    print_colored_jcal()
    print_colored_json()

