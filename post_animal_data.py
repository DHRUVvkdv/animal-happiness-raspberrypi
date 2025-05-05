#!/usr/bin/env python3
import requests
import time
import random
import json
import logging
import uuid
import argparse
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("animal_data_poster.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configuration
API_URL = "<REPLACE WITH BACKEND API_URL>"
API_KEY = "<REPLACE WITH BACKEND API_KEY>"
INTERVAL_SECONDS = 20  # Post data every 20 seconds

# Response types
RESPONSE_TYPES = ["optimistic", "pessimistic"]


def generate_animal_data(cow_id=None, response_type=None):
    """
    Generate animal data with specified or random values.

    Args:
        cow_id (str, optional): Specific cow ID to use. If None, one will be generated.
        response_type (str, optional): Specific response type to use. If None, one will be randomly chosen.

    Returns:
        dict: The generated animal data.
    """
    # Generate current time in ISO 8601 format with local timezone
    current_time = datetime.now().astimezone().isoformat()

    # Use provided cow_id or generate one
    if cow_id is None:
        # Decide whether to use a fixed ID or generate a random one (50% chance)
        if random.random() < 0.5:
            cow_id = random.choice(["cow1", "cow2", "cow3"])
        else:
            # Generate a random cow ID
            cow_id = str(random.randint(100, 999))

    # Use provided response_type or generate one
    if response_type is None:
        response_type = random.choice(RESPONSE_TYPES)

    return {
        "cow_id": cow_id,
        "response_type": response_type,
        "time": current_time,
        "metadata": None,  # Added for future expandability, set to null by default
        "source": "Raspberry Pi",
    }


def post_animal_data(cow_id=None, response_type=None):
    """
    Generate and post animal data to the API.

    Args:
        cow_id (str, optional): Specific cow ID to use.
        response_type (str, optional): Specific response type to use.

    Returns:
        bool: Success status of the post operation.
    """
    try:
        # Generate animal data with specified or random values
        animal_data = generate_animal_data(cow_id, response_type)

        # Post data
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json",
            "accept": "application/json",
        }

        logger.info(
            f"Posting data for {animal_data['cow_id']} with response type: {animal_data['response_type']}"
        )

        response = requests.post(
            f"{API_URL}/animal/data", headers=headers, json=animal_data
        )

        if response.status_code in [200, 201]:
            logger.info(
                f"Successfully posted data for {animal_data['cow_id']}: {response.text[:100]}..."
            )
            return True
        else:
            logger.error(
                f"Failed to post data: Status {response.status_code}, Response: {response.text}"
            )
            return False

    except Exception as e:
        logger.error(f"Error posting animal data: {e}")
        return False


def run_interval_posting(cow_id, response_type, interval):
    """
    Run continuous interval-based posting of animal data.

    Args:
        cow_id (str): The cow ID to use in all posts
        response_type (str): The response type to use in all posts
        interval (int): Seconds between posts
    """
    logger.info(
        f"Starting interval posting with cow_id={cow_id}, response_type={response_type}, interval={interval}s"
    )

    # Post immediately on startup
    post_result = post_animal_data(cow_id, response_type)
    logger.info(f"Initial post result: {'Success' if post_result else 'Failed'}")

    # Continue with regular posting
    while True:
        try:
            time.sleep(interval)
            post_result = post_animal_data(cow_id, response_type)
            logger.info(f"Posting result: {'Success' if post_result else 'Failed'}")
        except Exception as e:
            logger.error(f"Error in interval posting: {e}")
            # Wait a bit and continue rather than crashing
            time.sleep(5)


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Post animal data to API.")
    parser.add_argument("--cow_id", default="N/A", help="Cow ID to use (default: N/A)")
    parser.add_argument(
        "--response",
        choices=RESPONSE_TYPES,
        help="Response type to use (optimistic or pessimistic)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=INTERVAL_SECONDS,
        help=f"Interval between posts in seconds (default: {INTERVAL_SECONDS})",
    )
    parser.add_argument(
        "--once", action="store_true", help="Post once and exit (for testing)"
    )
    args = parser.parse_args()

    # Use command line arguments
    cow_id = args.cow_id
    response_type = args.response
    interval = args.interval

    # For testing - post once and exit if --once flag is used
    if args.once:
        logger.info(f"Posting once with cow_id={cow_id}, response_type={response_type}")
        post_result = post_animal_data(cow_id, response_type)
        logger.info(f"Post result: {'Success' if post_result else 'Failed'}")
        return

    # Otherwise run the continuous interval posting
    run_interval_posting(cow_id, response_type, interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Stopping animal data poster")
