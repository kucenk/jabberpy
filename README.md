# Python Jabber/XMPP Bot

A feature-rich Python XMPP bot that supports multi-user chat (MUC) conferences, automatic greetings, hourly time announcements, and extensible command handling.

## Features

- **XMPP/Jabber Connection**: Connects to any XMPP server with robust error handling
- **Multi-User Chat Support**: Joins and manages conference rooms
- **Greeting System**: Automatically greets new users joining conferences
- **Hourly Announcements**: Sends time announcements every hour to all connected rooms
- **Command System**: Extensible command handling with built-in commands
- **Configuration Management**: Easy configuration via INI file or environment variables
- **Logging**: Comprehensive logging for debugging and monitoring
- **Reconnection**: Automatic reconnection on connection loss

## Installation

### Prerequisites

Install the required Python packages:
```bash
pip install slixmpp configparser pytz
```

### Quick Start

1. **Edit Configuration**: Copy and modify `config.ini` with your XMPP credentials:
   ```ini
   [bot]
   jid = your_bot@your_server.com
   password = your_password
   nickname = MyBot
   auto_join_rooms = room1@conference.server.com,room2@conference.server.com
   ```

2. **Run the Bot**:
   ```bash
   python main.py --debug
   ```

3. **Using Environment Variables** (optional):
   ```bash
   export XMPP_JID="your_bot@your_server.com"
   export XMPP_PASSWORD="your_password"
   python main.py
   ```

## Core Features

### 1. **Automatic Greetings**
Bot automatically welcomes new users joining conference rooms:
- Detects when someone joins a room
- Sends personalized greeting message
- Configurable greeting text in `config.ini`

### 2. **Hourly Time Announcements**
Bot sends time updates every hour to all connected rooms:
- Shows current time with timezone
- Includes special messages for different times of day
- Can be enabled/disabled in configuration

### 3. **Command System**
Bot responds to commands prefixed with `!`:

#### Available Commands:
- `!help` - Show available commands
- `!ping` - Check bot responsiveness
- `!time` - Show current time
- `!status` - Display bot status and statistics
- `!rooms` - List connected conference rooms
- `!users [room]` - Show users in a room
- `!about` - Bot information

#### Example Usage:
```
User: !time
Bot: Current time: Saturday, August 10, 2025 at 14:30:15 UTC

User: !status
Bot: Bot Status:
• Connected: ✅ Yes
• Nickname: JabberBot
• Joined rooms: 2
• Total tracked users: 8
• Timezone: UTC
```

### 4. **Multi-Room Support**
- Automatically joins configured rooms on startup
- Tracks users in each room separately
- Supports room-specific settings
- Handles room join/leave events

## Configuration

The bot uses `config.ini` for configuration with the following sections:

### [bot] Section
```ini
[bot]
jid = bot@example.com              # Bot's XMPP ID
password = your_password_here      # Bot's password
nickname = JabberBot              # Nickname in conferences
timezone = UTC                    # Timezone for announcements
auto_join_rooms = room1@conf.server.com,room2@conf.server.com
```

### [messages] Section
```ini
[messages]
greeting = Hello {nick}! Welcome to the conference! 👋
```

### [scheduler] Section
```ini
[scheduler]
hourly_announcements = true       # Enable/disable hourly time announcements
```

## Usage Examples

### Starting the Bot
```bash
# With debug logging
python main.py --debug

# With custom config file
python main.py --config my_config.ini

# Show help
python main.py --help
```

### Interacting with the Bot
In any conference room where the bot is present:

```
# Check if bot is working
!ping

# Get current time
!time

# See bot status
!status

# List all connected rooms
!rooms

# See who's in current room
!users

# See who's in specific room
!users room@conference.server.com
```

## Features in Detail

### Greeting System
- Monitors user presence in conference rooms
- Sends welcome message when new users join
- Tracks users to avoid duplicate greetings
- Configurable greeting message with nickname placeholder

### Time Announcements
- Automatic hourly announcements at the top of each hour
- Time-specific greetings (Good morning, afternoon, etc.)
- Special messages for midnight, noon, and evening
- Timezone-aware time display

### Error Handling & Reconnection
- Automatic reconnection on connection loss
- Comprehensive error logging
- Graceful handling of network issues
- Configurable retry mechanisms

## Logging

The bot provides detailed logging:
- File logging to `jabberbot.log`
- Console output for real-time monitoring
- Debug mode for troubleshooting
- Structured log messages with timestamps

## Architecture

The bot follows a modular design:
- **JabberBot**: Main bot class handling XMPP connections
- **CommandHandler**: Processes user commands
- **ConferenceManager**: Manages room operations
- **TaskScheduler**: Handles time-based tasks
- **Configuration**: INI-based configuration management
