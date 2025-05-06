# Animal Happiness Raspberry Pi

![Python](https://img.shields.io/badge/python-3.9+-blue.svg) ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?logo=raspberrypi&logoColor=white) ![GPIO](https://img.shields.io/badge/GPIO-enabled-green)

## Overview

This repository contains the Raspberry Pi code for the Animal Happiness system, which measures dairy cow affective states through an interactive game. The system displays visual cues, captures cow responses through button presses, and logs the data to a cloud database for analysis.

## Features

- **Interactive Game**: Displays randomized visual cues to cows
- **Response Tracking**: Records optimistic or pessimistic button presses
- **Reward System**: Controls a motor to dispense appropriate food rewards
- **Audio Cues**: Plays bell sounds to attract cows at regular intervals
- **Real-time Data Transmission**: Sends response data to the cloud backend

## Hardware Requirements

**Note for IDC Students**: All hardware components should already be provided to you. You do not need to purchase any new components.

Required components (already included in your project kit):

- Raspberry Pi 3 Model B+ (pre-configured)
- Screen (16x14-inch) - **Required for running the program**
- Speakers (integrated in monitor)
- Push buttons (already connected to GPIO pins)
- Motor for food dispensing
- Appropriate power supply

## GPIO Configuration

- **Button 1 (Optimistic)**: GPIO 5
- **Button 2 (Pessimistic)**: GPIO 6
- **Motor Control**: GPIO 23
- **Animal Sensor**: GPIO 21

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ahidvt/animal-happiness-raspberrypi.git
   cd animal-happiness-raspberrypi
   ```

2. Install dependencies:

   ```bash
   pip3 install pygame RPi.GPIO requests
   ```

3. Configure API credentials directly in `post_animal_data.py` file:

   ```python
   # Configuration
   API_URL = "your_backend_api_url"  # Replace with actual URL
   API_KEY = "your_api_key"          # Replace with actual key
   ```

   **Note for IDC Students**: These values should already be filled in for you in the provided Pi.

4. Ensure the audio file is in the correct location:
   ```
   /home/animalvideogame/BellSoundCue.wav
   ```

## Usage

### Main Application

**For IDC Students**: Simply open the AnimalVideoGame.py file and click the run button on the screen. A screen is required for the application to run properly, otherwise it will throw an error.

For manual execution:

```bash
python3 AnimalVideoGame.py
```

This will:

1. Initialize the display with a white background
2. Play the bell sound every 30 seconds
3. Display random color cues when an animal is detected
4. Process button presses and control the motor
5. Send data to the backend API

### Data Posting Utility

The `post_animal_data.py` script can be used separately to test API connectivity:

```bash
# Send a test response
python3 post_animal_data.py --once --cow_id="cow123" --response="optimistic"

# Continuously post at specific intervals
python3 post_animal_data.py --interval=30
```

#### Command Line Options:

- `--cow_id`: Specify a cow ID (default: "N/A")
- `--response`: Set response type ("optimistic" or "pessimistic")
- `--interval`: Set seconds between posts (default: 20)
- `--once`: Send a single post and exit

## System Operation

1. The system plays a bell sound every 30 seconds to attract cows
2. A button is pressed manually to start the game, which displays a random color on the screen
   (Note: Automatic animal detection is a future goal)
3. If the cow presses the optimistic button, the motor runs for 15 seconds
4. If the cow presses the pessimistic button, the motor runs for 5 seconds
5. Response data is sent to the backend for analysis in real-time
6. If no response is received within 30 seconds, the display returns to default

## Troubleshooting

- If buttons aren't responding, check GPIO connections
- For API connection issues, verify credentials in `post_animal_data.py`
- Check `animal_data_poster.log` for error messages
- Ensure the Raspberry Pi has internet connectivity

## Contributors

Developed by Bryce Eller and Dhruv Varshney of the Animal Happiness Team at Virginia Tech as part of the Interdisciplinary Design Capstone (IDC) 2024 - 2025.

For questions, contact dhruvvarshney@vt.edu or message on LinkedIn: https://www.linkedin.com/in/dvar/
