# Bird Identifier Bot

A bot trained with Azure Custom Vision to identify birds in pictures shared on Twitter. When a picture of a bird is shared with the account @JakiToPtak, the bot responds with the name of the bird in Polish.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Overview](#file-overview)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Bird Identifier Bot is designed to identify birds from pictures shared on Twitter. When a user mentions @JakiToPtak with a picture, the bot processes the image using Azure Custom Vision and replies with the bird's name in Polish.

## Features

- **Image Recognition**: Uses Azure Custom Vision to identify birds from images.
- **Twitter Integration**: Listens to mentions of @JakiToPtak on Twitter.
- **Automated Responses**: Replies to tweets with the identified bird's name in Polish.

## Installation

### Prerequisites

- Python 3.8+
- Twitter Developer Account with API keys
- Azure Custom Vision Account with a trained model

### Steps

1. **Clone the Repository**:
   Open your terminal and clone the repository using the following command:
   ```bash
   git clone https://github.com/yourusername/bird-identifier-bot.git
   ```

2. **Navigate into the Project Directory**:
   Change your directory to the project folder:
   ```bash
   cd bird-identification-twitter-bot
   ```

3. **Create and Activate Virtual Environment**:
   It is recommended to use a virtual environment to manage dependencies.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install Dependencies**:
   Install the required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**:
   Create a `.env` file in the root directory of your project and add the following:
   ```env
   TWITTER_CONSUMER_KEY=your_consumer_key
   TWITTER_CONSUMER_SECRET=your_consumer_secret
   TWITTER_ACCESS_TOKEN_KEY=your_access_token_key
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   AZURE_CUSTOM_VISION_ENDPOINT=your_custom_vision_endpoint
   AZURE_CUSTOM_VISION_PREDICTION_KEY=your_prediction_key
   AZURE_CUSTOM_VISION_PROJECT_ID=your_project_id
   AZURE_CUSTOM_VISION_PUBLISHED_NAME=your_published_model_name
   ```

## Usage

To start the bot, run the following command:

```bash
python bot_custom_vision.py
```

The bot will begin listening to mentions of @JakiToPtak on Twitter. When a user tweets a picture of a bird to this account, the bot will analyze the image and respond with the bird's name in Polish.

### Example

User tweets:
```
@JakiToPtak Check out this bird!
```
The bot replies:
```
To jest sikorka (This is a titmouse).
```

## Configuration

The bot can be configured using the `.env` file. Here are the configuration options:

- **Twitter API keys**: These keys are necessary to interact with the Twitter API.
- **Azure Custom Vision settings**: These details are required to access your trained model on Azure Custom Vision.

## File Overview

- **model/**: Directory containing the custom vision model files.
- **tests/**: Directory containing unit tests for the project.
- **.gitignore**: Specifies files and directories to be ignored by git.
- **BirdBot.code-workspace**: VS Code workspace configuration.
- **birds.csv**: List of birds with columns 'Polish name', 'Scientific name'.
- **bot_custom_vision.py**: Main bot script integrating Twitter API and Azure Custom Vision.
- **database.py**: Script for database interactions (details needed).
- **fetch_and_download_images.py**: Python Selenium script for downloading bird images from Google Images based on `birds.csv`.
- **list_downloaded_species.py**: Script to cross-check which species have been downloaded.
- **Procfile**: File for declaring process types for deployment (e.g., Heroku).
- **README.md**: This README file.
- **requirements.txt**: List of dependencies required for the project.
- **scrape_wiki.py**: Script to scrape Wikipedia for a list of birds in Poland and export as `birds.csv`.
- **upload_images_and_tags.py**: Script to upload and tag images to Azure Custom Vision.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.