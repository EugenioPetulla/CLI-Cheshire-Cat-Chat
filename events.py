"""Events."""

import elements
import json
from inputhread import UserInputThread


class Events:
    """WS events."""

    def __init__(self, spinner, console):
        self.spinner = spinner
        self.console = console

    def on_message(self, ws, message):
        """Stop the spinner and print the cat's response."""
        self.spinner.stop()
        self.spinner.clear()

        user_thread = UserInputThread(ws, self.console, self.spinner)
        cat_response = json.loads(message)
        if cat_response["error"]:
            self.on_error(ws, "Connection issues")
            return
        user_thread.update_console(cat_response["content"])

        # Start the user input thread to ask for new input from the user
        user_thread.start()

    def on_error(self, ws, error):
        """Check errors."""
        # Check if the error message contains the string "WebSocketApp' object has no attribute 'pong'"
        if "WebSocketApp' object has no attribute 'pong'" in str(error):
            return
        # Otherwise, print the error message
        self.console.print(elements._error(error))

    def on_ping(self, ws, ping_data):
        """Send a pong response."""
        ws.pong()

    def on_open(self, ws):
        """Open and request user input."""
        # Send a full welcome message when connected
        self.console.print(elements._greetings(), justify="center")

        # Request user input to start the conversation
        user_thread = UserInputThread(ws, self.console, self.spinner)
        user_thread.start()

    def on_close(self, ws, close_status_code, close_msg):
        """Close session."""
        ws.close()
