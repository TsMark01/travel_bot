from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from keyboard import menu, helpkey, travelhelp
import random
from super_secret import TOKEN
from config import MAX_GPT_TOKENS, MAX_USER_GPT_TOKENS, MAX_USERS
from database import Database
from yandexgpt import ask_gpt
from geopy.geocoders import Nominatim
import requests

bot = TeleBot(TOKEN)
db = Database()

def check_number_of_users(chat_id):
    """Check if the user limit has been exceeded."""
    count = db.count_users(chat_id)
    if count is None:
        return None, "Database error"
    if count > MAX_USERS:
        return None, "Maximum number of users exceeded"
    return True, ""

@bot.message_handler(commands=['start'])
def start(message):
    """Handle the /start command and welcome the user."""
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    db.add_user(chat_id)
    bot.send_message(
        chat_id,
        f"<b>Hello {user_name}👋, I'm Ford Prefect. Planet Earth turned out to be the most interesting in my journey across the galaxy, I've been to all cities and countries on Earth, and more—I've been to almost all galaxies. If you've read Hitchhiker's Guide to the Galaxy, you definitely remember me!\n If you're planning a trip, be sure to message me, and I'll tell you a lot about the city, its attractions, and restaurants. </b>\n\n"
        f"For more detailed information, type /help.\n"
        f"The /menu command will take you to the mode with all bot commands. "
        f"The /weather command will show you the weather in your city. "
        f"The /set_town command will set your current city. "
        f"The /set_country command will set your country of interest. "
        f"The /town_history command will tell the history of the city. "
        f"The /travel_help command will provide information about city attractions. "
        f"The /interesting_facts command will share 9 interesting facts about the user's country. "
        f"The /city_restaurants command will recommend restaurants in the city. "
        f"The /travel_quiz command will start a quiz about world cities.",
        parse_mode='HTML',
        reply_markup=menu
    )

@bot.message_handler(commands=['menu'])
def menu_func(message):
    """Handle the /menu command to show the main menu."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "All commands:", reply_markup=helpkey)

@bot.message_handler(commands=['help'])
def help_func(message):
    """Handle the /help command to provide detailed help."""
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Hello! I'm a travel bot. I can tell you about attractions in your city, weather, and much more. "
        "To start, set your city with /set_town and country with /set_country. "
        "For attractions, use /travel_help. "
        "For city history, use /town_history. "
        "For interesting facts about your country, use /interesting_facts. "
        "For restaurant recommendations, use /city_restaurants. "
        "For weather, use /weather. "
        "For a quiz, use /travel_quiz. "
        "For support, use /support.",
        reply_markup=helpkey
    )

@bot.message_handler(commands=['set_town'])
def set_town(message):
    """Prompt the user to set their city."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Enter your current city:")
    bot.register_next_step_handler(message, handle_message_for_city)

def handle_message_for_city(message):
    """Handle the city input and update the database."""
    chat_id = message.chat.id
    city = message.text
    db.update_city(city, chat_id)
    bot.send_message(chat_id, f"Your city is set to {city}.", reply_markup=helpkey)

@bot.message_handler(commands=['set_country'])
def set_country(message):
    """Prompt the user to set their country."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Enter the country you're interested in:")
    bot.register_next_step_handler(message, handle_message_for_country)

def handle_message_for_country(message):
    """Handle the country input and update the database."""
    chat_id = message.chat.id
    country = message.text
    db.update_country(country, chat_id)
    bot.send_message(chat_id, f"Your country of interest is set to {country}.", reply_markup=helpkey)

@bot.message_handler(commands=['town_history'])
def town_history(message):
    """Provide the history of the user's city using GPT."""
    chat_id = message.chat.id
    city = db.get_city(chat_id)
    if city:
        bot.send_message(chat_id, "Generating city history...")
        SYSTEM_PROMPT = [{'role': 'system', 'text': f"Tell the history of {city} in 3-5 sentences."}]
        status, answer, tokens_in_answer = ask_gpt(SYSTEM_PROMPT)
        if status:
            db.update_tokens(tokens_in_answer, chat_id)
            bot.send_message(chat_id, answer, reply_markup=helpkey)
        else:
            bot.send_message(chat_id, "Failed to generate history.")
    else:
        bot.send_message(chat_id, "Please set your city first with /set_town.")

@bot.message_handler(commands=['interesting_facts'])
def interesting_facts(message):
    """Provide interesting facts about the user's country using GPT."""
    chat_id = message.chat.id
    country = db.get_country(chat_id)
    if country:
        bot.send_message(chat_id, "Generating interesting facts...")
        SYSTEM_PROMPT = [{'role': 'system', 'text': f"Share 9 interesting facts about {country}."}]
        status, answer, tokens_in_answer = ask_gpt(SYSTEM_PROMPT)
        if status:
            db.update_tokens(tokens_in_answer, chat_id)
            bot.send_message(chat_id, answer, reply_markup=helpkey)
        else:
            bot.send_message(chat_id, "Failed to generate facts.")
    else:
        bot.send_message(chat_id, "Please set your country first with /set_country.")

