import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from config import BOT_TOKEN, CREATOR_USERNAME, CREATOR_NAME, BOT_VERSION
from database import Database
from keyboards import (
    get_main_menu_keyboard, 
    get_bet_keyboard, 
    get_admin_keyboard, 
    get_back_keyboard, 
    get_rules_keyboard,
    get_game_selection_keyboard
)
from games.fruit_slots import FruitSlots
from games.cosmic_jackpot import CosmicJackpotULTRA as CosmicJackpot
from games.retro_reels import RetroReelsULTRA as RetroReels
from games.egypt_slots import EgyptSlotsULTRA as EgyptSlots
from admin_panel import AdminPanel
from utils import format_user_stats, update_user_activity

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SlotBotULTRA:
    def __init__(self):
        self.db = Database()
        self.admin_panel = AdminPanel()
        self.user_states = {}
        self.admin_states = {}
        
        # ULTRA ИГРЫ
        self.games = {
            "fruit": FruitSlots(),
            "cosmic": CosmicJackpot(),
            "retro": RetroReels(),
            "egypt": EgyptSlots()
        }
        
        logger.info(f"🎰 ULTRA Slot Bot v{BOT_VERSION} initialized with {len(self.games)} ULTRA games")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        update_user_activity(self.db, user_id)
        
        welcome_text = (
            f"👋 *Добро пожаловать, {user.first_name}!*\n\n"
            f"🎰 *ULTRA SLOTS BOT v{BOT_VERSION}*\n\n"
            f"*🌟 ДОСТУПНЫЕ ULTRA-ИГРЫ:*\n"
            f"• 🎰 Fruit Slots ULTRA - 3x3 кинематографические слоты\n"
            f"• 🚀 Cosmic Jackpot ULTRA - 5x3 межгалактический джекпот\n"
            f"• 🕹️ Retro Reels ULTRA - 3x3 аркадные ретро-автоматы\n"
            f"• 🐫 Egypt Slots ULTRA - 4x4 фараонские сокровища\n\n"
            f"💫 *ОСОБЕННОСТИ:*\n"
            f"• Кинематографические анимации\n"
            f"• Эпические бонусные раунды\n"
            f"• Ультра-визуальные эффекты\n"
            f"• Система достижений\n\n"
            f"💡 *Создатель: {CREATOR_NAME} ({CREATOR_USERNAME})*\n\n"
            f"👇 *Выберите ULTRA-игру в меню ниже:*"
        )
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        user_state = self.user_states.get(user_id, {})
        
        update_user_activity(self.db, user_id)
        
        # Обработка админ-команд
        if self.admin_panel.is_admin(user_id):
            if await self.handle_admin_commands(update, context, text, user_id):
                return
        
        # Обработка обычных команд
        if await self.handle_user_commands(update, context, text, user_id, user_state):
            return
        
        # Обработка ставок
        if user_state.get('waiting_for_bet'):
            await self.handle_bet_input(update, context, text, user_id, user_state)
            return
        
        # Дефолтное сообщение
        await update.message.reply_text(
            "🎰 *ULTRA SLOTS BOT*\n\n👇 Пожалуйста, используйте меню для навигации:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def handle_admin_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, user_id: int) -> bool:
        """Обработка админ-команд"""
        admin_state = self.admin_states.get(user_id, {})
        
        if text == "👑 Админ панель":
            await self.show_admin_panel(update)
            return True
        elif text == "📊 Статистика бота":
            await self.show_bot_stats(update)
            return True
        elif text == "👥 Список пользователей":
            await self.show_users_list(update)
            return True
        elif text == "💰 Изменить баланс":
            self.admin_states[user_id] = {'waiting_for_user_id': True}
            await update.message.reply_text(
                "👤 *Введите ID пользователя:*",
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
            return True
        elif text == "📢 Рассылка":
            self.admin_states[user_id] = {'waiting_for_broadcast': True}
            await update.message.reply_text(
                "📝 *Введите сообщение для рассылки:*",
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
            return True
        elif admin_state.get('waiting_for_user_id'):
            try:
                target_user_id = int(text)
                self.admin_states[user_id] = {
                    'waiting_for_amount': True,
                    'target_user_id': target_user_id
                }
                await update.message.reply_text(
                    f"👤 *Пользователь:* {target_user_id}\n💵 *Введите сумму для изменения баланса:*",
                    reply_markup=get_back_keyboard(),
                    parse_mode='Markdown'
                )
                return True
            except ValueError:
                await update.message.reply_text(
                    "❌ *Неверный ID пользователя!*",
                    reply_markup=get_admin_keyboard(),
                    parse_mode='Markdown'
                )
                self.admin_states[user_id] = {}
                return True
        elif admin_state.get('waiting_for_amount'):
            try:
                amount = int(text)
                target_user_id = admin_state['target_user_id']
                
                if self.admin_panel.update_user_balance(target_user_id, amount):
                    await update.message.reply_text(
                        f"✅ *Баланс пользователя {target_user_id} изменен на {amount} монет*",
                        reply_markup=get_admin_keyboard(),
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        "❌ *Ошибка при изменении баланса!*",
                        reply_markup=get_admin_keyboard(),
                        parse_mode='Markdown'
                    )
                self.admin_states[user_id] = {}
                return True
            except ValueError:
                await update.message.reply_text(
                    "❌ *Неверная сумма!*",
                    reply_markup=get_back_keyboard(),
                    parse_mode='Markdown'
                )
                return True
        elif admin_state.get('waiting_for_broadcast'):
            await self.send_broadcast(update, context, text)
            self.admin_states[user_id] = {}
            return True
        
        return False
    
    async def handle_user_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, user_id: int, user_state: dict) -> bool:
        """Обработка пользовательских команд"""
        if text == "🎰 Fruit Slots":
            await self.show_game_rules(update, "fruit")
            return True
        elif text == "🚀 Cosmic Jackpot":
            await self.show_game_rules(update, "cosmic")
            return True
        elif text == "🕹️ Retro Reels":
            await self.show_game_rules(update, "retro")
            return True
        elif text == "🐫 Egypt Slots":
            await self.show_game_rules(update, "egypt")
            return True
        elif text == "💰 Мой баланс":
            await self.show_balance(update)
            return True
        elif text == "📊 Статистика":
            await self.show_stats(update)
            return True
        elif text == "🎮 Начать игру":
            game_type = user_state.get('selected_game')
            if game_type:
                await self.select_game(update, context, game_type)
            else:
                await self.show_main_menu(update)
            return True
        elif text in ["🔙 Назад в меню", "🔙 Главное меню"]:
            await self.show_main_menu(update)
            return True
        elif text == "🎯 Выбрать другую игру":
            await self.show_game_selection(update)
            return True
        
        return False
    
    async def handle_bet_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, user_id: int, user_state: dict):
        """Обработка ввода ставки"""
        try:
            if "🪙" in text:
                bet_amount = int(text.split()[0])
            else:
                bet_amount = int(text)
            
            game_type = user_state.get('selected_game')
            await self.play_game(update, context, game_type, bet_amount)
            
        except ValueError:
            await update.message.reply_text(
                "❌ *Пожалуйста, выберите ставку из меню ниже!*",
                reply_markup=get_bet_keyboard(),
                parse_mode='Markdown'
            )
    
    async def show_game_selection(self, update: Update):
        """Показать выбор игры"""
        selection_text = (
            "🎰 *ULTRA SLOTS BOT*\n\n"
            "🌟 *Выберите ULTRA-игру:*\n\n"
            "• 🎰 Fruit Slots ULTRA - Фруктовое безумие\n"
            "• 🚀 Cosmic Jackpot ULTRA - Космические приключения\n"
            "• 🕹️ Retro Reels ULTRA - Аркадная классика\n"
            "• 🐫 Egypt Slots ULTRA - Древние сокровища"
        )
        
        await update.message.reply_text(
            selection_text,
            reply_markup=get_game_selection_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_game_rules(self, update: Update, game_type: str):
        """Показать правила игры перед началом"""
        user_id = update.effective_user.id
        
        # Сохраняем выбранную игру
        self.user_states[user_id] = {
            'selected_game': game_type
        }
        
        rules_text = self.get_game_rules(game_type)
        game_info = self.get_game_info(game_type)
        
        full_message = f"{game_info}\n\n{rules_text}"
        
        await update.message.reply_text(
            full_message,
            reply_markup=get_rules_keyboard(),
            parse_mode='Markdown'
        )
    
    def get_game_info(self, game_type: str) -> str:
        """Получить информацию об игре"""
        info = {
            "fruit": (
                "🎰 *Fruit Slots ULTRA*\n\n"
                "💫 *Кинематографические фруктовые слоты!*\n"
                "📊 Сетка: 3x3 | 🎯 Линии: 8 | ⭐ Ультра-анимации"
            ),
            "cosmic": (
                "🚀 *Cosmic Jackpot ULTRA*\n\n"
                "🌌 *Межгалактическое приключение!*\n"
                "📊 Сетка: 5x3 | 🪐 Орбиты: 15 | 👽 Инопланетные бонусы"
            ),
            "retro": (
                "🕹️ *Retro Reels ULTRA*\n\n"
                "🎮 *Аркадная классика 80-х!*\n"
                "📊 Сетка: 3x3 | 👾 Комбо: 12 | 💾 Пиксельные эффекты"
            ),
            "egypt": (
                "🐫 *Egypt Slots ULTRA*\n\n"
                "🔱 *Путь к сокровищам фараонов!*\n"
                "📊 Сетка: 4x4 | 📜 Линии: 20 | 👑 Фараонские ритуалы"
            )
        }
        return info.get(game_type, "")
    
    def get_game_rules(self, game_type: str) -> str:
        """Получить правила игры"""
        rules = {
            "fruit": (
                "📖 *ПРАВИЛА ИГРЫ:*\n\n"
                "🎯 *Выигрышные комбинации:*\n"
                "• 3 одинаковых символа в строке 🏆\n"
                "• 3 одинаковых символа в столбце 📈\n"
                "• Диагональные комбинации ↗️↙️\n\n"
                "💎 *Особые символы:*\n"
                "• 💎 Алмаз: x15 множитель\n"
                "• 🔔 Колокольчик: x8 множитель\n"
                "• 🍀 Клевер: Удача + x5\n"
                "• 🌈 Радуга: x20 множитель\n\n"
                "💰 *ULTRA-Бонусы:*\n"
                "• Фруктовый дождь: +x5\n"
                "• Джекпот (все одинаковые): x100!\n"
                "• Эпическая победа: x200! 🌟\n\n"
                "🎬 *Кинематографические анимации!*"
            ),
            "cosmic": (
                "📖 *ПРАВИЛА ИГРЫ:*\n\n"
                "🎯 *Выигрышные комбинации:*\n"
                "• 3-5 одинаковых символа в строке 🌟\n"
                "• Специальные космические паттерны 🪐\n\n"
                "👽 *Особые символы:*\n"
                "• 👽 Инопланетянин: x12 множитель\n"
                "• 🪐 Планета: x10 множитель\n"
                "• 🚀 Ракета: x8 множитель\n"
                "• 🌌 Туманность: x15 множитель\n\n"
                "💰 *ULTRA-Бонусы:*\n"
                "• Инопланетное вторжение: +x12\n"
                "• Космический джекпот: x75! 🚀\n"
                "• Галактический взрыв: x150! 💫\n\n"
                "🌌 *Межгалактические анимации!*"
            ),
            "retro": (
                "📖 *ПРАВИЛА ИГРЫ:*\n\n"
                "🎯 *Выигрышные комбинации:*\n"
                "• Классические линии 🎮\n"
                "• Пиксельные паттерны 👾\n"
                "• Аркадные комбинации 🕹️\n\n"
                "💾 *Особые символы:*\n"
                "• 👾 Пришелец: x10 множитель\n"
                "• 🕹️ Джойстик: x8 множитель\n"
                "• 🎮 Приставка: x6 множитель\n"
                "• 💎 Кристалл: x12 множитель\n\n"
                "💰 *ULTRA-Бонусы:*\n"
                "• Бонусный раунд: x20! 🎰\n"
                "• Легенда аркады: x35! 🏆\n"
                "• Пиксельный шторм: x50! 🔥\n\n"
                "🎮 *Аркадные анимации 80-х!*"
            ),
            "egypt": (
                "📖 *ПРАВИЛА ИГРЫ:*\n\n"
                "🎯 *Выигрышные комбинации:*\n"
                "• 4 символа в строке/столбце 🔺\n"
                "• Квадраты 2x2 ⬛\n"
                "• Пирамидальные паттерны 🔱\n\n"
                "👑 *Особые символы:*\n"
                "• 👑 Корона: x15 множитель\n"
                "• 💎 Алмаз: x12 множитель\n"
                "• ⚱️ Саркофаг: x10 множитель\n"
                "• 🔱 Трезубец: x8 множитель\n\n"
                "💰 *ULTRA-Бонусы:*\n"
                "• Бонус фараона: x25! ⚱️\n"
                "• Королевское сокровище: x50! 💎\n"
                "• Пирамида света: x100! 👑\n\n"
                "🐫 *Фараонские анимации!*"
            )
        }
        
        return rules.get(game_type, "Правила для этой игры пока не доступны.")
    
    async def select_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE, game_type: str):
        """Выбор игры и переход к ставкам"""
        user_id = update.effective_user.id
        user_data = self.db.get_user(user_id)
        game = self.games[game_type]
        
        self.user_states[user_id] = {
            'waiting_for_bet': True,
            'selected_game': game_type
        }
        
        game_info = self.get_game_selection_text(game_type)
        
        bet_text = (
            f"{game_info}\n\n"
            f"💰 *Ваш баланс:* {user_data['balance']} 🪙\n"
            f"💎 *Доступно для игры:* {user_data['balance']} монет\n\n"
            f"💵 *Выберите ULTRA-ставку:*"
        )
        
        await update.message.reply_text(
            bet_text,
            reply_markup=get_bet_keyboard(),
            parse_mode='Markdown'
        )
    
    def get_game_selection_text(self, game_type: str) -> str:
        """Получить текст выбора игры"""
        texts = {
            "fruit": "🎰 *Fruit Slots ULTRA*\n\n🍒 *Готовы к фруктовому безумию?*",
            "cosmic": "🚀 *Cosmic Jackpot ULTRA*\n\n🌌 *Готовы к межгалактическому приключению?*", 
            "retro": "🕹️ *Retro Reels ULTRA*\n\n🎮 *Готовы к аркадной классике?*",
            "egypt": "🐫 *Egypt Slots ULTRA*\n\n🔱 *Готовы к поиску сокровищ фараонов?*"
        }
        return texts.get(game_type, "")
    
    async def play_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE, game_type: str, bet_amount: int):
        """Запуск ULTRA-игры с кинематографическими анимациями"""
        user_id = update.effective_user.id
        user_data = self.db.get_user(user_id)
        game = self.games[game_type]
        
        # Проверка баланса
        if user_data["balance"] < bet_amount:
            await update.message.reply_text(
                "❌ *Недостаточно средств на балансе!*\n\n"
                "💡 Пополните баланс или выберите меньшую ставку.",
                reply_markup=get_main_menu_keyboard(),
                parse_mode='Markdown'
            )
            return
        
        # ULTRA-сообщение о запуске
        start_message = await update.message.reply_text(
            f"🎬 *Запуск {game.name}...*\n\n"
            f"💰 *ULTRA-ставка:* {bet_amount} 🪙\n"
            f"📊 *Баланс:* {user_data['balance']} монет\n"
            f"🎯 *Режим:* Кинематографический\n\n"
            f"🌟 *Подготовка ULTRA-анимаций...*",
            parse_mode='Markdown'
        )
        
        try:
            # Запуск ULTRA-игры с кинематографическими анимациями
            result_text, win_amount, sticker_id = await game.spin_with_animation(
                bet_amount, update, context, start_message.message_id
            )
            
            # Отправка ULTRA-стикера
            if sticker_id:
                try:
                    await context.bot.send_sticker(
                        chat_id=update.effective_chat.id,
                        sticker=sticker_id
                    )
                except Exception as e:
                    logger.warning(f"Не удалось отправить ULTRA-стикер: {e}")
            
            # Обновление статистики пользователя
            user_data["balance"] += win_amount
            user_data["games_played"] = user_data.get("games_played", 0) + 1
            user_data["total_bets"] = user_data.get("total_bets", 0) + bet_amount
            
            if win_amount > 0:
                user_data["total_wins"] = user_data.get("total_wins", 0) + 1
                # ULTRA-достижение за крупный выигрыш
                if win_amount >= bet_amount * 10:
                    user_data["big_wins"] = user_data.get("big_wins", 0) + 1
            
            self.db.update_user(user_id, user_data)
            
            # ULTRA-информация о балансе
            if win_amount > 0:
                balance_change = f"📈 *ULTRA-выигрыш:* +{win_amount} 🪙"
                if win_amount >= bet_amount * 20:
                    balance_change = f"🎊 *ЭПИЧЕСКИЙ ВЫИГРЫШ:* +{win_amount} 🪙"
                elif win_amount >= bet_amount * 10:
                    balance_change = f"🌟 *БОЛЬШОЙ ВЫИГРЫШ:* +{win_amount} 🪙"
            else:
                balance_change = f"📉 *Ставка:* {bet_amount} 🪙"
            
            balance_info = f"💰 *Текущий баланс:* {user_data['balance']} монет"
            
            final_message = f"{result_text}\n{balance_change}\n{balance_info}"
            
            # Обновление сообщения с ULTRA-результатом
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=start_message.message_id,
                text=final_message,
                parse_mode='Markdown'
            )
            
            # ULTRA-автоматический возврат в меню
            await asyncio.sleep(6)  # Увеличенное время для наслаждения анимациями
            await self.show_ultra_return_menu(update, user_data['balance'], win_amount > 0, win_amount)
            
        except Exception as e:
            logger.error(f"ULTRA-ошибка в игре {game_type}: {e}")
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=start_message.message_id,
                text="❌ *Произошла ULTRA-ошибка во время игры. Попробуйте еще раз!*",
                reply_markup=get_main_menu_keyboard(),
                parse_mode='Markdown'
            )
        finally:
            # Всегда сбрасываем состояние пользователя
            if user_id in self.user_states:
                self.user_states[user_id] = {}
    
    async def show_ultra_return_menu(self, update: Update, balance: int, is_win: bool, win_amount: int):
        """Показать ULTRA-меню возврата"""
        if is_win:
            if win_amount >= 1000:
                message = (
                    f"🎊 *ЭПИЧЕСКАЯ ПОБЕДА!* 🌟\n\n"
                    f"💰 *Ваш баланс:* {balance} 🪙\n\n"
                    f"🏆 *Продолжайте в том же духе!*\n"
                    f"💫 *Удача на вашей стороне!*"
                )
            elif win_amount >= 500:
                message = (
                    f"🌟 *ОТЛИЧНАЯ ИГРА!* 🎉\n\n"
                    f"💰 *Ваш баланс:* {balance} 🪙\n\n"
                    f"🎯 *Почти у цели!*\n"
                    f"🚀 *Следующий джекпот близко!*"
                )
            else:
                message = (
                    f"🎉 *ХОРОШАЯ ИГРА!* 👍\n\n"
                    f"💰 *Ваш баланс:* {balance} 🪙\n\n"
                    f"💫 *Продолжайте играть!*\n"
                    f"⭐ *Удача ждет вас!*"
                )
        else:
            message = (
                f"🎰 *СЛЕДУЮЩИЙ РАЗ ПОВЕЗЕТ!* 💫\n\n"
                f"💰 *Ваш баланс:* {balance} 🪙\n\n"
                f"🌟 *Удача переменчива!*\n"
                f"🎯 *Попробуйте другую ULTRA-игру!*"
            )
        
        await update.message.reply_text(
            message,
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_balance(self, update: Update):
        """Показать ULTRA-баланс"""
        user_data = self.db.get_user(update.effective_user.id)
        
        # ULTRA-статистика баланса
        total_wagered = user_data.get('total_bets', 0)
        total_wins = user_data.get('total_wins', 0)
        big_wins = user_data.get('big_wins', 0)
        
        balance_text = (
            f"💰 *ULTRA-БАЛАНС*\n\n"
            f"💎 *Текущий баланс:* {user_data['balance']} 🪙\n"
            f"🎯 *Доступно для игры:* {user_data['balance']} монет\n\n"
            f"📊 *Статистика:*\n"
            f"• 🎰 Сыграно игр: {user_data.get('games_played', 0)}\n"
            f"• 📈 Всего ставок: {total_wagered} 🪙\n"
            f"• 🏆 Выигрышей: {total_wins}\n"
            f"• 🌟 Крупных побед: {big_wins}\n\n"
            f"🎮 *Выберите ULTRA-игру для продолжения:*"
        )
        
        await update.message.reply_text(
            balance_text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_stats(self, update: Update):
        """Показать ULTRA-статистику"""
        user_data = self.db.get_user(update.effective_user.id)
        stats_text = format_user_stats(user_data)
        
        ultra_stats = (
            f"📊 *ULTRA-СТАТИСТИКА*\n\n"
            f"{stats_text}\n\n"
            f"🌟 *ULTRA-достижения:*\n"
            f"• 🎯 Первая игра: {'✅' if user_data.get('games_played', 0) > 0 else '⏳'}\n"
            f"• 🏆 Первая победа: {'✅' if user_data.get('total_wins', 0) > 0 else '⏳'}\n"
            f"• 💎 Крупный выигрыш: {'✅' if user_data.get('big_wins', 0) > 0 else '⏳'}\n"
            f"• 🚀 Активный игрок: {'✅' if user_data.get('games_played', 0) > 10 else '⏳'}\n\n"
            f"🎰 *Продолжайте играть для новых достижений!*"
        )
        
        await update.message.reply_text(
            ultra_stats,
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_admin_panel(self, update: Update):
        """Показать ULTRA-админ панель"""
        user_id = update.effective_user.id
        
        if not self.admin_panel.is_admin(user_id):
            await update.message.reply_text(
                "❌ *У вас нет доступа к ULTRA-админ панели!*",
                reply_markup=get_main_menu_keyboard(),
                parse_mode='Markdown'
            )
            return
        
        admin_text = (
            f"👑 *ULTRA-АДМИН ПАНЕЛЬ v{BOT_VERSION}*\n\n"
            f"💫 *Добро пожаловать в центр управления!*\n\n"
            f"🎯 *Доступные действия:*"
        )
        
        await update.message.reply_text(
            admin_text,
            reply_markup=get_admin_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_bot_stats(self, update: Update):
        """Показать ULTRA-статистику бота"""
        user_id = update.effective_user.id
        
        if not self.admin_panel.is_admin(user_id):
            await update.message.reply_text("❌ *Доступ запрещен!*", parse_mode='Markdown')
            return
        
        stats_text = self.admin_panel.get_bot_stats()
        await update.message.reply_text(
            stats_text,
            reply_markup=get_admin_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_users_list(self, update: Update):
        """Показать ULTRA-список пользователей"""
        user_id = update.effective_user.id
        
        if not self.admin_panel.is_admin(user_id):
            await update.message.reply_text("❌ *Доступ запрещен!*", parse_mode='Markdown')
            return
        
        users_text = self.admin_panel.get_users_list()
        await update.message.reply_text(
            users_text,
            reply_markup=get_admin_keyboard(),
            parse_mode='Markdown'
        )
    
    async def send_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """ULTRA-рассылка сообщений"""
        user_id = update.effective_user.id
        
        if not self.admin_panel.is_admin(user_id):
            await update.message.reply_text("❌ *Доступ запрещен!*", parse_mode='Markdown')
            return
        
        users_data = self.db.get_all_users()
        success_count = 0
        fail_count = 0
        
        progress_msg = await update.message.reply_text(
            "📢 *Запуск ULTRA-рассылки...*", 
            parse_mode='Markdown'
        )
        
        for user_id_str in users_data:
            try:
                await context.bot.send_message(
                    chat_id=int(user_id_str),
                    text=(
                        f"📢 *ULTRA-ОБЪЯВЛЕНИЕ ОТ АДМИНИСТРАЦИИ:*\n\n"
                        f"{message}\n\n"
                        f"💫 *С наилучшими пожеланиями,*\n"
                        f"*Команда ULTRA Slots Bot* 🎰"
                    ),
                    parse_mode='Markdown'
                )
                success_count += 1
                
                # ULTRA-прогресс каждые 5 сообщений
                if success_count % 5 == 0:
                    await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=progress_msg.message_id,
                        text=f"📢 *ULTRA-рассылка...* Отправлено: {success_count}/{len(users_data)}",
                        parse_mode='Markdown'
                    )
                
                # ULTRA-задержка
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"ULTRA-ошибка отправки пользователю {user_id_str}: {e}")
                fail_count += 1
        
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=progress_msg.message_id,
            text=(
                f"✅ *ULTRA-рассылка завершена!*\n\n"
                f"📊 *Результаты:*\n"
                f"• ✅ Успешно: {success_count}\n"
                f"• ❌ Не удалось: {fail_count}\n"
                f"• 📈 Охват: {success_count/len(users_data)*100:.1f}%"
            ),
            parse_mode='Markdown',
            reply_markup=get_admin_keyboard()
        )
    
    async def show_main_menu(self, update: Update):
        """Показать ULTRA-главное меню"""
        # Сбрасываем состояние пользователя
        user_id = update.effective_user.id
        if user_id in self.user_states:
            self.user_states[user_id] = {}
        if user_id in self.admin_states:
            self.admin_states[user_id] = {}
        
        await update.message.reply_text(
            "🎰 *ULTRA SLOTS BOT - ГЛАВНОЕ МЕНЮ*\n\n"
            "🌟 *Выберите ULTRA-игру для начала:*",
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )

def main():
    """Запуск ULTRA-бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        bot = SlotBotULTRA()
        
        # ULTRA-обработчики
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
        
        logger.info(f"🎰 ULTRA SLOTS BOT v{BOT_VERSION} запущен успешно!")
        print(f"🎰 ULTRA SLOTS BOT v{BOT_VERSION}")
        print("🚀 Бот запущен с кинематографическими анимациями!")
        print("💫 Нажмите Ctrl+C для остановки")
        print("=" * 50)
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"ULTRA-ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска ULTRA-бота: {e}")

if __name__ == "__main__":
    main()