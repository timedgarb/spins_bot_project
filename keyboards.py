from telegram import ReplyKeyboardMarkup, KeyboardButton

# ULTRA-Главное меню
def get_main_menu_keyboard():
    keyboard = [
        ["🎰 Fruit Slots", "🚀 Cosmic Jackpot"],
        ["🕹️ Retro Reels", "🐫 Egypt Slots"],
        ["💰 Мой баланс", "📊 Статистика"],
        ["👑 Админ панель"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="🎰 Выберите ULTRA-игру...")

# ULTRA-Клавиатура ставок
def get_bet_keyboard():
    keyboard = [
        ["10 🪙", "50 🪙", "100 🪙"],
        ["200 🪙", "500 🪙", "1000 🪙"],
        ["🎯 Выбрать другую игру", "🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ULTRA-Клавиатура правил игры
def get_rules_keyboard():
    keyboard = [
        ["🎮 Начать игру"],
        ["🎯 Выбрать другую игру"],
        ["🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ULTRA-Выбор игры
def get_game_selection_keyboard():
    keyboard = [
        ["🎰 Fruit Slots", "🚀 Cosmic Jackpot"],
        ["🕹️ Retro Reels", "🐫 Egypt Slots"],
        ["🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ULTRA-Админ клавиатура
def get_admin_keyboard():
    keyboard = [
        ["📊 Статистика бота", "👥 Список пользователей"],
        ["💰 Изменить баланс", "📢 Рассылка"],
        ["🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ULTRA-Клавиатура назад
def get_back_keyboard():
    keyboard = [
        ["🔙 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)