import telebot
import fsm
import message_handlers.add_word
from utilities import utils
from utilities import bot_utils
from flashcard import Word, Card
from utilities.bot_utils import get_id


def handle_add_word_translation(bot, rtd):

	@bot.message_handler(func = lambda msg:
					rtd.get_user(get_id(msg)).get_state() == (fsm.ADD_WORD, fsm.SEND_TRANSLATION),
					content_types=['text'])
	def add_word8(msg):
		"""
			ADD_WORD, RELATE_MENU, 'send_translation'
		"""
		user = rtd.get_user(get_id(msg))
		user_id = user.get_id()
		user.set_state(fsm.LOCKED)

		
		translation = msg.text.strip()
		print(translation)

		word = user.temp_word
		card_id = user.get_highest_card_id() + 1 + len(word.cards)
		card = Card(word.user_id, word.word_id, word.language, word.topic, word.foreign_word,
					card_id, 'translation')

		card.add_archive(translation)
		word.set_card(card)
		print(str(user.temp_word))
		bot.send_message(user_id, "Text received successfuly")

		if user.receive_queue.empty():
			message_handlers.add_word.save_word(bot, user)
			
			language = user.temp_word.get_language() 
			topic = user.temp_word.get_topic()
			
			options = ['Yes', 'No']
			markup = bot_utils.create_keyboard(topics, 2)
			text = "_Would you like to add more words in_ *{}*_, in topic_ *{}*_?_\n".format(
						treat_msg_to_send(language, "*"), treat_msg_to_send(topic, "*")) + bot_utils.create_string_keyboard(options)
			bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")		
			
			user.set_state(fsm.next_state[(fsm.ADD_WORD, fsm.SEND_TRANSLATION)]['done'])
		else:
			content_type = user.receive_queue.get()
			message_handlers.add_word.prepare_to_receive(bot, user, content_type)
			user.set_state(fsm.next_state[(fsm.ADD_WORD, fsm.SEND_TRANSLATION)][content_type])