@bot.message_handler(commands=['city_restaurants'])
def city_restaurants(message):
    """Recommend restaurants in the user's city using GPT."""
    chat_id = message.chat.id
    city = db.get_city(chat_id)
    if city:
        bot.send_message(chat_id, "Recommending restaurants...")
        SYSTEM_PROMPT = [{'role': 'system', 'text': f"Recommend top restaurants in {city}."}]
        status, answer, tokens_in_answer = ask_gpt(SYSTEM_PROMPT)
        if status:
            db.update_tokens(tokens_in_answer, chat_id)
            bot.send_message(chat_id, answer, reply_markup=helpkey)
        else:
            bot.send_message(chat_id, "Failed to recommend restaurants.")
    else:
        bot.send_message(chat_id, "Please set your city first with /set_town.")

@bot.message_handler(commands=['travel_help'])
def travel_help(message):
    """Provide travel help for the user's city using GPT."""
    chat_id = message.chat.id
    city = db.get_city(chat_id)
    if city:
        bot.send_message(chat_id, "Providing travel help...")
        SYSTEM_PROMPT = [{'role': 'system', 'text': f"Provide travel tips and attractions for {city}."}]
        status, answer, tokens_in_answer = ask_gpt(SYSTEM_PROMPT)
        if status:
            db.update_tokens(tokens_in_answer, chat_id)
            bot.send_message(chat_id, answer, reply_markup=travelhelp)
        else:
            bot.send_message(chat_id, "Failed to provide travel help.")
    else:
        bot.send_message(chat_id, "Please set your city first with /set_town.")

@bot.message_handler(commands=['support'])
def support(message):
    """Provide support contact information."""
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "For questions or help, contact the creator:\n"
        "Discord: lathanael\n"
        "Telegram: @Ts_Mark1"
    )

@bot.message_handler(commands=['weather'])
def weather(message):
    """Provide weather information for the user's city."""
    chat_id = message.chat.id
    city = db.get_city(chat_id)
    if city:
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode(city)
        if location:
            lat, lon = location.latitude, location.longitude
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                current_weather = data['current_weather']
                bot.send_message(
                    chat_id,
                    f"Weather in {city}:\n"
                    f"Temperature: {current_weather['temperature']}°C\n"
                    f"Wind Speed: {current_weather['windspeed']} km/h\n"
                    f"Weather Code: {current_weather['weathercode']}",
                    reply_markup=helpkey
                )
            else:
                bot.send_message(chat_id, "Failed to get weather data.")
        else:
            bot.send_message(chat_id, "City not found.")
    else:
        bot.send_message(chat_id, "Please set your city first with /set_town.")

questions = {
    "What is the capital of France?": ["Paris", "London", "Berlin"],
    "What is the capital of Japan?": ["Tokyo", "Seoul", "Beijing"],
    # Add more questions as needed
}

def generate_quiz():
    """Generate a random quiz question and answers."""
    question = random.choice(list(questions.keys()))
    answers = questions[question]
    return question, answers

def check_answer(question, text):
    """Check if the user's answer is correct."""
    correct_answer = questions[question][0]
    return text == correct_answer

@bot.message_handler(commands=['travel_quiz'])
def start_quiz(message):
    """Start the travel quiz."""
    global question  # Assuming global for simplicity; better to use states in production
    chat_id = message.chat.id
    bot.send_message(chat_id, "Let's play a quiz about world cities.")
    question, answers = generate_quiz()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(chat_id, f"Question: {question}")
    for answer in answers:
        keyboard.add(KeyboardButton(answer))
    bot.send_message(chat_id, 'Your answer:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_message_for_quiz)

def handle_message_for_quiz(message):
    """Handle the quiz answer."""
    chat_id = message.chat.id
    score = db.get_score(chat_id)
    text = message.text
    if text in questions[question]:
        correct = check_answer(question, text)
        if correct:
            bot.send_message(chat_id, "Correct! Play again?\n For a new question, press /travel_quiz", reply_markup=helpkey)
            db.update_score(score + 2, chat_id)
        else:
            bot.send_message(chat_id, f"Incorrect. The correct answer is: {questions[question][0]}. Play again?\n For a new question, press /travel_quiz", reply_markup=helpkey)
    else:
        bot.send_message(chat_id, "Please answer the question by choosing one of the options.")

bot.polling()
