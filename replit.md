# Overview

This is a Python XMPP/Jabber bot built with the slixmpp library that provides multi-user chat (MUC) functionality, automated greetings, hourly announcements, and an extensible command system. The bot is designed to connect to XMPP servers, join conference rooms, interact with users through commands, and perform scheduled tasks like time announcements.

# User Preferences

Preferred communication style: Simple, everyday language.
Language preference: Indonesian (user requested "buatkan jabberbot python" and features in Indonesian).

# System Architecture

## Core Components

The bot follows a modular architecture with clear separation of concerns:

**Main Bot Class (JabberBot)**: Extends slixmpp.ClientXMPP to handle XMPP protocol connections and core messaging functionality. This serves as the central coordinator that initializes and manages all other components.

**Command System**: Implemented through a dedicated CommandHandler class that provides an extensible framework for processing user commands. Commands are prefixed with '!' and include basic functionality like help, ping, time, status, and room management.

**Conference Management**: The ConferenceManager handles Multi-User Chat (MUC) operations including joining rooms, managing room-specific settings, and tracking user presence. This allows the bot to participate in group conversations and maintain context about different chat rooms.

**Task Scheduling**: A TaskScheduler component manages time-based operations like hourly announcements and other periodic tasks using Python's asyncio framework for non-blocking execution.

## Configuration Management

The system uses a dual configuration approach:
- INI configuration files for structured settings
- Environment variable fallbacks for sensitive data like credentials
- This design allows for easy deployment in different environments while maintaining security

## Asynchronous Architecture

The bot is built on Python's asyncio framework, allowing it to:
- Handle multiple concurrent connections and conversations
- Perform non-blocking I/O operations
- Execute scheduled tasks without interrupting message processing
- Maintain responsive real-time communication

## Logging and Error Handling

Comprehensive logging is implemented throughout all components with:
- File-based logging for persistence
- Console output for development
- Configurable log levels (debug/info)
- Structured error handling for network failures and reconnection

# External Dependencies

**slixmpp**: Core XMPP/Jabber protocol implementation providing connection management, message handling, and Multi-User Chat (MUC) support through XEP-0045.

**pytz**: Timezone handling for accurate time announcements and scheduling across different geographical locations.

**configparser**: Standard Python library for INI file configuration management.

**asyncio**: Built-in Python library for asynchronous programming and task scheduling.

The bot is designed to connect to any standard XMPP server and can be configured to join multiple conference rooms simultaneously. Authentication is handled through standard XMPP mechanisms with support for both password-based and other authentication methods supported by the underlying slixmpp library.