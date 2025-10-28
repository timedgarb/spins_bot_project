import os
from datetime import datetime

# ==================== BOT CONFIGURATION ====================
BOT_TOKEN = "000000000000000000"
CREATOR_USERNAME = "Timed_Garb"
CREATOR_NAME = "Timed Garb"
BOT_VERSION = "3.0.0"
LAUNCH_DATE = "2024-01-20"

# ==================== STICKER CONFIGURATION ====================
STICKER_IDS = {
    "win": "CAACAgEAAxkBAAEPKetooEEgAaf--p0bdtEcbcfQIuF8fAACEgADPRpJTFS5y5sbRkrMNgQ",
    "lose": "CAACAgIAAxkBAAEPmVVo9UqsFJOr9SNAR5AWVbP8YK3WtAAC0QQAAiBtOwABFpAsMNBwYBg2BA",
    "jackpot": "CAACAgIAAxkBAAEPmVdo9UrvQ7vJ9UYAAW7k6QABXK4AAX4QAALRBQACIG07AAEWkCww0HBgGDYE",
    "bonus": "CAACAgEAAxkBAAEPmWVo9VpMH3V58tmYe5jAl7yLm00QhwACEAADsV3gTW95WXexW4F7NgQ",
    "mega_win": "CAACAgEAAxkBAAEPmWNo9Vnyt9vB78Zm2lABzJW5moZ8jgACBQADzkupTsoQUQf-wQABZzYE",
    "epic_win": "CAACAgEAAxkBAAEPmWFo9VnMz62Ek_q4HWE5hCrUjs3IiwACBwADNXxZTxvhrdpyc0ayNgQ"
}

# ==================== GAME ECONOMY ====================
INITIAL_BALANCE = 1000
MIN_BET = 10
MAX_BET = 5000
DAILY_BONUS = 100
WELCOME_BONUS = 500

# ==================== ADMIN SETTINGS ====================
ADMIN_IDS = [000000000]
SUPER_ADMIN_IDS = [0000000000]

# ==================== ULTRA ANIMATION SETTINGS ====================
# Core Animation Timing
SPIN_DELAY = 0.25
ULTRA_ANIMATION = True
CINEMATIC_MODE = True

# Phase Settings
ANIMATION_PHASES = 6
PHASE_DURATION = 0.3
FINAL_PHASE_DURATION = 0.8

# Visual Effects
FLASH_EFFECTS = True
GLOW_EFFECTS = True 
PARTICLE_EFFECTS = True
RAINBOW_EFFECTS = True
NEON_EFFECTS = True

# Advanced Effects
BLUR_EFFECT = True
SHAKE_EFFECT = True
ZOOM_EFFECT = True
FADE_EFFECT = True

# Performance
MAX_FRAME_RATE = 60
ANIMATION_QUALITY = "ULTRA"

# ==================== GAME GRID CONFIGURATION ====================
GRID_CONFIG = {
    "fruit": {"rows": 3, "cols": 3},
    "cosmic": {"rows": 3, "cols": 5},
    "retro": {"rows": 3, "cols": 3},
    "egypt": {"rows": 4, "cols": 4}
}

