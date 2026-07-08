import html
import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from agent_workflow import NanachanResponse, WorkflowInput, _has_corrections, run_workflow

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

HISTORIES_KEY = "conversation_histories"
LAST_REPLY_KEY = "last_replies"

DETAIL_FURIGANA = "detail:furigana"
DETAIL_ENGLISH = "detail:english"
DETAIL_CORRECTIONS = "detail:corrections"

DETAIL_LABELS = {
    DETAIL_FURIGANA: ("ふりがな", "furigana"),
    DETAIL_ENGLISH: ("English", "english"),
    DETAIL_CORRECTIONS: ("訂正", "corrections"),
}


def _histories(context: ContextTypes.DEFAULT_TYPE) -> dict[int, list]:
    if HISTORIES_KEY not in context.application.bot_data:
        context.application.bot_data[HISTORIES_KEY] = {}
    return context.application.bot_data[HISTORIES_KEY]


def _last_replies(context: ContextTypes.DEFAULT_TYPE) -> dict[int, NanachanResponse]:
    if LAST_REPLY_KEY not in context.application.bot_data:
        context.application.bot_data[LAST_REPLY_KEY] = {}
    return context.application.bot_data[LAST_REPLY_KEY]


def _reply_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ふりがな", callback_data=DETAIL_FURIGANA),
                InlineKeyboardButton("English", callback_data=DETAIL_ENGLISH),
            ],
            [InlineKeyboardButton("✏️ 訂正", callback_data=DETAIL_CORRECTIONS)],
        ]
    )


def _format_main_message(response: NanachanResponse) -> str:
    lines = [f"<b>🇯🇵</b> {html.escape(response.reply_ja)}"]

    if _has_corrections(response.correction_notes):
        lines.append(
            f"\n<b>✏️</b> {html.escape(response.corrected_user_ja)}"
        )

    return "\n".join(lines)


def _format_detail(response: NanachanResponse, detail_key: str) -> str:
    title, field = DETAIL_LABELS[detail_key]

    if field == "furigana":
        body = response.furigana
    elif field == "english":
        body = response.english
    else:
        if not _has_corrections(response.correction_notes):
            return "<b>✏️ 訂正</b>\n問題なし — looks good!"
        return (
            f"<b>✏️ {html.escape(title)}</b>\n"
            f"{html.escape(response.corrected_user_ja)}\n\n"
            f"<i>{html.escape(response.correction_notes)}</i>"
        )

    return f"<b>{html.escape(title)}</b>\n{html.escape(body)}"


async def _send_html(message, text: str, reply_markup=None) -> None:
    try:
        await message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
    except Exception:
        await message.reply_text(text, reply_markup=reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "こんにちは！ななちゃんです 🇯🇵\n\n"
        "日本語で話しかけてください。\n"
        "ふりがな・英語・訂正は下のボタンで見られます。\n"
        "/reset — 会話をリセット"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    _histories(context).pop(chat_id, None)
    _last_replies(context).pop(chat_id, None)
    await update.message.reply_text("会話をリセットしました。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    histories = _histories(context)
    prior = histories.get(chat_id)

    await update.message.chat.send_action("typing")

    try:
        response, new_history = await run_workflow(
            WorkflowInput(input_as_text=update.message.text),
            conversation_history=prior,
        )
    except Exception:
        logger.exception("Agent run failed for chat %s", chat_id)
        await update.message.reply_text(
            "すみません、エラーが起きました。もう一度送ってください。"
        )
        return

    histories[chat_id] = new_history
    _last_replies(context)[chat_id] = response

    await _send_html(
        update.message,
        _format_main_message(response),
        reply_markup=_reply_keyboard(),
    )


async def handle_detail_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()

    chat_id = update.effective_chat.id
    response = _last_replies(context).get(chat_id)
    if not response or query.data not in DETAIL_LABELS:
        await query.message.reply_text("もう一度メッセージを送ってください。")
        return

    text = _format_detail(response, query.data)
    await _send_html(query.message, text)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in .env or the environment.")

    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY in .env or the environment.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(
        CallbackQueryHandler(handle_detail_button, pattern=r"^detail:")
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Starting ななちゃん Telegram bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
