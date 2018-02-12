import telebot
import fsm
import bot_utils
from flashcard import Word, Card
from bot_utils import get_id


def handle_erase_languages(bot, rtd):

	#=====================ERASE LANGUAGES=====================
	@bot.message_handler(func = lambda msg:
					rtd.get_user(get_id(msg)).get_state() == fsm.IDLE, 
					commands = ['erase_languages'])
	def erase_languages(msg):
		user = rtd.get_user(get_id(msg))
		user_id = user.get_id()
		user.set_state(fsm.LOCKED)

		known_languages = user.get_languages()

		if len(known_languages) == 0:
			bot.send_message(user_id, "Please, add a language first.")
			user.set_state(fsm.IDLE)
			return 	
		
		btn = bot_utils.create_inline_keys_sequential(known_languages)
		btn_set = set()
		markup = bot_utils.create_selection_inline_keyboard(btn_set, btn, 3, ("End selection", "DONE"))

		
		user.btn_set = btn_set
		user.keyboard_options = btn
		bot.send_message(user_id, "Select languages to erase:", reply_markup=markup, parse_mode="Markdown")
		user.set_state(fsm.next_state[fsm.IDLE]['erase_languages'])
		

	@bot.callback_query_handler(func=lambda call:
							rtd.get_user(get_id(call.message)).get_state() == (fsm.ERASE_LANGUAGES, fsm.SELECT_LANGUAGES))
	def callback_select_words(call):
		user = rtd.get_user(get_id(call.message))
		user_id = user.get_id()
		user.set_state(fsm.LOCKED)
	
		btn_set = user.btn_set
		btn_set, done = bot_utils.parse_selection_inline_keyboard_ans(call.data, btn_set)
		btn = user.keyboard_options
		
		if done == True:
			bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
			text = "_Erased languages:_\n"
			for i in btn_set:
				print(user.erase_language(btn[i][0]))
				text += "*." + btn[i][0] + "*\n"
			bot.send_message(user_id, text, parse_mode="Markdown")
			user.set_state(fsm.next_state[(fsm.ERASE_LANGUAGES, fsm.SELECT_LANGUAGES)]['done'])
		
		else:
			markup = bot_utils.create_selection_inline_keyboard(btn_set, btn, 3, ("End selection", "DONE"))
			bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="Select languages to erase:", reply_markup=markup)
			user.set_state(fsm.next_state[(fsm.ERASE_LANGUAGES, fsm.SELECT_LANGUAGES)]['continue'])