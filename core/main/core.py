# Main module that runs continuously and acts like an API for the terminal.py
from EventNotifier import EventNotifier
# Import observer modules
# from system_monitor import SystemMonitor
# from security_checker import SecurityChecker
# ... (import other observer modules here)

class Core:
    def __init__(self):
        self.event_notifier = EventNotifier()

        # Initialize and register observer modules
        # self.system_monitor = SystemMonitor()
        # self.event_notifier.register_observer(self.system_monitor)

        # self.security_checker = SecurityChecker()
        # self.event_notifier.register_observer(self.security_checker)

        # ... (initialize and register other modules)

    def start(self):
        """Start the EventNotifier and the core process."""
        try:
            self.event_notifier.start()
        except KeyboardInterrupt:
            print("Shutting down ErgoMonitor...")
            # Probably will have to change how this "shutting down" works later,
            # as this is the core and not the terminal
        finally:
            # Perform any cleanup here before the application closes
            pass

def main():
    core = Core()
    core.start()

if __name__ == "__main__":
    main()
