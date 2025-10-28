import time
from datetime import datetime

def format_user_stats(user_data: dict) -> str:
    stats_text = "📊 *Ваша статистика*\n\n"
    stats_text += f"💰 Баланс: {user_data.get('balance', 0)} монет\n"
    stats_text += f"🎰 Сыграно игр: {user_data.get('games_played', 0)}\n"
    stats_text += f"📈 Всего ставок: {user_data.get('total_bets', 0)}\n"
    stats_text += f"🏆 Выигрышей: {user_data.get('total_wins', 0)}\n"
    
    wins = user_data.get('total_wins', 0)
    bets = user_data.get('total_bets', 0)
    win_rate = (wins / bets * 100) if bets > 0 else 0
    stats_text += f"📊 Процент выигрышей: {win_rate:.1f}%\n"
    
    return stats_text

def update_user_activity(db, user_id: int):
    user_data = db.get_user(user_id)
    user_data["last_activity"] = datetime.now().isoformat()
    if not user_data.get("registration_date"):
        user_data["registration_date"] = datetime.now().isoformat()
    db.update_user(user_id, user_data)