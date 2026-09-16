import json
import os

class SettingsManager:
    """
    Manages application settings with persistence to a JSON file.
    
    This class handles loading, saving, and providing access to user preferences
    such as appearance mode, UI scaling, and notification settings. It automatically
    creates a default settings file if one doesn't exist.
    """
    def __init__(self, file_path="settings.json"):
        """
        Initialize the SettingsManager with a settings file.
        
        Args:
            file_path (str): Path to the JSON file where settings will be stored.
                            Defaults to 'settings.json' in the current directory.
        """
        self.file_path = file_path
        # Load settings from file or use defaults if file doesn't exist
        self.settings = self._load_settings()

    def _load_settings(self):
        """
        Load settings from the settings file.
        
        If the file doesn't exist or is corrupted, returns default settings.
        
        Returns:
            dict: Loaded settings or default settings if loading fails
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings from {self.file_path}: {e}")
                print("Using default settings instead.")
                return self._get_default_settings()
        return self._get_default_settings()

    def _get_default_settings(self):
        """
        Get the default application settings.
        
        These settings are used when no settings file exists or when the file is corrupted.
        
        Returns:
            dict: Dictionary containing default settings
        """
        return {
            "appearance_mode": "System",  # Can be 'Light', 'Dark', or 'System'
            "ui_scaling": "100%",        # UI scaling percentage as a string
            "notifications_enabled": True  # Whether to show desktop notifications
        }

    def get_setting(self, key):
        """
        Retrieve a setting value by its key.
        
        Args:
            key (str): The setting key to retrieve
            
        Returns:
            The setting value, or None if the key doesn't exist
        """
        return self.settings.get(key)

    def set_setting(self, key, value):
        """
        Update a setting and save it to disk.
        
        Args:
            key (str): The setting key to update
            value: The new value for the setting
            
        Note:
            This will immediately persist the change to the settings file.
        """
        self.settings[key] = value
        self.save_settings()

    def save_settings(self):
        """
        Save the current settings to the settings file.
        
        Creates the settings directory if it doesn't exist. If saving fails,
        an error message will be printed to stderr.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
            
            # Write settings to file with pretty-printing
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
                
        except (IOError, OSError) as e:
            print(f"Error: Failed to save settings to {self.file_path}: {e}", file=sys.stderr)