# ==================== ENHANCED ANIMATION FRAMES ====================
ULTRA_ANIMATION_FRAMES = {
    "fruit": {
        "phases": [
            {
                "name": "SYSTEM_BOOT",
                "text": "🎰 *Fruit Slots ULTRA*\n\n⚙️ *ЗАПУСК СИСТЕМЫ...*\n\n",
                "frames": ["🔋", "⚡", "💻", "🚀"],
                "effects": ["vibrate", "glow"]
            },
            {
                "name": "REEL_ACCELERATION", 
                "text": "🎰 *Fruit Slots ULTRA*\n\n🌀 *РАЗГОН БАРАБАНОВ...*\n\n",
                "frames": ["🎡", "💫", "🌟", "✨"],
                "effects": ["spin_fast", "blur"]
            },
            {
                "name": "MAXIMUM_VELOCITY",
                "text": "🎰 *Fruit Slots ULTRA*\n\n⚡ *МАКСИМАЛЬНАЯ СКОРОСТЬ!*\n\n", 
                "frames": ["🚀", "🌈", "🎇", "🎆"],
                "effects": ["turbo", "rainbow"]
            },
            {
                "name": "COSMIC_ALIGNMENT",
                "text": "🎰 *Fruit Slots ULTRA*\n\n🌌 *КОСМИЧЕСКОЕ ВЫРАВНИВАНИЕ...*\n\n",
                "frames": ["🪐", "⭐", "🌠", "💫"],
                "effects": ["align", "glow"]
            },
            {
                "name": "QUANTUM_DECELERATION",
                "text": "🎰 *Fruit Slots ULTRA*\n\n⏳ *КВАНТОВОЕ ЗАМЕДЛЕНИЕ...*\n\n",
                "frames": ["🔄", "⚗️", "🔬", "🎯"],
                "effects": ["slow_motion", "focus"]
            },
            {
                "name": "FINAL_REVEAL",
                "text": "🎰 *Fruit Slots ULTRA*\n\n🎊 *ФИНАЛЬНОЕ ОТКРЫТИЕ!*\n\n",
                "frames": ["💥", "🎉", "🏆", "💰"],
                "effects": ["explode", "celebrate"]
            }
        ]
    },
    "cosmic": {
        "phases": [
            {
                "name": "LAUNCH_SEQUENCE",
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n🛰️ *ПОСЛЕДОВАТЕЛЬНОСТЬ ЗАПУСКА...*\n\n",
                "frames": ["🔋", "⚡", "💻", "🚀"],
                "effects": ["countdown", "vibrate"]
            },
            {
                "name": "ORBITAL_ASCENT",
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n🌌 *ОРБИТАЛЬНЫЙ ПОДЪЕМ...*\n\n",
                "frames": ["🛸", "👨‍🚀", "🌍", "🪐"],
                "effects": ["lift_off", "glow"]
            },
            {
                "name": "HYPERSPACE_TRAVEL",
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n⭐ *ПУТЕШЕСТВИЕ В ГИПЕРПРОСТРАНСТВЕ!*\n\n",
                "frames": ["💫", "🌠", "✨", "🌟"],
                "effects": ["warp_speed", "star_trail"]
            },
            {
                "name": "GALACTIC_NAVIGATION", 
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n🪐 *ГАЛАКТИЧЕСКАЯ НАВИГАЦИЯ...*\n\n",
                "frames": ["🗺️", "🧭", "🎯", "📍"],
                "effects": ["scan", "target_lock"]
            },
            {
                "name": "NEBULA_APPROACH",
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n🌠 *ПРИБЛИЖЕНИЕ К ТУМАННОСТИ...*\n\n",
                "frames": ["☁️", "💨", "🌈", "🎇"],
                "effects": ["nebula_effect", "color_shift"]
            },
            {
                "name": "COSMIC_REVEAL",
                "text": "🚀 *Cosmic Jackpot ULTRA*\n\n👽 *КОСМИЧЕСКОЕ ОТКРЫТИЕ!*\n\n",
                "frames": ["🛸", "👾", "💎", "🏆"],
                "effects": ["alien_glow", "cosmic_celebration"]
            }
        ]
    },
    "retro": {
        "phases": [
            {
                "name": "RETRO_BOOT",
                "text": "🕹️ *Retro Reels ULTRA*\n\n💾 *РЕТРО-ЗАГРУЗКА...*\n\n",
                "frames": ["⌛", "⏳", "💿", "📼"],
                "effects": ["pixel_glitch", "scan_lines"]
            },
            {
                "name": "ARCADE_INIT",
                "text": "🕹️ *Retro Reels ULTRA*\n\n🎮 *ИНИЦИАЛИЗАЦИЯ АРКАДЫ...*\n\n",
                "frames": ["👾", "🤖", "🎯", "🔫"],
                "effects": ["pixel_art", "crt_effect"]
            },
            {
                "name": "8BIT_TURBO",
                "text": "🕹️ *Retro Reels ULTRA*\n\n🔥 *8-БИТНЫЙ ТУРБО-РЕЖИМ!*\n\n",
                "frames": ["🔴", "🟢", "🟡", "🔵"],
                "effects": ["color_cycle", "pixel_explosion"]
            },
            {
                "name": "PIXEL_PERFECTION",
                "text": "🕹️ *Retro Reels ULTRA*\n\n🎯 *ПИКСЕЛЬНОЕ СОВЕРШЕНСТВО...*\n\n",
                "frames": ["💎", "💠", "🔶", "🔷"],
                "effects": ["pixel_align", "crystal_effect"]
            },
            {
                "name": "HIGH_SCORE_SYNC",
                "text": "🕹️ *Retro Reels ULTRA*\n\n🏆 *СИНХРОНИЗАЦИЯ РЕКОРДОВ...*\n\n",
                "frames": ["📈", "⭐", "💯", "🎖️"],
                "effects": ["score_flash", "achievement_unlock"]
            },
            {
                "name": "LEGACY_REVEAL",
                "text": "🕹️ *Retro Reels ULTRA*\n\n🎊 *ЛЕГЕНДАРНОЕ ОТКРЫТИЕ!*\n\n",
                "frames": ["🎰", "💰", "🏅", "👑"],
                "effects": ["retro_celebration", "pixel_party"]
            }
        ]
    },
    "egypt": {
        "phases": [
            {
                "name": "PYRAMID_ENTRY",
                "text": "🐫 *Egypt Slots ULTRA*\n\n🏜️ *ВХОД В ПИРАМИДУ...*\n\n",
                "frames": ["🔐", "🚪", "🏛️", "🔺"],
                "effects": ["sand_effect", "hieroglyph_reveal"]
            },
            {
                "name": "TOMB_EXPLORATION",
                "text": "🐫 *Egypt Slots ULTRA*\n\n⚱️ *ИССЛЕДОВАНИЕ ГРОБНИЦЫ...*\n\n", 
                "frames": ["🗝️", "🔍", "💎", "🏺"],
                "effects": ["torch_light", "gold_glow"]
            },
            {
                "name": "PHARAOH_RITUAL",
                "text": "🐫 *Egypt Slots ULTRA*\n\n👑 *РИТУАЛ ФАРАОНА!*\n\n",
                "frames": ["🔥", "🌅", "🌄", "✨"],
                "effects": ["ritual_fire", "divine_light"]
            },
            {
                "name": "HIEROGLYPH_DECODE",
                "text": "🐫 *Egypt Slots ULTRA*\n\n📜 *РАСШИФРОВКА ИЕРОГЛИФОВ...*\n\n",
                "frames": ["🔤", "✍️", "📖", "🎭"],
                "effects": ["ancient_wisdom", "mystery_solve"]
            },
            {
                "name": "SANDSTORM_FINAL",
                "text": "🐫 *Egypt Slots ULTRA*\n\n🌪️ *ФИНАЛЬНАЯ ПЕСЧАНАЯ БУРЯ...*\n\n",
                "frames": ["💨", "🌪️", "🏜️", "🌅"],
                "effects": ["sandstorm", "treasure_reveal"]
            },
            {
                "name": "ROYAL_TREASURE",
                "text": "🐫 *Egypt Slots ULTRA*\n\n💎 *КОРОЛЕВСКОЕ СОКРОВИЩЕ!*\n\n",
                "frames": ["👑", "⚱️", "💎", "🏆"],
                "effects": ["gold_shower", "pharaoh_blessing"]
            }
        ]
    }
}

