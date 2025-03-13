# AI Image Bot

This repository contains a Telegram bot built using the Pyrogram library that generates images based on user prompts using an AI image generation API.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/abirxdhack/AIARTGEN.git
    cd AIARTGEN
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Create a `config.py` file in the project directory and add the following configuration variables:

```python
# config.py

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
```

Replace the placeholder values with your actual API keys and tokens.

## Usage

To run the AI Image Bot, use the following command:
```sh
python ai_image_bot.py
```

## Commands

### AI Image Bot Commands

- `/ai <prompt>`: Generates images based on the provided prompt using an AI image generation API.
  
  **Example:**
  ```
  /ai Batman
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
