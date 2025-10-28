import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from config import STICKER_IDS, SPIN_DELAY, ULTRA_ANIMATION_FRAMES, ULTRA_MULTIPLIERS, ULTRA_SYMBOLS

class FruitSlots:
    def __init__(self):
        self.symbols = ULTRA_SYMBOLS["fruit"]["common"] + ULTRA_SYMBOLS["fruit"]["rare"] + ULTRA_SYMBOLS["fruit"]["epic"] + ULTRA_SYMBOLS["fruit"]["legendary"]
        self.name = "Fruit Slots ULTRA"
        self.rows = 3
        self.cols = 3
    
    async def spin_with_animation(self, bet: int, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int):
        chat_id = update.effective_chat.id
        final_reels = self.generate_ultra_reels()
        win_amount, multiplier, lines, jackpot, epic_win = self.calculate_ultra_win(final_reels, bet)
        
        # УЛЬТРА-СИКВЕНС АНИМАЦИИ
        await self.ultra_cinematic_sequence(update, context, message_id, bet, final_reels, chat_id)
        
        # МЕГА-ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
        result_data = await self.create_epic_result(final_reels, win_amount, multiplier, lines, jackpot, epic_win, bet)
        
        return result_data
    
    def generate_ultra_reels(self):
        """Генерация ультра-реелсов с весами"""
        reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Весовая система для символов
                weights = [50, 30, 15, 5]  # common, rare, epic, legendary
                symbol_pool = []
                for idx, weight in enumerate(weights):
                    symbol_pool.extend([ULTRA_SYMBOLS["fruit"][list(ULTRA_SYMBOLS["fruit"].keys())[idx]][0]] * weight)
                
                row.append(random.choice(symbol_pool))
            reels.append(row)
        return reels
    
    async def ultra_cinematic_sequence(self, update, context, message_id, bet, final_reels, chat_id):
        """УЛЬТРА-КИНЕМАТОГРАФИЧЕСКАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ"""
        phases = ULTRA_ANIMATION_FRAMES["fruit"]["phases"]
        
        for phase_idx, phase in enumerate(phases):
            phase_text = phase["text"]
            frames = phase["frames"]
            effects = phase["effects"]
            
            for frame_idx, frame in enumerate(frames):
                # Создание ультра-анимированных барабанов
                progress = (phase_idx * len(frames) + frame_idx) / (len(phases) * len(frames))
                temp_reels = self.create_cinematic_reels(final_reels, progress, effects)
                
                # Ультра-форматирование доски
                board = self.format_cinematic_board(temp_reels, effects, frame_idx)
                
                # Создание эпического сообщения
                message = self.create_epic_message(phase_text, frame, board, bet, effects, progress)
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Динамическая задержка для кинематографического эффекта
                dynamic_delay = self.calculate_cinematic_delay(phase_idx, frame_idx, progress)
                await asyncio.sleep(dynamic_delay)
        
        # ФИНАЛЬНЫЙ ШОУКЕЙС
        await self.final_showcase(update, context, message_id, final_reels, bet, chat_id)
    
    def create_cinematic_reels(self, final_reels, progress, effects):
        """Создание кинематографических барабанов"""
        temp_reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Прогрессивное раскрытие финальных символов
                reveal_chance = min(1.0, progress * 1.5 + random.random() * 0.3)
                
                if random.random() < reveal_chance:
                    row.append(final_reels[i][j])
                else:
                    # Специальные эффекты для разных фаз
                    if "rainbow" in effects:
                        row.append(random.choice(["🌈", "🎯", "✨"]))
                    elif "turbo" in effects:
                        row.append(random.choice(["⚡", "💫", "🌟"]))
                    else:
                        row.append(random.choice(self.symbols))
            temp_reels.append(row)
        return temp_reels
    
    def format_cinematic_board(self, reels, effects, frame_idx):
        """Кинематографическое форматирование доски"""
        board = "┌─────────┐\n"
        
        for i, row in enumerate(reels):
            formatted_row = []
            for j, symbol in enumerate(row):
                # Применение эффектов
                if "glow" in effects and frame_idx % 2 == 0:
                    formatted_symbol = f"✨{symbol}"
                elif "vibrate" in effects:
                    formatted_symbol = f"🌀{symbol}"
                elif "rainbow" in effects:
                    formatted_symbol = f"🌈{symbol}"
                else:
                    formatted_symbol = symbol
                formatted_row.append(formatted_symbol)
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────┘"
        return f"```\n{board}```"
    
    def create_epic_message(self, phase_text, frame, board, bet, effects, progress):
        """Создание эпического сообщения"""
        progress_bar = self.create_progress_bar(progress)
        effect_emojis = " ".join(["✨"] * int(progress * 5))
        
        return (
            f"{phase_text}"
            f"{frame} {frame} {frame}\n\n"
            f"{board}\n"
            f"{progress_bar}\n"
            f"💰 Ставка: {bet} 🪙 {effect_emojis}\n"
            f"🎬 *Кинематографический режим: {int(progress * 100)}%*"
        )
    
    def create_progress_bar(self, progress, length=20):
        """Создание прогресс-бара"""
        filled = int(progress * length)
        empty = length - filled
        return f"▰{'▰' * filled}{'▱' * empty}▰"
    
    def calculate_cinematic_delay(self, phase_idx, frame_idx, progress):
        """Расчет кинематографической задержки"""
        base_delay = SPIN_DELAY
        
        # Ускорение в середине, замедление в конце
        if progress < 0.3:
            return base_delay * 0.8  # Быстрее в начале
        elif progress > 0.7:
            return base_delay * 1.5  # Медленнее в конце
        else:
            return base_delay
    
    async def final_showcase(self, update, context, message_id, final_reels, bet, chat_id):
        """ФИНАЛЬНЫЙ ШОУКЕЙС С ЭФФЕКТАМИ"""
        showcase_effects = ["💥", "🎊", "🎉", "🏆", "💰", "👑"]
        
        for i in range(6):
            # Чередование эффектов
            effect = showcase_effects[i % len(showcase_effects)]
            
            if i % 2 == 0:
                # Эффектная версия
                board = self.format_showcase_board(final_reels, effect, True)
            else:
                # Стандартная версия
                board = self.format_showcase_board(final_reels, effect, False)
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"🎰 *Fruit Slots ULTRA*\n\n{effect} *ФИНАЛЬНЫЙ РЕЗУЛЬТАТ!* {effect}\n\n{board}\n💰 Ставка: {bet} 🪙",
                parse_mode='Markdown'
            )
            await asyncio.sleep(0.4)
    
    def format_showcase_board(self, reels, effect, enhanced=False):
        """Форматирование доски для шоукейса"""
        board = "┌─────────┐\n"
        
        for row in reels:
            if enhanced:
                formatted_row = [f"{effect}{symbol}" for symbol in row]
            else:
                formatted_row = row
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────┘"
        return f"```\n{board}```"
    
    async def create_epic_result(self, final_reels, win_amount, multiplier, lines, jackpot, epic_win, bet):
        """Создание эпического результата"""
        board = self.format_ultra_board(final_reels, lines if win_amount > 0 else [])
        
        if epic_win:
            result_emoji = "👑"
            result_text = f"*ЭПИЧЕСКАЯ ПОБЕДА!* 🌟"
            win_info = f"💰 *НЕВЕРОЯТНЫЙ ВЫИГРЫШ: {win_amount} МОНЕТ!* 🎊"
            sticker_id = STICKER_IDS["epic_win"]
        elif jackpot:
            result_emoji = "🎊"
            result_text = f"*ДЖЕКПОТ!* 🎰"
            win_info = f"💰 *ГРАНД-ВЫИГРЫШ: {win_amount} МОНЕТ!* 🎉"
            sticker_id = STICKER_IDS["jackpot"]
        elif win_amount > 0:
            result_emoji = "🎉"
            result_text = f"*ПОБЕДА!* 🏆"
            win_info = f"💰 *Выигрыш: {win_amount} монет!* (x{multiplier})"
            sticker_id = STICKER_IDS["win"]
        else:
            result_emoji = "🎰"
            result_text = f"*Попробуйте еще раз!* 💫"
            win_info = f"💸 *Ставка: {bet} монет*"
            sticker_id = STICKER_IDS["lose"]
        
        result_message = (
            f"🎰 *Fruit Slots ULTRA - РЕЗУЛЬТАТ!* {result_emoji}\n\n"
            f"{board}\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"{result_text}\n"
            f"{win_info}\n"
        )
        
        if lines and win_amount > 0:
            result_message += f"📈 *Активированные линии:* {', '.join(lines)}\n"
        
        if epic_win:
            result_message += f"\n🌟 *ЭПИЧЕСКАЯ УДАЧА!* 🌟\n"
            result_message += f"🎯 *Вы достигли максимального уровня везения!* 👑\n"
        elif jackpot:
            result_message += f"\n🎰 *ДЖЕКПОТ СОРВАН!* 🎰\n"
            result_message += f"💎 *Фруктовое безумие!* 🍒🍋🍊\n"
        
        return result_message, win_amount, sticker_id
    
    def format_ultra_board(self, reels, winning_lines):
        """Ультра-форматирование доски"""
        if not winning_lines:
            return self.format_showcase_board(reels, "", False)
        
        # Создаем ультра-подсвеченную доску
        highlighted = [row.copy() for row in reels]
        
        for line in winning_lines:
            if "Горизонталь" in line:
                i = int(line.split()[1]) - 1
                for j in range(3):
                    highlighted[i][j] = f"🎯{highlighted[i][j]}"
            elif "Вертикаль" in line:
                j = int(line.split()[1]) - 1
                for i in range(3):
                    highlighted[i][j] = f"🎯{highlighted[i][j]}"
            elif "Диагональ ↘️" in line:
                for i in range(3):
                    highlighted[i][i] = f"🎯{highlighted[i][i]}"
            elif "Диагональ ↙️" in line:
                for i in range(3):
                    highlighted[i][2-i] = f"🎯{highlighted[i][2-i]}"
        
        board = "┌─────────┐\n"
        for row in highlighted:
            board += "│ " + " ".join(row) + " │\n"
        board += "└─────────┘"
        return f"```\n{board}```"
    
    def calculate_ultra_win(self, reels, bet):
        """Ультра-расчет выигрыша"""
        lines = []
        multiplier = 0
        jackpot = False
        epic_win = False
        
        # Проверка линий с ультра-бонусами
        for i in range(self.rows):
            if reels[i][0] == reels[i][1] == reels[i][2]:
                lines.append(f"Горизонталь {i+1}")
                symbol_multiplier = self.get_symbol_multiplier(reels[i][0])
                multiplier += symbol_multiplier
        
        for j in range(self.cols):
            if reels[0][j] == reels[1][j] == reels[2][j]:
                lines.append(f"Вертикаль {j+1}")
                symbol_multiplier = self.get_symbol_multiplier(reels[0][j])
                multiplier += symbol_multiplier
        
        if reels[0][0] == reels[1][1] == reels[2][2]:
            lines.append("Диагональ ↘️")
            multiplier += ULTRA_MULTIPLIERS["fruit"]["diagonal"]
        
        if reels[0][2] == reels[1][1] == reels[2][0]:
            lines.append("Диагональ ↙️")
            multiplier += ULTRA_MULTIPLIERS["fruit"]["diagonal"]
        
        # Джекпот и эпические победы
        all_symbols = [symbol for row in reels for symbol in row]
        
        # Эпическая победа (все символы легендарные)
        if all(symbol in ULTRA_SYMBOLS["fruit"]["legendary"] for symbol in all_symbols):
            epic_win = True
            multiplier += 100
        
        # Джекпот (все символы одинаковые)
        elif len(set(all_symbols)) == 1:
            jackpot = True
            multiplier += ULTRA_MULTIPLIERS["fruit"]["jackpot"]
        
        # Бонусы за комбинации
        for symbol in set(all_symbols):
            count = all_symbols.count(symbol)
            if count >= 7:
                multiplier += 5
            if count >= 8:
                multiplier += 3
        
        # Фруктовый бонус
        fruit_count = sum(1 for symbol in all_symbols if symbol in ["🍒", "🍋", "🍊", "🍇", "🍉"])
        if fruit_count >= 6:
            multiplier += ULTRA_MULTIPLIERS["fruit"]["fruit_bonus"]
        
        # Рандомный шанс на эпическую победу
        if random.random() < 0.005:  # 0.5% шанс
            epic_win = True
            multiplier *= 2
        
        win_amount = bet * multiplier if multiplier > 0 else -bet
        return win_amount, multiplier, lines, jackpot, epic_win
    
    def get_symbol_multiplier(self, symbol):
        """Получение множителя для символа"""
        if symbol in ULTRA_SYMBOLS["fruit"]["legendary"]:
            return ULTRA_MULTIPLIERS["fruit"]["special_symbol"] * 2
        elif symbol in ULTRA_SYMBOLS["fruit"]["epic"]:
            return ULTRA_MULTIPLIERS["fruit"]["special_symbol"]
        elif symbol in ULTRA_SYMBOLS["fruit"]["rare"]:
            return ULTRA_MULTIPLIERS["fruit"]["three_horizontal"] * 1.5
        else:
            return ULTRA_MULTIPLIERS["fruit"]["three_horizontal"]