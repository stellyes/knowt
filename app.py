import streamlit as st
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse
import base64
from pathlib import Path
import os

# Configure page
st.set_page_config(
    page_title="Knowt",
    page_icon="📝",
    layout="wide"
)

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = []
if 'filter_mode' not in st.session_state:
    st.session_state.filter_mode = 'today'
if 'selected_tags' not in st.session_state:
    st.session_state.selected_tags = []
if 'date_range' not in st.session_state:
    st.session_state.date_range = None

# Storage file path
STORAGE_FILE = 'whiteboard_data.json'

def load_data():
    """Load entries from JSON file"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                data = json.load(f)
                st.session_state.entries = data.get('entries', [])
        except Exception as e:
            st.error(f"Error loading data: {e}")

def save_data():
    """Save entries to JSON file"""
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump({'entries': st.session_state.entries}, f)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def add_entry(entry_type, content, tags=None, image_data=None, link=None):
    """Add a new entry"""
    entry = {
        'id': len(st.session_state.entries),
        'timestamp': datetime.now().isoformat(),
        'type': entry_type,
        'content': content,
        'tags': tags or [],
        'image_data': image_data,
        'link': link
    }
    st.session_state.entries.insert(0, entry)
    save_data()

def delete_entry(entry_id):
    """Delete an entry"""
    st.session_state.entries = [e for e in st.session_state.entries if e['id'] != entry_id]
    save_data()

def get_all_tags():
    """Get all unique tags from entries"""
    tags = set()
    for entry in st.session_state.entries:
        tags.update(entry.get('tags', []))
    return sorted(list(tags))

def filter_entries():
    """Filter entries based on current filter settings"""
    filtered = st.session_state.entries
    
    if st.session_state.filter_mode == 'today':
        today = datetime.now().date()
        filtered = [e for e in filtered if datetime.fromisoformat(e['timestamp']).date() == today]
    
    elif st.session_state.filter_mode == 'date_range' and st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        filtered = [e for e in filtered if start_date <= datetime.fromisoformat(e['timestamp']).date() <= end_date]
    
    elif st.session_state.filter_mode == 'tags' and st.session_state.selected_tags:
        filtered = [e for e in filtered if any(tag in e.get('tags', []) for tag in st.session_state.selected_tags)]
    
    return filtered

def get_link_preview(url):
    """Generate a simple link preview"""
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    return f"🔗 {domain}"

def render_entry(entry):
    """Render a single entry"""
    with st.container():
        col1, col2 = st.columns([6, 1])
        
        with col1:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            st.caption(f"📅 {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if entry['type'] == 'note':
                st.markdown(f"**Note:** {entry['content']}")
            
            elif entry['type'] == 'image':
                if entry.get('content'):
                    st.markdown(f"**Caption:** {entry['content']}")
                if entry.get('image_data'):
                    try:
                        image_bytes = base64.b64decode(entry['image_data'])
                        st.image(image_bytes, width=400)
                    except:
                        st.error("Error displaying image")
            
            elif entry['type'] == 'link':
                st.markdown(f"**{entry['content']}**")
                link_url = entry.get('link', '')
                if link_url:
                    st.markdown(f"{get_link_preview(link_url)}")
                    st.markdown(f"[Open Link]({link_url})")
            
            if entry.get('tags'):
                tags_str = ' '.join([f'`{tag}`' for tag in entry['tags']])
                st.markdown(f"Tags: {tags_str}")
        
        with col2:
            if st.button("🗑️", key=f"delete_{entry['id']}"):
                delete_entry(entry['id'])
                st.rerun()
        
        st.divider()

# Load data on startup
load_data()

# Header
st.title("Knowt™")
st.markdown("Your portable note-taking and organization hub")

# Sidebar for adding entries
with st.sidebar:
    st.header("➕ Add New Entry")
    
    entry_type = st.selectbox(
        "Entry Type",
        ["Note", "Image", "Link"],
        key="entry_type_select"
    )
    
    if entry_type == "Note":
        note_content = st.text_area("Note Content", height=100)
        note_tags = st.text_input("Tags (comma-separated)", key="note_tags")
        
        if st.button("Add Note", type="primary"):
            if note_content:
                tags = [tag.strip() for tag in note_tags.split(',') if tag.strip()]
                add_entry('note', note_content, tags=tags)
                st.success("Note added!")
                st.rerun()
            else:
                st.error("Please enter note content")
    
    elif entry_type == "Image":
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif'])
        image_caption = st.text_input("Caption (optional)")
        image_tags = st.text_input("Tags (comma-separated)", key="image_tags")
        
        if st.button("Add Image", type="primary"):
            if uploaded_file:
                image_bytes = uploaded_file.read()
                image_b64 = base64.b64encode(image_bytes).decode()
                tags = [tag.strip() for tag in image_tags.split(',') if tag.strip()]
                add_entry('image', image_caption, tags=tags, image_data=image_b64)
                st.success("Image added!")
                st.rerun()
            else:
                st.error("Please upload an image")
    
    elif entry_type == "Link":
        link_url = st.text_input("URL")
        link_title = st.text_input("Link Title")
        link_tags = st.text_input("Tags (comma-separated)", key="link_tags")
        
        if st.button("Add Link", type="primary"):
            if link_url and link_title:
                tags = [tag.strip() for tag in link_tags.split(',') if tag.strip()]
                add_entry('link', link_title, tags=tags, link=link_url)
                st.success("Link added!")
                st.rerun()
            else:
                st.error("Please enter URL and title")
    
    st.divider()
    
    # Export/Import functionality
    st.header("💾 Data Management")
    
    if st.button("Download Backup"):
        if st.session_state.entries:
            json_data = json.dumps({'entries': st.session_state.entries}, indent=2)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_data,
                file_name=f"whiteboard_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No entries to export")
    
    uploaded_backup = st.file_uploader("Import Backup", type=['json'])
    if uploaded_backup:
        try:
            data = json.load(uploaded_backup)
            st.session_state.entries = data.get('entries', [])
            save_data()
            st.success("Data imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing data: {e}")

# Main content area - Filters
st.header("🔍 Filter Entries")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Today", use_container_width=True):
        st.session_state.filter_mode = 'today'
        st.rerun()

with col2:
    if st.button("📆 Date Range", use_container_width=True):
        st.session_state.filter_mode = 'date_range'

with col3:
    if st.button("🏷️ Tags", use_container_width=True):
        st.session_state.filter_mode = 'tags'

with col4:
    if st.button("🔄 All", use_container_width=True):
        st.session_state.filter_mode = 'all'
        st.rerun()

# Additional filter controls
if st.session_state.filter_mode == 'date_range':
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.now().date())
    st.session_state.date_range = (start_date, end_date)

elif st.session_state.filter_mode == 'tags':
    all_tags = get_all_tags()
    if all_tags:
        st.session_state.selected_tags = st.multiselect("Select Tags", all_tags)
    else:
        st.info("No tags available yet")

st.divider()

# Display entries
st.header("📋 Entries")

filtered_entries = filter_entries()

if filtered_entries:
    st.markdown(f"*Showing {len(filtered_entries)} entries*")
    for entry in filtered_entries:
        render_entry(entry)
else:
    st.info("No entries found. Add your first entry using the sidebar!")

# Footer
st.divider()
st.caption(f"Total entries: {len(st.session_state.entries)} | Storage-efficient JSON format")