# ==================== SPECIAL EFFECTS CONFIG ====================
SPECIAL_EFFECTS = {
    "fruit": {
        "highlight": "🎯",
        "blink": ["💥", "✨", "🌟", "⭐"],
        "bonus_frames": ["💰", "💎", "🔔", "🍀"],
        "win_effects": ["fruit_shower", "juice_splash", "rainbow_fruits"]
    },
    "cosmic": {
        "highlight": "✨",
        "blink": ["🌠", "💫", "⭐", "🌟"], 
        "bonus_frames": ["👽", "🛸", "🪐", "🚀"],
        "win_effects": ["supernova", "black_hole", "galactic_explosion"]
    },
    "retro": {
        "highlight": "🔴",
        "blink": ["👾", "🕹️", "🎮", "💾"],
        "bonus_frames": ["🏆", "⭐", "💯", "🎖️"],
        "win_effects": ["pixel_storm", "high_score", "game_complete"]
    },
    "egypt": {
        "highlight": "💎",
        "blink": ["👑", "⚱️", "🔱", "🏺"],
        "bonus_frames": ["🐫", "🦂", "🌵", "📜"],
        "win_effects": ["gold_shower", "pyramid_light", "pharaoh_curse"]
    }
}

# ==================== WIN MULTIPLIERS ULTRA ====================
ULTRA_MULTIPLIERS = {
    "fruit": {
        "three_horizontal": 4,
        "three_vertical": 3,
        "diagonal": 7,
        "jackpot": 100,
        "special_symbol": 15,
        "fruit_bonus": 5,
        "rainbow_combo": 20
    },
    "cosmic": {
        "three_in_row": 6,
        "four_in_row": 15,
        "five_in_row": 40,
        "alien_bonus": 12,
        "planet_combo": 10,
        "cosmic_jackpot": 75,
        "galactic_bonus": 25
    },
    "retro": {
        "three_horizontal": 5,
        "three_vertical": 4,
        "diagonal": 9,
        "bonus_round": 20,
        "retro_combo": 8,
        "pixel_perfect": 15,
        "arcade_legend": 35
    },
    "egypt": {
        "four_horizontal": 9,
        "four_vertical": 8,
        "square": 7,
        "pharaoh_bonus": 25,
        "pyramid_combo": 12,
        "hieroglyph_bonus": 6,
        "royal_treasure": 50
    }
}

