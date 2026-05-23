"""
Scheduler Module - Schedule bot tasks and farming hours
"""

import logging
from datetime import datetime, time, timedelta
from typing import Optional, List, Callable
from enum import Enum
import threading
import time as time_module

logger = logging.getLogger(__name__)


class ScheduleType(Enum):
    """Types of scheduled tasks"""
    ATTACK = "attack"
    FARM = "farm"
    COLLECT = "collect"
    TRAINING = "training"
    MAINTENANCE = "maintenance"


class ScheduledTask:
    """Represents a scheduled task"""
    
    def __init__(self, name: str, task_type: ScheduleType, callback: Callable, 
                 schedule_time: str = None, repeat_interval: int = None):
        self.name = name
        self.task_type = task_type
        self.callback = callback
        self.schedule_time = schedule_time
        self.repeat_interval = repeat_interval
        self.enabled = True
        self.last_run = None
        self.next_run = None
        self.execution_count = 0
    
    def execute(self):
        """Execute the task"""
        try:
            logger.info(f"Executing task: {self.name}")
            self.callback()
            self.last_run = datetime.now()
            self.execution_count += 1
            logger.info(f"Task completed: {self.name}")
            
        except Exception as e:
            logger.error(f"Task execution error ({self.name}): {e}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "type": self.task_type.value,
            "schedule_time": self.schedule_time,
            "repeat_interval": self.repeat_interval,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "execution_count": self.execution_count
        }


class SimpleScheduler:
    """Simple task scheduler"""
    
    def __init__(self):
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self.scheduler_thread = None
    
    def add_task(self, task: ScheduledTask) -> bool:
        """Add scheduled task"""
        try:
            self.tasks.append(task)
            logger.info(f"Task added: {task.name}")
            return True
            
        except Exception as e:
            logger.error(f"Task add error: {e}")
            return False
    
    def remove_task(self, name: str) -> bool:
        """Remove scheduled task"""
        try:
            for i, task in enumerate(self.tasks):
                if task.name == name:
                    self.tasks.pop(i)
                    logger.info(f"Task removed: {name}")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Task removal error: {e}")
            return False
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Run scheduler loop"""
        while self.running:
            for task in self.tasks:
                if task.enabled:
                    self._check_and_execute(task)
            time_module.sleep(10)  # Check every 10 seconds
    
    def _check_and_execute(self, task: ScheduledTask):
        """Check if task should execute"""
        try:
            now = datetime.now()
            
            if task.repeat_interval:
                if task.last_run is None:
                    task.execute()
                elif (now - task.last_run).total_seconds() >= task.repeat_interval * 60:
                    task.execute()
            
            elif task.schedule_time:
                parts = task.schedule_time.split(":")
                if len(parts) == 2:
                    hour, minute = int(parts[0]), int(parts[1])
                    if now.hour == hour and now.minute == minute:
                        if task.last_run is None or (now - task.last_run).total_seconds() > 60:
                            task.execute()
        
        except Exception as e:
            logger.error(f"Task check error: {e}")
    
    def get_tasks(self) -> List[dict]:
        """Get all tasks"""
        return [task.to_dict() for task in self.tasks]


class FarmingScheduler:
    """Specialized scheduler for farming mode"""
    
    def __init__(self):
        self.farming_hours = {}  # day -> (start_hour, end_hour)
        self.is_farming_time = False
    
    def set_farming_hours(self, day: str, start_hour: int, end_hour: int):
        """Set farming hours for a specific day"""
        if 0 <= start_hour < 24 and 0 <= end_hour < 24:
            self.farming_hours[day.lower()] = (start_hour, end_hour)
            logger.info(f"Farming hours set for {day}: {start_hour:02d}:00 - {end_hour:02d}:00")
    
    def set_farming_hours_all_days(self, start_hour: int, end_hour: int):
        """Set same farming hours for all days"""
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in days:
            self.set_farming_hours(day, start_hour, end_hour)
    
    def is_farming_time_now(self) -> bool:
        """Check if current time is farming time"""
        try:
            now = datetime.now()
            day_name = now.strftime("%A").lower()
            current_hour = now.hour
            
            if day_name not in self.farming_hours:
                return False
            
            start_hour, end_hour = self.farming_hours[day_name]
            
            if start_hour <= end_hour:
                is_farming = start_hour <= current_hour < end_hour
            else:
                is_farming = current_hour >= start_hour or current_hour < end_hour
            
            self.is_farming_time = is_farming
            logger.debug(f"Farming time check: {is_farming}")
            return is_farming
            
        except Exception as e:
            logger.error(f"Farming time check error: {e}")
            return False
    
    def get_next_farming_time(self) -> Optional[datetime]:
        """Get next farming time"""
        try:
            now = datetime.now()
            current_day_index = now.weekday()
            
            # Check today
            day_name = now.strftime("%A").lower()
            if day_name in self.farming_hours:
                start_hour, _ = self.farming_hours[day_name]
                farming_time_today = now.replace(hour=start_hour, minute=0, second=0)
                
                if farming_time_today > now:
                    return farming_time_today
            
            # Check next days
            for i in range(1, 8):
                next_day_index = (current_day_index + i) % 7
                days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                next_day_name = days[next_day_index]
                
                if next_day_name in self.farming_hours:
                    start_hour, _ = self.farming_hours[next_day_name]
                    next_farming_time = now + timedelta(days=i)
                    next_farming_time = next_farming_time.replace(hour=start_hour, minute=0, second=0)
                    return next_farming_time
            
            return None
            
        except Exception as e:
            logger.error(f"Next farming time error: {e}")
            return None
