"""
Task scheduling module for the Jabber bot.
"""

import asyncio
import logging
from datetime import datetime, timedelta
import pytz


class TaskScheduler:
    """Handles scheduled tasks for the bot."""
    
    def __init__(self, bot):
        """Initialize task scheduler with bot instance."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        
        # Task management
        self.running = False
        self.tasks = []
        self.hourly_task = None
        
        # Configuration
        self.hourly_announcements = self.bot.config.getboolean(
            'scheduler', 'hourly_announcements', fallback=True
        )
        
    async def start(self):
        """Start the task scheduler."""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.logger.info("Starting task scheduler")
        
        # Start hourly announcements if enabled
        if self.hourly_announcements:
            self.hourly_task = asyncio.create_task(self._hourly_announcement_loop())
            self.hourly_task.add_done_callback(self._task_done_callback)
            self.tasks.append(self.hourly_task)
    
    async def stop(self):
        """Stop the task scheduler."""
        if not self.running:
            return
        
        self.running = False
        self.logger.info("Stopping task scheduler")
        
        # Cancel all running tasks
        for task in self.tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        self.tasks.clear()
        self.hourly_task = None
    
    async def _hourly_announcement_loop(self):
        """Main loop for hourly time announcements."""
        try:
            while self.running:
                # Calculate next hour boundary
                now = datetime.now(self.bot.timezone)
                next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                sleep_seconds = (next_hour - now).total_seconds()
                
                self.logger.debug(f"Sleeping {sleep_seconds:.1f} seconds until next hour")
                
                # Sleep until the next hour
                await asyncio.sleep(sleep_seconds)
                
                if self.running:
                    # Send hourly announcement
                    self._send_hourly_announcement()
                    
        except asyncio.CancelledError:
            self.logger.info("Hourly announcement task cancelled")
        except Exception as e:
            self.logger.error(f"Error in hourly announcement loop: {e}", exc_info=True)
    
    def _send_hourly_announcement(self):
        """Send hourly time announcement to all rooms."""
        try:
            now = datetime.now(self.bot.timezone)
            
            # Format time message
            time_str = now.strftime("%H:%M")
            day_str = now.strftime("%A")
            
            # Create announcement message
            message = f"🕐 {time_str} on {day_str}"
            
            # Add special messages for certain hours
            hour = now.hour
            if hour == 0:
                message += " - Midnight! 🌙"
            elif hour == 12:
                message += " - Noon! ☀️"
            elif hour == 18:
                message += " - Evening! 🌅"
            elif 6 <= hour < 12:
                message += " - Good morning! 🌄"
            elif 12 <= hour < 18:
                message += " - Good afternoon! ☀️"
            elif 18 <= hour < 22:
                message += " - Good evening! 🌆"
            elif hour >= 22 or hour < 6:
                message += " - Good night! 🌃"
            
            # Send to all connected rooms
            sent_count = 0
            for room_jid in self.bot.room_users.keys():
                try:
                    self.bot.send_message(mto=room_jid, mbody=message, mtype='groupchat')
                    sent_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to send hourly announcement to {room_jid}: {e}")
            
            self.logger.info(f"Sent hourly announcement to {sent_count} rooms: {message}")
            
        except Exception as e:
            self.logger.error(f"Error sending hourly announcement: {e}", exc_info=True)
    
    async def schedule_task(self, coro, delay_seconds):
        """Schedule a one-time task."""
        async def delayed_task():
            try:
                await asyncio.sleep(delay_seconds)
                await coro
            except Exception as e:
                self.logger.error(f"Scheduled task error: {e}", exc_info=True)
        
        task = asyncio.create_task(delayed_task())
        task.add_done_callback(self._task_done_callback)
        self.tasks.append(task)
        return task
    
    async def schedule_daily_task(self, coro, hour, minute=0):
        """Schedule a daily recurring task."""
        async def daily_task():
            try:
                while self.running:
                    now = datetime.now(self.bot.timezone)
                    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    
                    # If target time has passed today, schedule for tomorrow
                    if target_time <= now:
                        target_time += timedelta(days=1)
                    
                    sleep_seconds = (target_time - now).total_seconds()
                    await asyncio.sleep(sleep_seconds)
                    
                    if self.running:
                        try:
                            await coro
                        except Exception as e:
                            self.logger.error(f"Daily task execution error: {e}", exc_info=True)
            except asyncio.CancelledError:
                self.logger.info("Daily task cancelled")
            except Exception as e:
                self.logger.error(f"Daily task loop error: {e}", exc_info=True)
        
        task = asyncio.create_task(daily_task())
        task.add_done_callback(self._task_done_callback)
        self.tasks.append(task)
        return task
    
    def _task_done_callback(self, task):
        """Callback for when a task is done to handle exceptions."""
        try:
            task.result()
        except asyncio.CancelledError:
            self.logger.debug("Task was cancelled")
        except Exception as e:
            self.logger.error(f"Task exception: {e}", exc_info=True)
    
    def get_next_hourly_announcement(self):
        """Get the time of the next hourly announcement."""
        now = datetime.now(self.bot.timezone)
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        return next_hour
    
    def is_running(self):
        """Check if the scheduler is running."""
        return self.running
