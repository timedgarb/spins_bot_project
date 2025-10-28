import json
import os
from typing import Dict, Any

class Database:
    def __init__(self, filename: str = "users_data.json"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _read_data(self) -> Dict[str, Any]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_data(self, data: Dict[str, Any]):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        data = self._read_data()
        user_data = data.get(str(user_id), {})
        
        # Если пользователь новый, создаем запись
        if not user_data:
            user_data = {
                "balance": 1000,
                "total_bets": 0,
                "total_wins": 0,
                "games_played": 0,
                "registration_date": None,
                "last_activity": None
            }
            self.update_user(user_id, user_data)
        
        return user_data
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]):
        data = self._read_data()
        data[str(user_id)] = user_data
        self._write_data(data)
    
    def update_balance(self, user_id: int, amount: int):
        user_data = self.get_user(user_id)
        user_data["balance"] += amount
        self.update_user(user_id, user_data)
    
    def get_all_users(self) -> Dict[str, Any]:
        return self._read_data()
    
    def get_total_stats(self) -> Dict[str, Any]:
        data = self._read_data()
        total_users = len(data)
        total_balance = sum(user.get("balance", 0) for user in data.values())
        total_bets = sum(user.get("total_bets", 0) for user in data.values())
        total_wins = sum(user.get("total_wins", 0) for user in data.values())
        
        return {
            "total_users": total_users,
            "total_balance": total_balance,
            "total_bets": total_bets,
            "total_wins": total_wins
        }