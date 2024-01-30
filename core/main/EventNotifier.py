# It's a module by itself for communication between the modules.
class EventNotifier:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        """ Register an observer to receive notifications. """
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """ Unregister an observer from receiving notifications. """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event):
        """ Notify all registered observers of an event. """
        for observer in self._observers:
            observer.update(event)

    def start(self):
        """ Start the event monitoring and notification process. """
        print("Event Notifier started. Monitoring for events...") # will have to send it to logger.py on later configuration
        try:
            # The event detection and notification loop, using tools from /utils
            news = 0
            while True:
                # Here there's the logic to check for events.
                # This could involve calling utility functions from the utils/
                # directory or directly implementing event detection logic.
                # We'll have to use AsyncIO or other to check in different periods
                # of time on different utils/ changes. Ideally every code here is just
                # calls and notifies. No selfcode at all.

                # Example event detection logic:
                # event = self.detect_event()
                # if event:
                #     self.notify_observers(event)

                # Placeholder for a delay to prevent tight looping
                import time
                time.sleep(2)
                print(f"{news} News.")

        except KeyboardInterrupt:
            # Handle any cleanup or resource release here before exiting
            print("Event Notifier shutting down...")

    def detect_event(self):
        """ 
        Detect events that need to be notified to observers.
        This method should contain the logic for detecting events.
        """
        # Implement event detection logic by arguments to detect_event here
        # Return an event object or None if no event detected
        pass

if __name__ == "__main__":
    # For testing purposes
    notifier = EventNotifier()
    notifier.start()
