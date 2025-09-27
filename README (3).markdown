# Travel Bot for Telegram 🌍

## 📋 Project Overview

This Telegram bot helps you explore cities around the world and their attractions. It also provides weather information and an engaging quiz. The bot is entirely my own work, developed as part of my CS projects.

Telegram Bot Link: [Click Here](https://t.me/your_bot_username)

## 🎯 Key Objectives
- Provide city attractions, history, and restaurant recommendations.
- Offer weather updates and interesting country facts.
- Include a fun travel quiz.
- Manage user settings for city and country.

## 🛠️ Tech Stack

| Category          | Tools/Technologies       | Purpose |
|-------------------|--------------------------|---------|
| **Bot Framework** | pyTelegramBotAPI        | Telegram bot handling |
| **AI Integration**| Yandex GPT              | Generating city info and facts |
| **Database**      | SQLite                  | User data storage |
| **Geolocation**   | Geopy                   | City coordinates |
| **HTTP Requests** | Requests                | API calls for weather |
| **Language**      | Python 3.9+             | Core scripting |

## 🏗️ Architecture

1. **User Input**: Commands to set city/country or request info.
2. **Data Retrieval**: Use GPT for facts/history, API for weather.
3. **Quiz Logic**: Random questions with keyboard options.
4. **Database**: Store user preferences and scores.
5. **Limits**: Max users and tokens for GPT usage.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Telegram Bot Token and Yandex GPT credentials

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TsMark01/travel_bot.git
   cd travel_bot
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Secrets**
   - Edit `super_secret.py` with your `TOKEN`.

4. **Run the Bot**
   ```bash
   python bot.py
   ```

### Usage Commands
- `/start`: Welcome message.
- `/menu`: Show all commands.
- `/help`: Detailed help.
- `/set_town`: Set current city.
- `/set_country`: Set country of interest.
- `/town_history`: City history.
- `/travel_help`: Attractions info.
- `/interesting_facts`: Country facts.
- `/city_restaurants`: Restaurant recommendations.
- `/weather`: Current weather.
- `/travel_quiz`: Start quiz.
- `/support`: Contact info.

## 📊 Features

- **Customizable Settings**: Set city and country.
- **AI-Generated Info**: History, facts, attractions via GPT.
- **Weather API**: Real-time weather.
- **Quiz**: Interactive travel questions.
- **User Limits**: Tokens and max users.

## 🧪 Testing

- Test commands in Telegram.
- Verify database updates and GPT responses.
- Check weather API with valid cities.

## 🔮 Future Enhancements

- Add more quiz questions.
- Integrate maps or images.
- Support multiple languages.

## 📝 Contributing

Fork and PR suggestions!