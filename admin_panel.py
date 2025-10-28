from database import Database
from config import ADMIN_IDS

class AdminPanel:
    def __init__(self):
        self.db = Database()
    
    def is_admin(self, user_id: int) -> bool:
        return user_id in ADMIN_IDS
    
    def get_bot_stats(self) -> str:
        stats = self.db.get_total_stats()
        users_data = self.db.get_all_users()
        
        # Рассчитываем дополнительную статистику
        active_users = sum(1 for user in users_data.values() if user.get('games_played', 0) > 0)
        total_profit = stats['total_bets'] - sum(user.get('balance', 0) for user in users_data.values())
        
        stats_text = "👑 *Статистика бота*\n\n"
        stats_text += f"👥 Всего пользователей: {stats['total_users']}\n"
        stats_text += f"🎯 Активных пользователей: {active_users}\n"
        stats_text += f"💰 Общий баланс: {stats['total_balance']} монет\n"
        stats_text += f"🎰 Всего ставок: {stats['total_bets']}\n"
        stats_text += f"🏆 Всего выигрышей: {stats['total_wins']}\n"
        stats_text += f"💵 Прибыль казино: {total_profit} монет\n"
        
        # Топ пользователей по балансу
        top_users = sorted(users_data.items(), key=lambda x: x[1].get('balance', 0), reverse=True)[:3]
        stats_text += "\n🏅 *Топ пользователей:*\n"
        for i, (user_id, data) in enumerate(top_users, 1):
            stats_text += f"{i}. ID {user_id}: {data.get('balance', 0)} монет\n"
        
        return stats_text
    
    def get_users_list(self) -> str:
        users_data = self.db.get_all_users()
        
        if not users_data:
            return "📝 Пользователей пока нет"
        
        users_text = "👥 *Список пользователей*\n\n"
        for user_id, data in list(users_data.items())[:30]:  # Ограничиваем вывод
            balance = data.get('balance', 0)
            games_played = data.get('games_played', 0)
            last_activity = data.get('last_activity', 'Неизвестно')
            
            users_text += f"🆔 ID: {user_id}\n"
            users_text += f"💰 Баланс: {balance} монет\n"
            users_text += f"🎮 Игр сыграно: {games_played}\n"
            users_text += f"🕐 Активность: {last_activity[:16] if len(last_activity) > 16 else last_activity}\n"
            users_text += "─" * 25 + "\n"
        
        if len(users_data) > 30:
            users_text += f"\n... и еще {len(users_data) - 30} пользователей"
        
        return users_text
    
    def update_user_balance(self, user_id: int, amount: int) -> bool:
        try:
            user_data = self.db.get_user(user_id)
            old_balance = user_data["balance"]
            user_data["balance"] += amount
            self.db.update_user(user_id, user_data)
            
            # Логируем изменение баланса
            print(f"Админ изменил баланс пользователя {user_id}: {old_balance} -> {user_data['balance']} (изменение: {amount})")
            
            return True
        except Exception as e:
            print(f"Ошибка при изменении баланса: {e}")
            return False
    
    def get_user_details(self, user_id: int) -> str:
        try:
            user_data = self.db.get_user(user_id)
            
            details = f"👤 *Детали пользователя {user_id}*\n\n"
            details += f"💰 Баланс: {user_data.get('balance', 0)} монет\n"
            details += f"🎮 Сыграно игр: {user_data.get('games_played', 0)}\n"
            details += f"📈 Всего ставок: {user_data.get('total_bets', 0)}\n"
            details += f"🏆 Выигрышей: {user_data.get('total_wins', 0)}\n"
            
            wins = user_data.get('total_wins', 0)
            bets = user_data.get('total_bets', 0)
            win_rate = (wins / bets * 100) if bets > 0 else 0
            details += f"📊 Процент выигрышей: {win_rate:.1f}%\n"
            
            details += f"📅 Регистрация: {user_data.get('registration_date', 'Неизвестно')}\n"
            details += f"🕐 Последняя активность: {user_data.get('last_activity', 'Неизвестно')}\n"
            
            return details
        except Exception as e:
            return f"❌ Ошибка при получении данных пользователя: {e}"