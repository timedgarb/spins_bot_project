import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from config import STICKER_IDS, SPIN_DELAY, ULTRA_ANIMATION_FRAMES, ULTRA_MULTIPLIERS, ULTRA_SYMBOLS

class RetroReelsULTRA:
    def __init__(self):
        self.symbols = (ULTRA_SYMBOLS["retro"]["common"] + 
                       ULTRA_SYMBOLS["retro"]["rare"] + 
                       ULTRA_SYMBOLS["retro"]["epic"] + 
                       ULTRA_SYMBOLS["retro"]["legendary"])
        self.name = "Retro Reels ULTRA"
        self.rows = 3
        self.cols = 3
    
    async def spin_with_animation(self, bet: int, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int):
        chat_id = update.effective_chat.id
        final_reels = self.generate_retro_reels()
        win_amount, multiplier, lines, bonus_round, arcade_legend = self.calculate_retro_win(final_reels, bet)
        
        # РЕТРО-СИКВЕНС АНИМАЦИИ
        await self.retro_cinematic_sequence(update, context, message_id, bet, final_reels, chat_id)
        
        # АРКАДНЫЙ ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
        result_data = await self.create_arcade_result(final_reels, win_amount, multiplier, lines, bonus_round, arcade_legend, bet)
        
        return result_data
    
    def generate_retro_reels(self):
        """Генерация ретро-реелсов с пиксельными весами"""
        reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Пиксельная весовая система
                weights = [40, 30, 20, 10]  # common, rare, epic, legendary
                symbol_pool = []
                categories = list(ULTRA_SYMBOLS["retro"].keys())
                
                for idx, weight in enumerate(weights):
                    symbol_pool.extend([ULTRA_SYMBOLS["retro"][categories[idx]][0]] * weight)
                
                # Ретро-бонус: углы получают бонус к легендарным символам
                if (i == 0 and j == 0) or (i == 2 and j == 2):
                    symbol_pool.extend(ULTRA_SYMBOLS["retro"]["legendary"] * 3)
                
                row.append(random.choice(symbol_pool))
            reels.append(row)
        return reels
    
    async def retro_cinematic_sequence(self, update, context, message_id, bet, final_reels, chat_id):
        """РЕТРО-КИНЕМАТОГРАФИЧЕСКАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ"""
        phases = ULTRA_ANIMATION_FRAMES["retro"]["phases"]
        
        for phase_idx, phase in enumerate(phases):
            phase_text = phase["text"]
            frames = phase["frames"]
            effects = phase["effects"]
            
            for frame_idx, frame in enumerate(frames):
                # Создание ретро-барабанов
                progress = (phase_idx * len(frames) + frame_idx) / (len(phases) * len(frames))
                temp_reels = self.create_pixel_reels(final_reels, progress, effects)
                
                # Пиксельное форматирование доски
                board = self.format_pixel_board(temp_reels, effects, frame_idx)
                
                # Создание ретро-сообщения
                message = self.create_retro_message(phase_text, frame, board, bet, effects, progress)
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Ретро-задержка для аркадного эффекта
                retro_delay = self.calculate_retro_delay(phase_idx, frame_idx, progress)
                await asyncio.sleep(retro_delay)
        
        # АРКАДНЫЙ ШОУКЕЙС
        await self.arcade_showcase(update, context, message_id, final_reels, bet, chat_id)
    
    def create_pixel_reels(self, final_reels, progress, effects):
        """Создание пиксельных барабанов"""
        temp_reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Прогрессивное пиксельное раскрытие
                reveal_chance = min(1.0, progress * 1.4 + random.random() * 0.2)
                
                if random.random() < reveal_chance:
                    row.append(final_reels[i][j])
                else:
                    # Пиксельные эффекты для разных фаз
                    if "pixel_explosion" in effects:
                        row.append(random.choice(["🔴", "🟢", "🟡", "🔵"]))
                    elif "color_cycle" in effects:
                        colors = ["🔴", "🟢", "🟡", "🔵", "🟣", "🟠"]
                        row.append(random.choice(colors))
                    else:
                        row.append(random.choice(self.symbols))
            temp_reels.append(row)
        return temp_reels
    
    def format_pixel_board(self, reels, effects, frame_idx):
        """Пиксельное форматирование доски"""
        board = "┌─────────┐\n"
        
        for i, row in enumerate(reels):
            formatted_row = []
            for j, symbol in enumerate(row):
                # Применение пиксельных эффектов
                if "scan_lines" in effects and i % 2 == 0:
                    formatted_symbol = f"▬{symbol}"
                elif "pixel_glitch" in effects and frame_idx % 3 == 0:
                    formatted_symbol = f"▓{symbol}"
                elif "crt_effect" in effects:
                    formatted_symbol = f"◼{symbol}"
                else:
                    formatted_symbol = symbol
                formatted_row.append(formatted_symbol)
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────┘"
        return f"```\n{board}```"
    
    def create_retro_message(self, phase_text, frame, board, bet, effects, progress):
        """Создание ретро-сообщения"""
        progress_bar = self.create_retro_progress_bar(progress)
        effect_emojis = " ".join(["👾"] * int(progress * 4))
        
        return (
            f"{phase_text}"
            f"{frame} {frame} {frame}\n\n"
            f"{board}\n"
            f"{progress_bar}\n"
            f"💰 Ставка: {bet} 🪙 {effect_emojis}\n"
            f"🕹️ *Аркадный режим: {int(progress * 100)}%*"
        )
    
    def create_retro_progress_bar(self, progress, length=20):
        """Создание ретро-прогресс-бара"""
        filled = int(progress * length)
        empty = length - filled
        return f"🟥{'🟩' * filled}{'⬛' * empty}🟥"
    
    def calculate_retro_delay(self, phase_idx, frame_idx, progress):
        """Расчет ретро-задержки"""
        base_delay = SPIN_DELAY
        
        # Аркадные вариации скорости
        if "pixel_explosion" in ULTRA_ANIMATION_FRAMES["retro"]["phases"][phase_idx]["effects"]:
            return base_delay * 0.7  # Турбо-режим
        elif progress > 0.75:
            return base_delay * 1.6  # Замедление для драмы
        else:
            return base_delay
    
    async def arcade_showcase(self, update, context, message_id, final_reels, bet, chat_id):
        """АРКАДНЫЙ ШОУКЕЙС"""
        arcade_effects = ["👾", "🕹️", "🎮", "💾", "📺", "🔴", "🟢", "🟡"]
        
        for i in range(6):
            effect = arcade_effects[i % len(arcade_effects)]
            
            if i % 2 == 0:
                board = self.format_arcade_showcase_board(final_reels, effect, True)
            else:
                board = self.format_arcade_showcase_board(final_reels, effect, False)
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"🕹️ *Retro Reels ULTRA*\n\n{effect} *АРКАДНЫЙ РЕЗУЛЬТАТ!* {effect}\n\n{board}\n💰 Ставка: {bet} 🪙",
                parse_mode='Markdown'
            )
            await asyncio.sleep(0.4)
    
    def format_arcade_showcase_board(self, reels, effect, enhanced=False):
        """Форматирование доски для аркадного шоукейса"""
        board = "┌─────────┐\n"
        
        for row in reels:
            if enhanced:
                formatted_row = [f"{effect}{symbol}" for symbol in row]
            else:
                formatted_row = row
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────┘"
        return f"```\n{board}```"
    
    async def create_arcade_result(self, final_reels, win_amount, multiplier, lines, bonus_round, arcade_legend, bet):
        """Создание аркадного результата"""
        board = self.format_ultra_retro_board(final_reels, lines if win_amount > 0 else [])
        
        if arcade_legend:
            result_emoji = "👑"
            result_text = f"*ЛЕГЕНДА АРКАДЫ!* 🏆"
            win_info = f"💰 *ЭПИЧЕСКИЙ ВЫИГРЫШ: {win_amount} МОНЕТ!* 💯"
            sticker_id = STICKER_IDS["epic_win"]
        elif bonus_round:
            result_emoji = "🎰"
            result_text = f"*БОНУСНЫЙ РАУНД!* 🎮"
            win_info = f"💰 *СУПЕР ВЫИГРЫШ: {win_amount} монет!* 👾"
            sticker_id = STICKER_IDS["bonus"]
        elif win_amount > 0:
            result_emoji = "🎉"
            result_text = f"*HIGH SCORE!* ⭐"
            win_info = f"💰 *Выигрыш: {win_amount} монет!* (x{multiplier})"
            sticker_id = STICKER_IDS["win"]
        else:
            result_emoji = "🕹️"
            result_text = f"*GAME OVER!* 🔄"
            win_info = f"💸 *Ставка: {bet} монет*"
            sticker_id = STICKER_IDS["lose"]
        
        result_message = (
            f"🕹️ *Retro Reels ULTRA - РЕЗУЛЬТАТ!* {result_emoji}\n\n"
            f"{board}\n"
            f"👾🕹️🎮💾📺🔴🟢🟡🔵👾\n"
            f"{result_text}\n"
            f"{win_info}\n"
        )
        
        if lines and win_amount > 0:
            result_message += f"📊 *Комбо линии:* {', '.join(lines)}\n"
        
        if arcade_legend:
            result_message += f"\n🏆 *ВЫ СТАЛИ ЛЕГЕНДОЙ!* 👑\n"
            result_message += f"🎮 *Аркадные боги с вами!* 👾\n"
        elif bonus_round:
            result_message += f"\n🎰 *БОНУС АКТИВИРОВАН!* 🎮\n"
            result_message += f"💫 *Ретро-удача на максимуме!* 🕹️\n"
        
        return result_message, win_amount, sticker_id
    
    def format_ultra_retro_board(self, reels, winning_lines):
        """Ультра-форматирование ретро-доски"""
        if not winning_lines:
            return self.format_arcade_showcase_board(reels, "", False)
        
        highlighted = [row.copy() for row in reels]
        
        for line in winning_lines:
            if "Горизонталь" in line:
                i = int(line.split()[1]) - 1
                for j in range(3):
                    highlighted[i][j] = f"👾{highlighted[i][j]}"
            elif "Вертикаль" in line:
                j = int(line.split()[1]) - 1
                for i in range(3):
                    highlighted[i][j] = f"👾{highlighted[i][j]}"
            elif "Диагональ" in line:
                if "↘️" in line:
                    for i in range(3):
                        highlighted[i][i] = f"👾{highlighted[i][i]}"
                else:
                    for i in range(3):
                        highlighted[i][2-i] = f"👾{highlighted[i][2-i]}"
        
        board = "┌─────────┐\n"
        for row in highlighted:
            board += "│ " + " ".join(row) + " │\n"
        board += "└─────────┘"
        return f"```\n{board}```"
    
    def calculate_retro_win(self, reels, bet):
        """Ретро-расчет выигрыша"""
        lines = []
        multiplier = 0
        bonus_round = False
        arcade_legend = False
        
        # Стандартные линии
        for i in range(self.rows):
            if reels[i][0] == reels[i][1] == reels[i][2]:
                lines.append(f"Линия {i+1}")
                symbol_multiplier = self.get_retro_symbol_multiplier(reels[i][0])
                multiplier += symbol_multiplier
        
        for j in range(self.cols):
            if reels[0][j] == reels[1][j] == reels[2][j]:
                lines.append(f"Колонка {j+1}")
                symbol_multiplier = self.get_retro_symbol_multiplier(reels[0][j])
                multiplier += symbol_multiplier
        
        if reels[0][0] == reels[1][1] == reels[2][2]:
            lines.append("Диагональ ↘️")
            multiplier += ULTRA_MULTIPLIERS["retro"]["diagonal"]
        
        if reels[0][2] == reels[1][1] == reels[2][0]:
            lines.append("Диагональ ↙️")
            multiplier += ULTRA_MULTIPLIERS["retro"]["diagonal"]
        
        # Бонусный раунд (шанс + комбинация)
        if random.random() < 0.15 and any(reels[i][j] in ULTRA_SYMBOLS["retro"]["epic"] for i in range(3) for j in range(3)):
            bonus_round = True
            multiplier += ULTRA_MULTIPLIERS["retro"]["bonus_round"]
        
        # Пиксельное совершенство (все символы разные цвета)
        color_symbols = [s for s in [symbol for row in reels for symbol in row] if s in ["🔴", "🟢", "🟡", "🔵"]]
        if len(set(color_symbols)) >= 3:
            multiplier += ULTRA_MULTIPLIERS["retro"]["pixel_perfect"]
        
        # Легенда аркады (особая комбинация)
        if self.check_arcade_legend(reels):
            arcade_legend = True
            multiplier += ULTRA_MULTIPLIERS["retro"]["arcade_legend"]
        
        # Ретро-комбо
        unique_retro = len(set(symbol for row in reels for symbol in row))
        if unique_retro >= 7:
            multiplier += ULTRA_MULTIPLIERS["retro"]["retro_combo"]
        
        # Рандомный шанс на легенду аркады
        if random.random() < 0.004:  # 0.4% шанс
            arcade_legend = True
            multiplier *= 2
        
        win_amount = bet * multiplier if multiplier > 0 else -bet
        return win_amount, multiplier, lines, bonus_round, arcade_legend
    
    def get_retro_symbol_multiplier(self, symbol):
        """Получение ретро-множителя"""
        if symbol in ULTRA_SYMBOLS["retro"]["legendary"]:
            return ULTRA_MULTIPLIERS["retro"]["three_horizontal"] * 2
        elif symbol in ULTRA_SYMBOLS["retro"]["epic"]:
            return ULTRA_MULTIPLIERS["retro"]["three_horizontal"] * 1.5
        elif symbol in ULTRA_SYMBOLS["retro"]["rare"]:
            return ULTRA_MULTIPLIERS["retro"]["three_horizontal"]
        else:
            return ULTRA_MULTIPLIERS["retro"]["three_horizontal"] * 0.8
    
    def check_arcade_legend(self, reels):
        """Проверка легенды аркады"""
        # Легенда: все углы + центр - легендарные символы
        corners_and_center = [reels[0][0], reels[0][2], reels[2][0], reels[2][2], reels[1][1]]
        return all(symbol in ULTRA_SYMBOLS["retro"]["legendary"] for symbol in corners_and_center)