"""
Main Jabber/XMPP bot implementation using slixmpp.
"""

import logging
import configparser
import asyncio
import os
from datetime import datetime
import pytz

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

from commands import CommandHandler
from conference import ConferenceManager
from scheduler import TaskScheduler


class JabberBot(slixmpp.ClientXMPP):
    """
    Main Jabber bot class that handles XMPP connections and message processing.
    """
    
    def __init__(self, config_file='config.ini'):
        """Initialize the Jabber bot with configuration."""
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_file)
        
        # Get credentials from config or environment
        jid = self.config.get('bot', 'jid', fallback=os.getenv('XMPP_JID', 'bot@example.com'))
        password = self.config.get('bot', 'password', fallback=os.getenv('XMPP_PASSWORD', 'password'))
        
        super().__init__(jid, password)
        
        # Register required plugins
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0045')  # Multi-User Chat
        self.register_plugin('xep_0199')  # XMPP Ping
        
        # Initialize components
        self.command_handler = CommandHandler(self)
        self.conference_manager = ConferenceManager(self)
        self.scheduler = TaskScheduler(self)
        
        # Bot configuration
        self.nick = self.config.get('bot', 'nickname', fallback='JabberBot')
        self.timezone = pytz.timezone(self.config.get('bot', 'timezone', fallback='UTC'))
        self.greeting_message = self.config.get('messages', 'greeting', 
                                              fallback='Hello {nick}! Welcome to the conference!')
        
        # Conference rooms to join
        self.auto_join_rooms = self._parse_rooms()
        
        # Set up event handlers
        self._setup_event_handlers()
        
        # Track connected users per room
        self.room_users = {}
        
    def _load_config(self, config_file):
        """Load configuration from file."""
        config = configparser.ConfigParser()
        try:
            config.read(config_file)
            self.logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            self.logger.warning(f"Could not load config file {config_file}: {e}")
        return config
    
    def _parse_rooms(self):
        """Parse auto-join rooms from configuration."""
        rooms_str = self.config.get('bot', 'auto_join_rooms', fallback='')
        if not rooms_str:
            return []
        
        rooms = []
        for room in rooms_str.split(','):
            room = room.strip()
            if room:
                rooms.append(room)
        return rooms
    
    def _setup_event_handlers(self):
        """Set up XMPP event handlers."""
        self.add_event_handler('session_start', self._session_start)
        self.add_event_handler('message', self._message_received)
        self.add_event_handler('groupchat_message', self._groupchat_message)
        self.add_event_handler('muc::*::got_online', self._muc_user_joined)
        self.add_event_handler('muc::*::got_offline', self._muc_user_left)
        self.add_event_handler('disconnected', self._disconnected)
        
    async def _session_start(self, event):
        """Handle session start event."""
        self.logger.info("Bot session started")
        
        # Send initial presence
        self.send_presence()
        await self.get_roster()
        
        # Join auto-join rooms
        for room in self.auto_join_rooms:
            await self._join_room(room)
            
        # Start the task scheduler
        await self.scheduler.start()
        
    async def _join_room(self, room_jid):
        """Join a conference room."""
        try:
            self.plugin['xep_0045'].join_muc(room_jid, self.nick)
            self.logger.info(f"Joined room: {room_jid}")
            self.room_users[room_jid] = set()
        except Exception as e:
            self.logger.error(f"Failed to join room {room_jid}: {e}")
    
    async def _message_received(self, msg):
        """Handle private messages."""
        if msg['type'] in ('chat', 'normal'):
            self.logger.info(f"Private message from {msg['from']}: {msg['body']}")
            
            # Handle commands in private messages
            if msg['body'].startswith('!'):
                await self.command_handler.handle_command(msg)
            else:
                # Simple echo response for non-command messages
                reply = f"You said: {msg['body']}"
                msg.reply(reply).send()
    
    async def _groupchat_message(self, msg):
        """Handle group chat messages."""
        # Ignore messages from the bot itself
        if msg['mucnick'] == self.nick:
            return
            
        self.logger.debug(f"Group message in {msg['from'].bare}: <{msg['mucnick']}> {msg['body']}")
        
        # Handle commands in group chat
        if msg['body'].startswith('!'):
            await self.command_handler.handle_command(msg)
    
    async def _muc_user_joined(self, presence):
        """Handle user joining a conference room."""
        room = presence['from'].bare
        nick = presence['from'].resource
        
        # Skip if it's the bot itself
        if nick == self.nick:
            return
            
        self.logger.info(f"User {nick} joined room {room}")
        
        # Track user in room
        if room not in self.room_users:
            self.room_users[room] = set()
        
        # Check if this is a new user (not just a presence update)
        if nick not in self.room_users[room]:
            self.room_users[room].add(nick)
            
            # Send greeting message
            greeting = self.greeting_message.format(nick=nick, room=room)
            self.send_message(mto=room, mbody=greeting, mtype='groupchat')
            self.logger.info(f"Sent greeting to {nick} in {room}")
    
    async def _muc_user_left(self, presence):
        """Handle user leaving a conference room."""
        room = presence['from'].bare
        nick = presence['from'].resource
        
        if nick == self.nick:
            return
            
        self.logger.info(f"User {nick} left room {room}")
        
        # Remove user from tracking
        if room in self.room_users and nick in self.room_users[room]:
            self.room_users[room].remove(nick)
    
    async def _disconnected(self, event):
        """Handle disconnection event."""
        self.logger.warning("Bot disconnected from server")
        
        # Stop scheduler
        await self.scheduler.stop()
        
        # Attempt to reconnect after a delay
        await asyncio.sleep(5)
        self.logger.info("Attempting to reconnect...")
        if not self.connect():
            self.logger.error("Failed to reconnect")
    
    def send_hourly_announcement(self):
        """Send hourly time announcements to all joined rooms."""
        now = datetime.now(self.timezone)
        time_str = now.strftime("%H:%M %Z")
        message = f"🕐 Current time: {time_str}"
        
        for room in self.room_users.keys():
            try:
                self.send_message(mto=room, mbody=message, mtype='groupchat')
                self.logger.debug(f"Sent hourly announcement to {room}")
            except Exception as e:
                self.logger.error(f"Failed to send hourly announcement to {room}: {e}")
    
    def get_connected_rooms(self):
        """Get list of currently connected rooms."""
        return list(self.room_users.keys())
    
    def get_room_users(self, room):
        """Get list of users in a specific room."""
        return list(self.room_users.get(room, []))
