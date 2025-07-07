# Oink Macro - Auto Clicker

A powerful and user-friendly auto-clicker application built with Python and CustomTkinter for macOS.

## Features

- **Flexible Click Intervals**: Set specific time intervals or random intervals
- **Multiple Click Types**: Single click or double click support
- **Mouse Button Options**: Left, middle, or right mouse button
- **Position Control**: Follow mouse cursor or set fixed coordinates
- **Repeat Options**: Finite number of clicks or infinite until stopped
- **Hotkey Support**: Set custom hotkeys to start/stop clicking
- **Modern UI**: Clean, intuitive interface with custom theming

## Screenshots

*[Add screenshots of your application here]*

## Installation

### Prerequisites
- macOS 10.14 or later
- Python 3.11+ (for development)

### Download and Install

1. **Download the latest release** from the [Releases](https://github.com/yourusername/oink-macro/releases) page
2. **Extract the DMG file** (double-click to mount)
3. **Drag the app to Applications** folder
4. **Grant Accessibility permissions**:
   - Go to System Settings > Privacy & Security > Accessibility
   - Add "Oink Macro" and check the box
5. **Run the app** from Applications folder

## Usage

### Basic Setup

1. **Set Click Interval**:
   - Choose "Specified Interval" for fixed timing
   - Or choose "Random Interval" for variable timing
   - Set hours, minutes, seconds, and milliseconds

2. **Choose Click Position**:
   - "Follow Mouse": Clicks wherever your cursor is
   - "Fixed Position": Set specific X,Y coordinates
   - Use "Pick" button to select coordinates visually

3. **Configure Click Options**:
   - Select mouse button (Left, Middle, Right)
   - Choose click type (Single Click, Double Click)

4. **Set Repeat Options**:
   - "Repeat": Set number of times to click
   - "Infinite": Click until manually stopped

5. **Start Clicking**:
   - Click "Start" to begin auto-clicking
   - Use "Stop" to halt the process
   - Set a hotkey for quick start/stop

### Advanced Features

- **Hotkey Support**: Set custom keyboard shortcuts
- **Coordinate Picker**: Click "Pick" to visually select screen coordinates
- **Random Intervals**: Set minimum and maximum seconds for random timing

## Development

### Building from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/oink-macro.git
   cd oink-macro
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python GUI.py
   ```

### Building Distribution

To create a distributable `.app` bundle:

```bash
pyinstaller --name "Oink Macro" --windowed \
  --icon "assets/OinkMacro.icns" \
  --add-data "assets:assets" \
  --add-data "themes:themes" \
  --add-data "macro.py:." \
  GUI.py
```

## Requirements

- **Python 3.11+**
- **CustomTkinter**: Modern UI framework
- **PyAutoGUI**: Cross-platform GUI automation
- **Pynput**: Keyboard and mouse monitoring
- **PIL/Pillow**: Image processing

## File Structure

```
Oink Macro/
├── GUI.py              # Main application
├── macro.py            # Auto-clicker logic
├── assets/             # Images and icons
├── themes/             # UI theme files
├── venv/               # Virtual environment
└── dist/               # Built application
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **CustomTkinter** for the modern UI framework
- **PyAutoGUI** for cross-platform automation
- **Pynput** for keyboard and mouse monitoring

### Icon Credits

All icons used in this application are from [Icons8](https://icons8.com):

- **Session Timeout** icon for time interval functionality
- **Location Off** icon for position selection
- **Select Cursor** icon for mouse options
- **Synchronize** icon for repeat functionality

Thank you to Icons8 for providing these high-quality icons under their free license.

## Support

If you encounter any issues:

1. Check that Accessibility permissions are granted
2. Ensure the app is in the Applications folder
3. Try running from Terminal for error messages
4. Open an issue on GitHub with details

## Disclaimer

This tool is intended for legitimate automation tasks. Users are responsible for complying with applicable laws and terms of service when using this software.

---

**Made with ❤️ for macOS automation** 