"""
Command handling module for the Jabber bot.
"""

import logging
from datetime import datetime
import platform
import sys


class CommandHandler:
    """Handles bot commands and responses."""
    
    def __init__(self, bot):
        """Initialize command handler with bot instance."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        
        # Define available commands
        self.commands = {
            'help': self._cmd_help,
            'ping': self._cmd_ping,
            'time': self._cmd_time,
            'status': self._cmd_status,
            'rooms': self._cmd_rooms,
            'users': self._cmd_users,
            'about': self._cmd_about,
        }
    
    async def handle_command(self, msg):
        """Handle incoming command messages."""
        try:
            # Parse command and arguments
            body = msg['body'].strip()
            if not body.startswith('!'):
                return
            
            parts = body[1:].split()
            if not parts:
                return
                
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            self.logger.info(f"Processing command: {command} with args: {args}")
            
            # Execute command if it exists
            if command in self.commands:
                response = await self.commands[command](msg, args)
                if response:
                    msg.reply(response).send()
            else:
                response = f"Unknown command: {command}. Type !help for available commands."
                msg.reply(response).send()
                
        except Exception as e:
            self.logger.error(f"Error handling command: {e}", exc_info=True)
            error_msg = "Sorry, there was an error processing your command."
            msg.reply(error_msg).send()
    
    async def _cmd_help(self, msg, args):
        """Show available commands."""
        help_text = """Available commands:
!help - Show this help message
!ping - Check if bot is responsive
!time - Show current time
!status - Show bot status
!rooms - List connected rooms (group chat only)
!users <room> - List users in a room (group chat only)
!about - Show bot information"""
        
        return help_text
    
    async def _cmd_ping(self, msg, args):
        """Simple ping command."""
        return "Pong! 🏓"
    
    async def _cmd_time(self, msg, args):
        """Show current time."""
        now = datetime.now(self.bot.timezone)
        time_str = now.strftime("%A, %B %d, %Y at %H:%M:%S %Z")
        return f"Current time: {time_str}"
    
    async def _cmd_status(self, msg, args):
        """Show bot status information."""
        connected_rooms = len(self.bot.get_connected_rooms())
        total_users = sum(len(users) for users in self.bot.room_users.values())
        
        status = f"""Bot Status:
• Connected: ✅ Yes
• Nickname: {self.bot.nick}
• Joined rooms: {connected_rooms}
• Total tracked users: {total_users}
• Timezone: {self.bot.timezone}
• Python version: {sys.version.split()[0]}"""
        
        return status
    
    async def _cmd_rooms(self, msg, args):
        """List connected rooms (group chat only)."""
        if msg['type'] != 'groupchat':
            return "This command is only available in group chats."
        
        rooms = self.bot.get_connected_rooms()
        if not rooms:
            return "No rooms currently connected."
        
        room_list = "\n".join(f"• {room}" for room in rooms)
        return f"Connected rooms:\n{room_list}"
    
    async def _cmd_users(self, msg, args):
        """List users in a room."""
        if msg['type'] != 'groupchat':
            return "This command is only available in group chats."
        
        # If no room specified, use current room
        if not args:
            room = msg['from'].bare
        else:
            room = args[0]
        
        users = self.bot.get_room_users(room)
        if not users:
            return f"No users found in room: {room}"
        
        user_list = "\n".join(f"• {user}" for user in sorted(users))
        return f"Users in {room}:\n{user_list}"
    
    async def _cmd_about(self, msg, args):
        """Show bot information."""
        about_text = f"""🤖 Jabber Bot Information:
• Name: {self.bot.nick}
• Version: 1.0.0
• Platform: {platform.system()} {platform.release()}
• Python: {sys.version.split()[0]}
• Features: Conference greetings, hourly announcements, command handling
• Repository: https://github.com/kucenk/jabberpy"""
        
        return about_text
