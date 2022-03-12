from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


class ChatBot():

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Enter /register to subscribe to temperature change notifications')

    def button(self, update: Update, context: CallbackContext) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        query.edit_message_text(text=f"Selected option: {query.data}")

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Displays info on how to use the bot."""
        self.start(update, context)

    def register_command(self, update: Update, context: CallbackContext) -> None:
        """Displays info on how to use the bot."""
        userid = update.effective_user.id
        if userid not in self.users:
            self.users.append(userid)
            update.message.reply_text("You subscribed to the temperature notifications. Use /deregister to unsubscribe.")
        else:
            update.message.reply_text(
                "You already subscribed to the temperature notifications. Use /deregister to unsubscribe.")

    def deregister_command(self, update: Update, context: CallbackContext) -> None:
        """Displays info on how to use the bot."""
        userid = update.effective_user.id
        if userid in self.users:
            self.users.remove(userid)
            update.message.reply_text("You unsubscribed the temperature notifications. Use /register to subscribe.")
        else:
            update.message.reply_text(
                "No subscription found")

    def send_temperature(self, temp):
        for user in self.users:
            self.updater.bot.send_message(user, f"Temperature changed to: {temp} °C")

    def __init__(self, token):
        self.updater = Updater(token)
        # Create the Updater and pass it your bot's token.
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('register', self.register_command))
        self.updater.dispatcher.add_handler(CommandHandler('deregister', self.deregister_command))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button))

        self.users = []

        # Start the Bot
        self.updater.start_polling()