# ==================== GAME SYMBOLS ULTRA ====================
ULTRA_SYMBOLS = {
    "fruit": {
        "common": ["🍒", "🍋", "🍊", "🍇", "🍉"],
        "rare": ["🔔", "🍀", "💎", "⭐"],
        "epic": ["🌈", "🎯", "✨"],
        "legendary": ["👑", "🏆"]
    },
    "cosmic": {
        "common": ["🌙", "⭐", "🚀"],
        "rare": ["🛸", "🌍", "☄️"],
        "epic": ["👽", "🪐", "💫"],
        "legendary": ["🌌", "⚡", "🔭"]
    },
    "retro": {
        "common": ["🕹️", "👾", "💾"],
        "rare": ["📺", "🎮", "🔴"],
        "epic": ["🟢", "🟡", "🎰"],
        "legendary": ["🏆", "⭐", "👑"]
    },
    "egypt": {
        "common": ["🐫", "🦂", "🌵"],
        "rare": ["🏺", "🔱", "🪦"],
        "epic": ["📜", "💎", "⚱️"],
        "legendary": ["👑", "🔺", "🏛️"]
    }
}

# ==================== BET CONFIGURATION ====================
BET_OPTIONS = [10, 50, 100, 200, 500, 1000, 2000, 5000]
BET_QUICK_OPTIONS = [100, 500, 1000]

# ==================== DATABASE CONFIG ====================
DB_FILENAME = "users_data.json"
DB_BACKUP_INTERVAL = 1800  # 30 minutes
DB_ENCRYPTION = False

# ==================== ADMIN PANEL ULTRA ====================
ADMIN_LOG_ACTIONS = True
MAX_USERS_DISPLAY = 50
BROADCAST_DELAY = 0.08
ADMIN_COMMANDS = ["stats", "users", "balance", "broadcast", "maintenance"]

# ==================== GAME BALANCE ULTRA ====================
HOUSE_EDGE = 0.03  # 3% house edge
JACKPOT_CHANCE = 0.008  # 0.8% chance for jackpot
BONUS_ROUND_CHANCE = 0.12  # 12% chance for bonus round
EPIC_WIN_CHANCE = 0.005  # 0.5% chance for epic win

# ==================== PERFORMANCE ULTRA ====================
MAX_CONCURRENT_GAMES = 15
CACHE_USER_DATA = True
CACHE_TIMEOUT = 300
MEMORY_OPTIMIZATION = True
ASYNC_OPERATIONS = True

# ==================== LOGGING ULTRA ====================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "bot_ultra.log"
LOG_ROTATION = True
LOG_MAX_SIZE = "10MB"

# ==================== FEATURE FLAGS ULTRA ====================
ENABLE_DAILY_BONUS = True
ENABLE_ACHIEVEMENTS = True
ENABLE_LEADERBOARD = True
ENABLE_TOURNAMENTS = False  # Coming soon
ENABLE_GUILDS = False  # Coming soon
ENABLE_SEASONS = False  # Coming soon

# ==================== SECURITY ULTRA ====================
MAX_BET_PER_GAME = 10000
MAX_DAILY_LOSS = 50000
RATE_LIMIT_PER_USER = 15  # games per minute
ANTI_CHEAT_SYSTEM = True
SESSION_TIMEOUT = 3600  # 1 hour

# ==================== LOCALIZATION ULTRA ====================
LANGUAGE = "ru"
CURRENCY_SYMBOL = "🪙"
CURRENCY_NAME = "монет"
TIMEZONE = "Europe/Moscow"

# ==================== MAINTENANCE MODE ====================
MAINTENANCE_MODE = False
MAINTENANCE_MESSAGE = "🔧 Бот находится на техническом обслуживании. Пожалуйста, попробуйте позже."
MAINTENANCE_ETA = "2 часа"

# ==================== RULES SYSTEM ====================
SHOW_RULES_BEFORE_GAME = True
RULES_DISPLAY_TIME = 5
INTERACTIVE_RULES = True
RULES_QUIZ = False  # Coming soon

# ==================== ACHIEVEMENT SYSTEM ====================
ACHIEVEMENTS = {
    "first_win": {"name": "Первая победа", "reward": 100},
    "jackpot_king": {"name": "Король джекпотов", "reward": 500},
    "high_roller": {"name": "Высокий игрок", "reward": 300},
    "lucky_streak": {"name": "Счастливая серия", "reward": 200}
}

# ==================== SEASONAL EVENTS ====================
SEASONAL_EVENTS = {
    "new_year": {"active": False, "multiplier_bonus": 1.5},
    "valentines": {"active": False, "special_symbols": True},
    "halloween": {"active": False, "bonus_chance": 2.0}
}

# ==================== DEBUG & TESTING ====================
DEBUG_MODE = False
TEST_USER_IDS = [1015751543]
DEV_MODE = False
PERFORMANCE_MONITORING = True

print(f"🎰 ULTRA SLOTS BOT v{BOT_VERSION} - Configuration loaded!")
print(f"🚀 Ultra animations: {ULTRA_ANIMATION}")
print(f"🎯 Cinematic mode: {CINEMATIC_MODE}")
print(f"💫 Special effects: {len(SPECIAL_EFFECTS)} games enhanced")