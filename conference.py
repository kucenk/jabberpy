"""
Conference/MUC (Multi-User Chat) management for the Jabber bot.
"""

import logging
from datetime import datetime


class ConferenceManager:
    """Manages conference room operations and user interactions."""
    
    def __init__(self, bot):
        """Initialize conference manager with bot instance."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        
        # Store room-specific settings
        self.room_settings = {}
        
    def configure_room(self, room_jid, **settings):
        """Configure settings for a specific room."""
        if room_jid not in self.room_settings:
            self.room_settings[room_jid] = {}
        
        self.room_settings[room_jid].update(settings)
        self.logger.info(f"Updated settings for room {room_jid}: {settings}")
    
    def get_room_setting(self, room_jid, setting, default=None):
        """Get a setting for a specific room."""
        return self.room_settings.get(room_jid, {}).get(setting, default)
    
    async def join_room(self, room_jid, nick=None, password=None):
        """Join a conference room."""
        if nick is None:
            nick = self.bot.nick
            
        try:
            self.bot.plugin['xep_0045'].join_muc(
                room_jid, 
                nick, 
                password=password
            )
            
            # Initialize room tracking
            if room_jid not in self.bot.room_users:
                self.bot.room_users[room_jid] = set()
            
            self.logger.info(f"Successfully joined room: {room_jid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to join room {room_jid}: {e}")
            return False
    
    async def leave_room(self, room_jid, reason="Goodbye!"):
        """Leave a conference room."""
        try:
            self.bot.plugin['xep_0045'].leave_muc(room_jid, self.bot.nick, reason)
            
            # Clean up room tracking
            if room_jid in self.bot.room_users:
                del self.bot.room_users[room_jid]
            
            if room_jid in self.room_settings:
                del self.room_settings[room_jid]
            
            self.logger.info(f"Left room: {room_jid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to leave room {room_jid}: {e}")
            return False
    
    def send_room_message(self, room_jid, message):
        """Send a message to a conference room."""
        try:
            self.bot.send_message(mto=room_jid, mbody=message, mtype='groupchat')
            self.logger.debug(f"Sent message to {room_jid}: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message to {room_jid}: {e}")
            return False
    
    def broadcast_message(self, message, exclude_rooms=None):
        """Broadcast a message to all connected rooms."""
        if exclude_rooms is None:
            exclude_rooms = []
        
        sent_count = 0
        for room_jid in self.bot.room_users.keys():
            if room_jid not in exclude_rooms:
                if self.send_room_message(room_jid, message):
                    sent_count += 1
        
        self.logger.info(f"Broadcast message sent to {sent_count} rooms")
        return sent_count
    
    def get_room_info(self, room_jid):
        """Get information about a room."""
        try:
            # Get room configuration
            config_form = self.bot.plugin['xep_0045'].get_room_config(room_jid)
            
            info = {
                'jid': room_jid,
                'users': list(self.bot.room_users.get(room_jid, [])),
                'user_count': len(self.bot.room_users.get(room_jid, [])),
                'settings': self.room_settings.get(room_jid, {}),
                'bot_nick': self.bot.nick
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get room info for {room_jid}: {e}")
            return None
    
    def is_user_in_room(self, room_jid, nick):
        """Check if a user is in a specific room."""
        return nick in self.bot.room_users.get(room_jid, set())
    
    def get_user_rooms(self, nick):
        """Get all rooms where a specific user is present."""
        user_rooms = []
        for room_jid, users in self.bot.room_users.items():
            if nick in users:
                user_rooms.append(room_jid)
        return user_rooms
    
    def create_room_report(self):
        """Create a summary report of all rooms and users."""
        report_lines = ["📊 Conference Room Report", "=" * 30]
        
        if not self.bot.room_users:
            report_lines.append("No rooms currently connected.")
            return "\n".join(report_lines)
        
        total_users = 0
        for room_jid, users in self.bot.room_users.items():
            user_count = len(users)
            total_users += user_count
            
            report_lines.append(f"\n🏠 Room: {room_jid}")
            report_lines.append(f"   Users: {user_count}")
            
            if users:
                user_list = ", ".join(sorted(users))
                if len(user_list) > 80:
                    user_list = user_list[:77] + "..."
                report_lines.append(f"   Members: {user_list}")
        
        report_lines.append(f"\n📈 Total: {len(self.bot.room_users)} rooms, {total_users} users")
        report_lines.append(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report_lines)
