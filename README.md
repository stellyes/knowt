# 📝 Personal Whiteboard App

A lightweight, storage-efficient whiteboard application for capturing notes, images, and links on-the-go. Built with Python and Streamlit for easy deployment and cross-device access.

## Features

### 📌 Entry Types
- **Notes** - Quick text entries with optional tags
- **Images** - Upload and store images with captions
- **Links** - Save URLs with automatic domain preview

### 🔍 Flexible Organization
- **Today View** - Default view showing today's entries
- **Date Range Filter** - View entries within custom date ranges
- **Tag-based Filtering** - Filter by one or multiple tags
- **Chronological Display** - Newest entries appear first

### 💾 Data Management
- **Automatic Saving** - All changes persist immediately
- **Backup/Restore** - Export and import your data as JSON
- **Storage Efficient** - Lightweight JSON format for minimal disk usage

## Installation

### Local Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

### Streamlit Cloud Deployment (Recommended for Multi-Device Access)

1. Push your code to a GitHub repository

2. Visit [share.streamlit.io](https://share.streamlit.io)

3. Connect your GitHub account

4. Select your repository and deploy

5. Access your whiteboard from any device using the provided URL

## Usage

### Adding Entries

Use the sidebar to add new entries:

1. Select entry type (Note, Image, or Link)
2. Fill in the content and optional tags
3. Click the "Add" button

**Tags:** Separate multiple tags with commas (e.g., `work, urgent, meeting`)

### Filtering Entries

Use the filter buttons at the top:

- **📅 Today** - View only today's entries (default)
- **📆 Date Range** - Select start and end dates
- **🏷️ Tags** - Filter by specific tags
- **🔄 All** - View all entries

### Managing Data

**Delete Entries:** Click the 🗑️ button next to any entry

**Backup Data:** 
1. Click "Download Backup" in the sidebar
2. Save the JSON file to your device

**Restore Data:**
1. Click "Choose file" under "Import Backup"
2. Select a previously exported JSON file

## File Structure

```
.
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── whiteboard_data.json     # Auto-generated data storage (created on first run)
```

## Data Storage

All entries are stored in `whiteboard_data.json` in the same directory as `app.py`. This file is automatically created on first use and updated with each change.

**Note:** When deploying to Streamlit Cloud, the data persists during your session but may be reset if the app restarts. Use the backup feature regularly or consider connecting to a database for production use.

## Tips

- **Organize with Tags**: Create a consistent tagging system (e.g., `work`, `personal`, `urgent`)
- **Regular Backups**: Download backups periodically, especially before major changes
- **Mobile Access**: Deploy to Streamlit Cloud and bookmark the URL for quick mobile access
- **Image Sizes**: Keep images reasonably sized for best performance (< 5MB recommended)

## Technical Details

- **Framework**: Streamlit
- **Storage Format**: JSON
- **Image Encoding**: Base64 (for portability)
- **Python Version**: 3.7+

## Troubleshooting

**App won't start:**
- Ensure Python 3.7+ is installed
- Verify streamlit is installed: `pip list | grep streamlit`

**Data not saving:**
- Check file permissions in the app directory
- Ensure `whiteboard_data.json` is not read-only

**Images not displaying:**
- Verify image file is a supported format (PNG, JPG, JPEG, GIF)
- Check image file size (very large images may have issues)

## Future Enhancements

Potential features for future versions:
- Entry editing capability
- Full-text search across all entries
- Multiple sort options (date, type, tags)
- Color-coded tags
- Entry categories
- Markdown support in notes
- Cloud storage integration

## License

Free to use and modify for personal or commercial purposes.

## Support

For issues or questions, please create an issue in the GitHub repository.
