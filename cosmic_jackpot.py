import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from config import STICKER_IDS, SPIN_DELAY, ULTRA_ANIMATION_FRAMES, ULTRA_MULTIPLIERS, ULTRA_SYMBOLS

class CosmicJackpotULTRA:
    def __init__(self):
        self.symbols = (ULTRA_SYMBOLS["cosmic"]["common"] + 
                       ULTRA_SYMBOLS["cosmic"]["rare"] + 
                       ULTRA_SYMBOLS["cosmic"]["epic"] + 
                       ULTRA_SYMBOLS["cosmic"]["legendary"])
        self.name = "Cosmic Jackpot ULTRA"
        self.rows = 3
        self.cols = 5
    
    async def spin_with_animation(self, bet: int, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int):
        chat_id = update.effective_chat.id
        final_reels = self.generate_cosmic_reels()
        win_amount, multiplier, lines, cosmic_jackpot, alien_invasion = self.calculate_cosmic_win(final_reels, bet)
        
        # КОСМИЧЕСКАЯ СИКВЕНС АНИМАЦИИ
        await self.cosmic_cinematic_sequence(update, context, message_id, bet, final_reels, chat_id)
        
        # ГАЛАКТИЧЕСКИЙ ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
        result_data = await self.create_galactic_result(final_reels, win_amount, multiplier, lines, cosmic_jackpot, alien_invasion, bet)
        
        return result_data
    
    def generate_cosmic_reels(self):
        """Генерация космических реелсов с квантовыми весами"""
        reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Квантовая весовая система
                weights = [45, 25, 20, 10]  # common, rare, epic, legendary
                symbol_pool = []
                categories = list(ULTRA_SYMBOLS["cosmic"].keys())
                
                for idx, weight in enumerate(weights):
                    symbol_pool.extend([ULTRA_SYMBOLS["cosmic"][categories[idx]][0]] * weight)
                
                # Космический бонус: шанс на редкий символ увеличивается к краям
                if j == 0 or j == self.cols - 1:
                    symbol_pool.extend(ULTRA_SYMBOLS["cosmic"]["epic"] * 5)
                
                row.append(random.choice(symbol_pool))
            reels.append(row)
        return reels
    
    async def cosmic_cinematic_sequence(self, update, context, message_id, bet, final_reels, chat_id):
        """КОСМИЧЕСКАЯ КИНЕМАТОГРАФИЧЕСКАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ"""
        phases = ULTRA_ANIMATION_FRAMES["cosmic"]["phases"]
        
        for phase_idx, phase in enumerate(phases):
            phase_text = phase["text"]
            frames = phase["frames"]
            effects = phase["effects"]
            
            for frame_idx, frame in enumerate(frames):
                # Создание космических барабанов
                progress = (phase_idx * len(frames) + frame_idx) / (len(phases) * len(frames))
                temp_reels = self.create_galactic_reels(final_reels, progress, effects)
                
                # Галактическое форматирование доски
                board = self.format_galactic_board(temp_reels, effects, frame_idx)
                
                # Создание космического сообщения
                message = self.create_cosmic_message(phase_text, frame, board, bet, effects, progress)
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Космическая задержка для межзвездного эффекта
                cosmic_delay = self.calculate_cosmic_delay(phase_idx, frame_idx, progress)
                await asyncio.sleep(cosmic_delay)
        
        # МЕЖГАЛАКТИЧЕСКИЙ ШОУКЕЙС
        await self.galactic_showcase(update, context, message_id, final_reels, bet, chat_id)
    
    def create_galactic_reels(self, final_reels, progress, effects):
        """Создание галактических барабанов"""
        temp_reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Прогрессивное космическое раскрытие
                reveal_chance = min(1.0, progress * 1.3 + (j/self.cols) * 0.4)
                
                if random.random() < reveal_chance:
                    row.append(final_reels[i][j])
                else:
                    # Космические эффекты для разных фаз
                    if "warp_speed" in effects:
                        row.append(random.choice(["💫", "🌠", "✨", "⭐"]))
                    elif "alien_glow" in effects:
                        row.append(random.choice(["👽", "🛸", "👾", "🔭"]))
                    else:
                        row.append(random.choice(self.symbols))
            temp_reels.append(row)
        return temp_reels
    
    def format_galactic_board(self, reels, effects, frame_idx):
        """Галактическое форматирование доски"""
        board = "┌─────────────────┐\n"
        
        for i, row in enumerate(reels):
            formatted_row = []
            for j, symbol in enumerate(row):
                # Применение космических эффектов
                if "star_trail" in effects and j > 0:
                    formatted_symbol = f"✨{symbol}"
                elif "nebula_effect" in effects:
                    formatted_symbol = f"🌌{symbol}"
                elif "alien_glow" in effects and "👽" in symbol:
                    formatted_symbol = f"🛸{symbol}"
                else:
                    formatted_symbol = symbol
                formatted_row.append(formatted_symbol)
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────────────┘"
        return f"```\n{board}```"
    
    def create_cosmic_message(self, phase_text, frame, board, bet, effects, progress):
        """Создание космического сообщения"""
        progress_bar = self.create_cosmic_progress_bar(progress)
        effect_emojis = " ".join(["⭐"] * int(progress * 6))
        
        return (
            f"{phase_text}"
            f"{frame} {frame} {frame}\n\n"
            f"{board}\n"
            f"{progress_bar}\n"
            f"💰 Ставка: {bet} 🪙 {effect_emojis}\n"
            f"🚀 *Космический режим: {int(progress * 100)}%*"
        )
    
    def create_cosmic_progress_bar(self, progress, length=20):
        """Создание космического прогресс-бара"""
        filled = int(progress * length)
        empty = length - filled
        return f"🌕{'⭐' * filled}{'🌑' * empty}🌕"
    
    def calculate_cosmic_delay(self, phase_idx, frame_idx, progress):
        """Расчет космической задержки"""
        base_delay = SPIN_DELAY
        
        # Гиперпространственные вариации
        if "warp_speed" in ULTRA_ANIMATION_FRAMES["cosmic"]["phases"][phase_idx]["effects"]:
            return base_delay * 0.6  # Сверхсветовая скорость
        elif progress > 0.8:
            return base_delay * 1.8  # Замедление при подходе к цели
        else:
            return base_delay
    
    async def galactic_showcase(self, update, context, message_id, final_reels, bet, chat_id):
        """МЕЖГАЛАКТИЧЕСКИЙ ШОУКЕЙС"""
        cosmic_effects = ["👽", "🛸", "🌌", "💫", "🌠", "✨", "⭐", "🪐"]
        
        for i in range(8):
            effect = cosmic_effects[i % len(cosmic_effects)]
            
            if i % 2 == 0:
                board = self.format_cosmic_showcase_board(final_reels, effect, True)
            else:
                board = self.format_cosmic_showcase_board(final_reels, effect, False)
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"🚀 *Cosmic Jackpot ULTRA*\n\n{effect} *ГАЛАКТИЧЕСКИЙ РЕЗУЛЬТАТ!* {effect}\n\n{board}\n💰 Ставка: {bet} 🪙",
                parse_mode='Markdown'
            )
            await asyncio.sleep(0.35)
    
    def format_cosmic_showcase_board(self, reels, effect, enhanced=False):
        """Форматирование доски для космического шоукейса"""
        board = "┌─────────────────┐\n"
        
        for row in reels:
            if enhanced:
                formatted_row = [f"{effect}{symbol}" for symbol in row]
            else:
                formatted_row = row
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└─────────────────┘"
        return f"```\n{board}```"
    
    async def create_galactic_result(self, final_reels, win_amount, multiplier, lines, cosmic_jackpot, alien_invasion, bet):
        """Создание галактического результата"""
        board = self.format_ultra_cosmic_board(final_reels, lines if win_amount > 0 else [])
        
        if alien_invasion:
            result_emoji = "👽"
            result_text = f"*ИНОПЛАНЕТНОЕ ВТОРЖЕНИЕ!* 🛸"
            win_info = f"💰 *КОСМИЧЕСКИЙ ВЫИГРЫШ: {win_amount} МОНЕТ!* 🌌"
            sticker_id = STICKER_IDS["epic_win"]
        elif cosmic_jackpot:
            result_emoji = "🌌"
            result_text = f"*КОСМИЧЕСКИЙ ДЖЕКПОТ!* 🚀"
            win_info = f"💰 *МЕЖГАЛАКТИЧЕСКИЙ ВЫИГРЫШ: {win_amount} МОНЕТ!* 💫"
            sticker_id = STICKER_IDS["jackpot"]
        elif win_amount > 0:
            result_emoji = "⭐"
            result_text = f"*ОРБИТАЛЬНАЯ ПОБЕДА!* 🛰️"
            win_info = f"💰 *Выигрыш: {win_amount} монет!* (x{multiplier})"
            sticker_id = STICKER_IDS["win"]
        else:
            result_emoji = "🪐"
            result_text = f"*Следующая галактика ждет!* 🌠"
            win_info = f"💸 *Ставка: {bet} монет*"
            sticker_id = STICKER_IDS["lose"]
        
        result_message = (
            f"🚀 *Cosmic Jackpot ULTRA - РЕЗУЛЬТАТ!* {result_emoji}\n\n"
            f"{board}\n"
            f"🌌🌠⭐💫✨🌕🪐🌙🌠🌌\n"
            f"{result_text}\n"
            f"{win_info}\n"
        )
        
        if lines and win_amount > 0:
            result_message += f"📡 *Активированные орбиты:* {', '.join(lines)}\n"
        
        if alien_invasion:
            result_message += f"\n👽 *ИНОПЛАНЕТЯНЕ С ВАМИ!* 🛸\n"
            result_message += f"🌌 *Космические силы принесли удачу!* ✨\n"
        elif cosmic_jackpot:
            result_message += f"\n🚀 *КОСМИЧЕСКИЙ ДЖЕКПОТ!* 🌌\n"
            result_message += f"💫 *Вы покорили галактику!* 🪐\n"
        
        return result_message, win_amount, sticker_id
    
    def format_ultra_cosmic_board(self, reels, winning_lines):
        """Ультра-форматирование космической доски"""
        if not winning_lines:
            return self.format_cosmic_showcase_board(reels, "", False)
        
        highlighted = [row.copy() for row in reels]
        
        for line in winning_lines:
            if "Горизонталь" in line:
                i = int(line.split()[1]) - 1
                for j in range(self.cols):
                    highlighted[i][j] = f"⭐{highlighted[i][j]}"
            elif "Вертикаль" in line:
                # В Cosmic Jackpot вертикальные линии не стандартные
                pass
        
        board = "┌─────────────────┐\n"
        for row in highlighted:
            board += "│ " + " ".join(row) + " │\n"
        board += "└─────────────────┘"
        return f"```\n{board}```"
    
    def calculate_cosmic_win(self, reels, bet):
        """Космический расчет выигрыша"""
        lines = []
        multiplier = 0
        cosmic_jackpot = False
        alien_invasion = False
        
        # Проверка горизонтальных линий (3-5 символов)
        for i in range(self.rows):
            for length in [5, 4, 3]:
                for j in range(self.cols - length + 1):
                    if len(set(reels[i][j:j+length])) == 1:
                        line_name = f"Орбита {i+1}-{j+1}"
                        lines.append(line_name)
                        symbol_multiplier = self.get_cosmic_symbol_multiplier(reels[i][j], length)
                        multiplier += symbol_multiplier
                        break
        
        # Инопланетное вторжение (3+ инопланетян)
        alien_count = sum(row.count("👽") for row in reels)
        if alien_count >= 3:
            alien_invasion = True
            multiplier += ULTRA_MULTIPLIERS["cosmic"]["alien_bonus"] * alien_count
        
        # Планетарный бонус
        planet_count = sum(row.count("🪐") + row.count("🌍") for row in reels)
        if planet_count >= 4:
            multiplier += ULTRA_MULTIPLIERS["cosmic"]["planet_combo"]
        
        # Космический джекпот (особая комбинация)
        if self.check_cosmic_jackpot(reels):
            cosmic_jackpot = True
            multiplier += ULTRA_MULTIPLIERS["cosmic"]["cosmic_jackpot"]
        
        # Галактический бонус (все разные космические символы)
        unique_cosmic = len(set(symbol for row in reels for symbol in row if symbol in ["🚀", "🛸", "👽", "🪐", "🌍"]))
        if unique_cosmic >= 4:
            multiplier += ULTRA_MULTIPLIERS["cosmic"]["galactic_bonus"]
        
        # Рандомный шанс на инопланетное вторжение
        if random.random() < 0.003:  # 0.3% шанс
            alien_invasion = True
            multiplier *= 3
        
        win_amount = bet * multiplier if multiplier > 0 else -bet
        return win_amount, multiplier, lines, cosmic_jackpot, alien_invasion
    
    def get_cosmic_symbol_multiplier(self, symbol, length):
        """Получение космического множителя"""
        base_multipliers = {
            3: ULTRA_MULTIPLIERS["cosmic"]["three_in_row"],
            4: ULTRA_MULTIPLIERS["cosmic"]["four_in_row"], 
            5: ULTRA_MULTIPLIERS["cosmic"]["five_in_row"]
        }
        
        base = base_multipliers.get(length, 1)
        
        if symbol in ULTRA_SYMBOLS["cosmic"]["legendary"]:
            return base * 3
        elif symbol in ULTRA_SYMBOLS["cosmic"]["epic"]:
            return base * 2
        elif symbol in ULTRA_SYMBOLS["cosmic"]["rare"]:
            return base * 1.5
        else:
            return base
    
    def check_cosmic_jackpot(self, reels):
        """Проверка космического джекпота"""
        # Джекпот: все символы в средней строке одинаковые И есть инопланетянин
        middle_row = reels[1]
        if len(set(middle_row)) == 1 and "👽" in [symbol for row in reels for symbol in row]:
            return True
        return False