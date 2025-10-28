import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from config import STICKER_IDS, SPIN_DELAY, ULTRA_ANIMATION_FRAMES, ULTRA_MULTIPLIERS, ULTRA_SYMBOLS

class EgyptSlotsULTRA:
    def __init__(self):
        self.symbols = (ULTRA_SYMBOLS["egypt"]["common"] + 
                       ULTRA_SYMBOLS["egypt"]["rare"] + 
                       ULTRA_SYMBOLS["egypt"]["epic"] + 
                       ULTRA_SYMBOLS["egypt"]["legendary"])
        self.name = "Egypt Slots ULTRA"
        self.rows = 4
        self.cols = 4
    
    async def spin_with_animation(self, bet: int, update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int):
        chat_id = update.effective_chat.id
        final_reels = self.generate_egypt_reels()
        win_amount, multiplier, lines, pharaoh_bonus, royal_treasure = self.calculate_egypt_win(final_reels, bet)
        
        # ЕГИПЕТСКАЯ СИКВЕНС АНИМАЦИИ
        await self.egypt_cinematic_sequence(update, context, message_id, bet, final_reels, chat_id)
        
        # ФАРАОНСКИЙ ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
        result_data = await self.create_pharaoh_result(final_reels, win_amount, multiplier, lines, pharaoh_bonus, royal_treasure, bet)
        
        return result_data
    
    def generate_egypt_reels(self):
        """Генерация египетских реелсов с иероглифическими весами"""
        reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Иероглифическая весовая система
                weights = [35, 30, 25, 10]  # common, rare, epic, legendary
                symbol_pool = []
                categories = list(ULTRA_SYMBOLS["egypt"].keys())
                
                for idx, weight in enumerate(weights):
                    symbol_pool.extend([ULTRA_SYMBOLS["egypt"][categories[idx]][0]] * weight)
                
                # Египетский бонус: центр пирамиды получает бонус
                if (1 <= i <= 2) and (1 <= j <= 2):
                    symbol_pool.extend(ULTRA_SYMBOLS["egypt"]["epic"] * 5)
                    symbol_pool.extend(ULTRA_SYMBOLS["egypt"]["legendary"] * 2)
                
                row.append(random.choice(symbol_pool))
            reels.append(row)
        return reels
    
    async def egypt_cinematic_sequence(self, update, context, message_id, bet, final_reels, chat_id):
        """ЕГИПЕТСКАЯ КИНЕМАТОГРАФИЧЕСКАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ"""
        phases = ULTRA_ANIMATION_FRAMES["egypt"]["phases"]
        
        for phase_idx, phase in enumerate(phases):
            phase_text = phase["text"]
            frames = phase["frames"]
            effects = phase["effects"]
            
            for frame_idx, frame in enumerate(frames):
                # Создание египетских барабанов
                progress = (phase_idx * len(frames) + frame_idx) / (len(phases) * len(frames))
                temp_reels = self.create_pyramid_reels(final_reels, progress, effects)
                
                # Иероглифическое форматирование доски
                board = self.format_pyramid_board(temp_reels, effects, frame_idx)
                
                # Создание египетского сообщения
                message = self.create_egypt_message(phase_text, frame, board, bet, effects, progress)
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Египетская задержка для загадочного эффекта
                egypt_delay = self.calculate_egypt_delay(phase_idx, frame_idx, progress)
                await asyncio.sleep(egypt_delay)
        
        # ФАРАОНСКИЙ ШОУКЕЙС
        await self.pharaoh_showcase(update, context, message_id, final_reels, bet, chat_id)
    
    def create_pyramid_reels(self, final_reels, progress, effects):
        """Создание пирамидальных барабанов"""
        temp_reels = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # Прогрессивное иероглифическое раскрытие
                reveal_chance = min(1.0, progress * 1.2 + ((i+j)/(self.rows+self.cols)) * 0.6)
                
                if random.random() < reveal_chance:
                    row.append(final_reels[i][j])
                else:
                    # Египетские эффекты для разных фаз
                    if "sandstorm" in effects:
                        row.append(random.choice(["🏜️", "🌵", "🐫", "🦂"]))
                    elif "gold_glow" in effects:
                        row.append(random.choice(["💎", "👑", "⚱️", "🏺"]))
                    else:
                        row.append(random.choice(self.symbols))
            temp_reels.append(row)
        return temp_reels
    
    def format_pyramid_board(self, reels, effects, frame_idx):
        """Пирамидальное форматирование доски"""
        board = "┌───────────────┐\n"
        
        for i, row in enumerate(reels):
            formatted_row = []
            for j, symbol in enumerate(row):
                # Применение египетских эффектов
                if "hieroglyph_reveal" in effects and frame_idx % 4 == 0:
                    formatted_symbol = f"📜{symbol}"
                elif "torch_light" in effects and (i + j) % 2 == 0:
                    formatted_symbol = f"🪔{symbol}"
                elif "divine_light" in effects:
                    formatted_symbol = f"🌟{symbol}"
                else:
                    formatted_symbol = symbol
                formatted_row.append(formatted_symbol)
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└───────────────┘"
        return f"```\n{board}```"
    
    def create_egypt_message(self, phase_text, frame, board, bet, effects, progress):
        """Создание египетского сообщения"""
        progress_bar = self.create_pyramid_progress_bar(progress)
        effect_emojis = " ".join(["🔱"] * int(progress * 5))
        
        return (
            f"{phase_text}"
            f"{frame} {frame} {frame}\n\n"
            f"{board}\n"
            f"{progress_bar}\n"
            f"💰 Ставка: {bet} 🪙 {effect_emojis}\n"
            f"🐫 *Режим фараона: {int(progress * 100)}%*"
        )
    
    def create_pyramid_progress_bar(self, progress, length=20):
        """Создание пирамидального прогресс-бара"""
        filled = int(progress * length)
        empty = length - filled
        return f"🔺{'🔸' * filled}{'▫️' * empty}🔺"
    
    def calculate_egypt_delay(self, phase_idx, frame_idx, progress):
        """Расчет египетской задержки"""
        base_delay = SPIN_DELAY
        
        # Загадочные вариации скорости
        if "ritual_fire" in ULTRA_ANIMATION_FRAMES["egypt"]["phases"][phase_idx]["effects"]:
            return base_delay * 0.8  # Ускорение ритуала
        elif progress > 0.85:
            return base_delay * 2.0  # Драматическое замедление
        else:
            return base_delay
    
    async def pharaoh_showcase(self, update, context, message_id, final_reels, bet, chat_id):
        """ФАРАОНСКИЙ ШОУКЕЙС"""
        pharaoh_effects = ["👑", "⚱️", "💎", "🔱", "🏺", "🐫", "🦂", "📜"]
        
        for i in range(7):
            effect = pharaoh_effects[i % len(pharaoh_effects)]
            
            if i % 2 == 0:
                board = self.format_pharaoh_showcase_board(final_reels, effect, True)
            else:
                board = self.format_pharaoh_showcase_board(final_reels, effect, False)
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"🐫 *Egypt Slots ULTRA*\n\n{effect} *ФАРАОНСКИЙ РЕЗУЛЬТАТ!* {effect}\n\n{board}\n💰 Ставка: {bet} 🪙",
                parse_mode='Markdown'
            )
            await asyncio.sleep(0.45)
    
    def format_pharaoh_showcase_board(self, reels, effect, enhanced=False):
        """Форматирование доски для фараонского шоукейса"""
        board = "┌───────────────┐\n"
        
        for row in reels:
            if enhanced:
                formatted_row = [f"{effect}{symbol}" for symbol in row]
            else:
                formatted_row = row
            
            board += f"│ {' '.join(formatted_row)} │\n"
        
        board += "└───────────────┘"
        return f"```\n{board}```"
    
    async def create_pharaoh_result(self, final_reels, win_amount, multiplier, lines, pharaoh_bonus, royal_treasure, bet):
        """Создание фараонского результата"""
        board = self.format_ultra_egypt_board(final_reels, lines if win_amount > 0 else [])
        
        if royal_treasure:
            result_emoji = "💎"
            result_text = f"*КОРОЛЕВСКОЕ СОКРОВИЩЕ!* 👑"
            win_info = f"💰 *ВЕЛИКИЙ ВЫИГРЫШ: {win_amount} МОНЕТ!* 🏆"
            sticker_id = STICKER_IDS["epic_win"]
        elif pharaoh_bonus:
            result_emoji = "👑"
            result_text = f"*БЛАГОСЛОВЕНИЕ ФАРАОНА!* ⚱️"
            win_info = f"💰 *ФАРАОНСКИЙ ВЫИГРЫШ: {win_amount} монет!* 💎"
            sticker_id = STICKER_IDS["jackpot"]
        elif win_amount > 0:
            result_emoji = "🎉"
            result_text = f"*СОКРОВИЩА ПИРАМИДЫ!* 🔱"
            win_info = f"💰 *Выигрыш: {win_amount} монет!* (x{multiplier})"
            sticker_id = STICKER_IDS["win"]
        else:
            result_emoji = "🐫"
            result_text = f"*ПУТЬ К СОКРОВИЩАМ ПРОДОЛЖАЕТСЯ!* 🏜️"
            win_info = f"💸 *Ставка: {bet} монет*"
            sticker_id = STICKER_IDS["lose"]
        
        result_message = (
            f"🐫 *Egypt Slots ULTRA - РЕЗУЛЬТАТ!* {result_emoji}\n\n"
            f"{board}\n"
            f"👑⚱️💎🔱🏺🐫🦂📜🌵🏜️\n"
            f"{result_text}\n"
            f"{win_info}\n"
        )
        
        if lines and win_amount > 0:
            result_message += f"📜 *Сакральные линии:* {', '.join(lines)}\n"
        
        if royal_treasure:
            result_message += f"\n💎 *КОРОЛЕВСКАЯ УДАЧА!* 👑\n"
            result_message += f"🏆 *Сокровища фараонов ваши!* ⚱️\n"
        elif pharaoh_bonus:
            result_message += f"\n👑 *БЛАГОСЛОВЕНИЕ ФАРАОНА!* ⚱️\n"
            result_message += f"🌟 *Древние боги с вами!* 🔱\n"
        
        return result_message, win_amount, sticker_id
    
    def format_ultra_egypt_board(self, reels, winning_lines):
        """Ультра-форматирование египетской доски"""
        if not winning_lines:
            return self.format_pharaoh_showcase_board(reels, "", False)
        
        highlighted = [row.copy() for row in reels]
        
        for line in winning_lines:
            if "Горизонталь" in line:
                i = int(line.split()[1]) - 1
                for j in range(self.cols):
                    highlighted[i][j] = f"💎{highlighted[i][j]}"
            elif "Вертикаль" in line:
                j = int(line.split()[1]) - 1
                for i in range(self.rows):
                    highlighted[i][j] = f"💎{highlighted[i][j]}"
            elif "Квадрат" in line:
                coords = line.split()[-1].split('-')
                i, j = int(coords[0]), int(coords[1])
                for x in range(i, i+2):
                    for y in range(j, j+2):
                        highlighted[x][y] = f"💎{highlighted[x][y]}"
        
        board = "┌───────────────┐\n"
        for row in highlighted:
            board += "│ " + " ".join(row) + " │\n"
        board += "└───────────────┘"
        return f"```\n{board}```"
    
    def calculate_egypt_win(self, reels, bet):
        """Египетский расчет выигрыша"""
        lines = []
        multiplier = 0
        pharaoh_bonus = False
        royal_treasure = False
        
        # Горизонтальные линии (4 символа)
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if reels[i][j] == reels[i][j+1] == reels[i][j+2] == reels[i][j+3]:
                    lines.append(f"Горизонталь {i+1}-{j+1}")
                    symbol_multiplier = self.get_egypt_symbol_multiplier(reels[i][j])
                    multiplier += symbol_multiplier
        
        # Вертикальные линии (4 символа)
        for j in range(self.cols):
            for i in range(self.rows - 3):
                if reels[i][j] == reels[i+1][j] == reels[i+2][j] == reels[i+3][j]:
                    lines.append(f"Вертикаль {j+1}-{i+1}")
                    symbol_multiplier = self.get_egypt_symbol_multiplier(reels[i][j])
                    multiplier += symbol_multiplier
        
        # Квадраты 2x2
        for i in range(self.rows - 1):
            for j in range(self.cols - 1):
                if (reels[i][j] == reels[i][j+1] == reels[i+1][j] == reels[i+1][j+1]):
                    lines.append(f"Квадрат {i+1}-{j+1}")
                    multiplier += ULTRA_MULTIPLIERS["egypt"]["square"]
        
        # Бонус фараона
        if self.check_pharaoh_bonus(reels):
            pharaoh_bonus = True
            multiplier += ULTRA_MULTIPLIERS["egypt"]["pharaoh_bonus"]
        
        # Пирамидальная комбинация
        if self.check_pyramid_combo(reels):
            multiplier += ULTRA_MULTIPLIERS["egypt"]["pyramid_combo"]
        
        # Иероглифический бонус
        scroll_count = sum(row.count("📜") for row in reels)
        if scroll_count >= 3:
            multiplier += ULTRA_MULTIPLIERS["egypt"]["hieroglyph_bonus"]
        
        # Королевское сокровище
        if self.check_royal_treasure(reels):
            royal_treasure = True
            multiplier += ULTRA_MULTIPLIERS["egypt"]["royal_treasure"]
        
        # Рандомный шанс на королевское сокровище
        if random.random() < 0.002:  # 0.2% шанс
            royal_treasure = True
            multiplier *= 4
        
        win_amount = bet * multiplier if multiplier > 0 else -bet
        return win_amount, multiplier, lines, pharaoh_bonus, royal_treasure
    
    def get_egypt_symbol_multiplier(self, symbol):
        """Получение египетского множителя"""
        if symbol in ULTRA_SYMBOLS["egypt"]["legendary"]:
            return ULTRA_MULTIPLIERS["egypt"]["four_horizontal"] * 2.5
        elif symbol in ULTRA_SYMBOLS["egypt"]["epic"]:
            return ULTRA_MULTIPLIERS["egypt"]["four_horizontal"] * 1.8
        elif symbol in ULTRA_SYMBOLS["egypt"]["rare"]:
            return ULTRA_MULTIPLIERS["egypt"]["four_horizontal"] * 1.3
        else:
            return ULTRA_MULTIPLIERS["egypt"]["four_horizontal"]
    
    def check_pharaoh_bonus(self, reels):
        """Проверка бонуса фараона"""
        # Фараонский бонус: корона и саркофаг в центре пирамиды
        center_symbols = [reels[1][1], reels[1][2], reels[2][1], reels[2][2]]
        return "👑" in center_symbols and "⚱️" in center_symbols
    
    def check_pyramid_combo(self, reels):
        """Проверка пирамидальной комбинации"""
        # Пирамида: углы + центр образуют пирамиду
        pyramid_positions = [(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,1), (3,2)]
        pyramid_symbols = [reels[i][j] for i, j in pyramid_positions]
        return len(set(pyramid_symbols)) == 1
    
    def check_royal_treasure(self, reels):
        """Проверка королевского сокровища"""
        # Королевское сокровище: все легендарные символы
        all_symbols = [symbol for row in reels for symbol in row]
        return all(symbol in ULTRA_SYMBOLS["egypt"]["legendary"] for symbol in all_symbols)