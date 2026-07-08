# 🇯🇵 Nana-chan: Japanese Conversation Practice Chatbot

Nana-chan is an AI-powered Japanese conversation practice chatbot built on Telegram to help Japanese learners improve their communication skills through interactive conversations.

The chatbot allows learners to practice writing Japanese naturally while receiving AI-powered corrections, explanations, furigana support, and translations to improve their understanding.

## ✨ Features

- 💬 Practice Japanese conversations through Telegram
- 🤖 AI-powered conversational responses
- ✅ Japanese grammar and sentence correction
- 📝 Provides explanations for mistakes and improvements
- 🔤 Supports furigana for kanji reading assistance
- 🌐 Provides English translations for easier understanding
- 🎯 Helps learners practice Japanese naturally based on their level

---

# 🛠️ Technologies Used

- **Python** - Main programming language
- **python-telegram-bot** - Telegram Bot API framework
- **OpenAI Agents SDK** - AI agent workflow and response generation
- **Pydantic** - Data validation and structured responses
- **python-dotenv** - Environment variable management

## Main Libraries

| Library | Purpose |
|---|---|
| `python-telegram-bot` | Handles Telegram bot commands, messages, callbacks, and user interactions |
| `openai` | Provides AI agent capabilities and model integration |
| `pydantic` | Defines structured response models and validates chatbot outputs |
| `python-dotenv` | Loads environment variables from `.env` files |

---

# 🚀 Getting Started

## Prerequisites

Before running Nana-chan, make sure you have:

- Python 3.10 or above installed
- A Telegram account
- A Telegram Bot Token
- OpenAI API access

---

# 🤖 Creating a Telegram Bot

Before using the chatbot, you need to create your own Telegram bot.

## Step 1: Create a Telegram Account

If you do not have a Telegram account:

1. Download Telegram:
   - Mobile: Install Telegram from your app store
   - Desktop: Install Telegram Desktop
2. Create an account using your phone number

---

## Step 2: Create a Bot Using BotFather

1. Open Telegram
2. Search for:

```
@BotFather
```

3. Start a conversation with BotFather
4. Follow the instructions to create a new bot

Official Telegram Bot tutorial:

https://core.telegram.org/bots/tutorial

After successfully creating your bot, BotFather will provide a unique bot token.

Example:

```
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

Keep this token private. Do not share it publicly or upload it to GitHub.

---

## Step 3: Configure Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

Replace the values with your own credentials.

Example:

```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
OPENAI_API_KEY=sk-your-api-key
```

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/eunicetehh/telegram_japanese_chatbot.git
```

Navigate into the project folder:

```bash
cd telegram_japanese_chatbot
```

---

## 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install python-telegram-bot python-dotenv openai pydantic
```

---

# ▶️ Running the Bot

Start the chatbot:

```bash
python telegram_bot.py
```

If everything is configured correctly, the Telegram bot will start running.

Open Telegram and search for your bot.

Start the conversation using:

```
/start
```

You can now begin practicing Japanese with Nana-chan.

---

# 💬 Example Conversation

### User

```
昨日映画を見ました。
```

### Nana-chan

```
Correct!

昨日映画を見ました。
(きのう えいがを みました)

Translation:
I watched a movie yesterday.

Explanation:
Your sentence is grammatically correct!
```

---

# 📂 Project Structure

```
telegram_japanese_chatbot/
│
├── telegram_bot.py                 # Telegram bot entry point
│
├── agent_workflow.py       # AI workflow and response processing
│
├── .env                    # API keys and environment variables
│
├── requirements.txt        # Python dependencies
│
└── README.md               # Project documentation
```

---

# 🔒 Security

To protect your credentials:

- Never commit your `.env` file
- Never share your Telegram Bot Token
- Never expose your OpenAI API key

Add `.env` into `.gitignore`:

```
.env
__pycache__/
*.pyc
```

---

# 🌱 Future Improvements

Potential improvements:

- Run on cloud premise
- Vocabulary tracking
- Conversation history
- Daily Japanese practice reminders
- User progress dashboard

---

# 📄 License

This project is created for educational purposes.
