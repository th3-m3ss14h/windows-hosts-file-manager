# 🛡️ Hosts File Manager

A comprehensive Python-based wizard for managing website blocking via the Windows hosts file. Perfect for parental controls, productivity enhancement, or blocking unwanted content.

## ✨ Features

### 🎯 **Smart Website Blocking**
- Block websites by redirecting them to `0.0.0.0`
- Automatically blocks both `example.com` and `www.example.com`
- Handles various URL formats (with/without protocols, paths, etc.)
- Domain validation to prevent invalid entries

### 🔧 **Intelligent Management**
- **Dual View System**: Distinguish between sites managed by this tool vs. existing entries
- **Safe Operation**: Uses comment markers to avoid interfering with other hosts file entries
- **Bulk Operations**: Add multiple sites at once
- **Search & Filter**: Find specific blocked sites quickly

### 🚀 **Quality of Life Features**
- **Automatic DNS Flushing**: Changes take effect immediately
- **Site Testing**: Verify if a website is actually blocked
- **File Statistics**: Detailed info about your hosts file
- **Timestamped Backups**: Never lose your configuration
- **Visual Interface**: Emojis and clear status indicators

### 🔒 **Safety & Reliability**
- Administrator privilege detection
- Temporary file operations prevent corruption
- Comprehensive error handling
- Non-destructive editing (preserves existing entries)

## 📋 Requirements

- **Windows 10/11** (targets Windows hosts file location)
- **Python 3.6+**
- **Administrator privileges** (required to modify hosts file)

## 🚀 Installation & Usage

### Quick Start
1. **Download** the `hosts_manager.py` script
2. **Right-click Command Prompt** → "Run as administrator"
3. **Navigate** to the script location
4. **Run**: `python hosts_manager.py`

### Step-by-Step Guide

```bash
# 1. Open Command Prompt as Administrator
# Right-click Start button → "Terminal (Admin)" or "Command Prompt (Admin)"

# 2. Navigate to your script location
cd C:\path\to\your\script

# 3. Run the script
python hosts_manager.py
```

## 🎮 Menu Options

| Option | Feature | Description |
|--------|---------|-------------|
| 1 | 📝 Add Single Site | Add one website to block list |
| 2 | 📝 Add Multiple Sites | Bulk add multiple websites |
| 3 | 🗑️ Remove Site | Remove website from block list |
| 4 | 📋 List Managed Sites | Show sites managed by this tool |
| 5 | 📋 List ALL Sites | Show all blocked sites in hosts file |
| 6 | 🔍 Search Sites | Search through blocked sites |
| 7 | 🧪 Test Site | Check if a site is actually blocked |
| 8 | 💾 Update Hosts File | Apply changes to hosts file |
| 9 | 🔄 Flush DNS | Clear DNS cache manually |
| 10 | 💾 Backup Hosts | Create timestamped backup |
| 11 | 📊 Show Stats | Display hosts file statistics |
| 12 | ❌ Exit | Close the program |

## 💡 Usage Examples

### Adding Sites
The tool accepts various URL formats:
```
✅ example.com
✅ www.example.com  
✅ https://example.com
✅ http://www.example.com/path
✅ facebook.com
```

### Bulk Adding
Use Option 2 to add multiple sites:
```
Site: facebook.com
Site: twitter.com  
Site: youtube.com
Site: done
```

### Testing Blocks
Use Option 7 to verify blocking:
```
Enter site to test: facebook.com
✅ facebook.com is blocked (resolves to 0.0.0.0)
```

## 🔧 How It Works

### File Structure
The tool adds a clearly marked section to your hosts file:
```
# === START HOSTS MANAGER ENTRIES ===
# Added by Hosts Manager on 2025-06-08 14:30:15
0.0.0.0 facebook.com
0.0.0.0 www.facebook.com
0.0.0.0 youtube.com
0.0.0.0 www.youtube.com
# === END HOSTS MANAGER ENTRIES ===
```

### Safety Mechanisms
- **Non-destructive**: Preserves existing hosts file entries
- **Marked sections**: Clear boundaries prevent conflicts
- **Temporary files**: Atomic operations prevent corruption
- **Automatic backups**: Create backups before major changes

## ⚠️ Important Notes

### Administrator Rights
- **Required** for modifying the hosts file
- **Warning displayed** if not running as admin
- You can still manage your block list without admin rights

### DNS Cache
- Changes may not take effect immediately
- Tool automatically flushes DNS cache after updates
- Manual flush available via Option 9: `ipconfig /flushdns`

### File Location
- Targets: `C:\Windows\System32\drivers\etc\hosts`
- Creates backups in the same directory
- Backup format: `hosts_backup_YYYYMMDD_HHMMSS.txt`

## 🐛 Troubleshooting

### Common Issues

**"Access Denied" Error**
```
❌ Administrator privileges required to modify hosts file!
```
**Solution**: Run Command Prompt as Administrator

**Sites Still Loading**
```
❌ site.com is NOT blocked (resolves to X.X.X.X)  
```
**Solutions**:
1. Use Option 9 to flush DNS cache
2. Clear browser cache
3. Restart browser
4. Check if site is actually in the list (Option 4)

**Script Won't Start**
```
'python' is not recognized...
```
**Solution**: Install Python from [python.org](https://python.org) or use `py` instead of `python`

### Verification Steps
1. **Check Admin Status**: Look for 👑 ADMIN in the menu header
2. **Verify Entries**: Use Option 4 to list managed sites
3. **Test Blocking**: Use Option 7 to test specific sites
4. **Check File**: Use Option 11 for hosts file statistics

## 🤝 Best Practices

### Recommended Workflow
1. **Start with backup** (Option 10)
2. **Add sites to list** (Options 1-2)
3. **Review your list** (Option 4)
4. **Update hosts file** (Option 8)
5. **Test blocking** (Option 7)

### Maintenance
- **Regular backups** before major changes
- **Periodic cleanup** of unused entries
- **Test blocking** after system updates
- **Review statistics** to monitor file health

## 📁 File Structure

```
your-project/
├── hosts_manager.py          # Main script
├── README.md                 # This documentation
└── backups/                  # Backup files (created automatically)
    ├── hosts_backup_20250608_143015.txt
    └── hosts_backup_20250608_150230.txt
```

## 🔄 Version History

### Current Version
- **Enhanced Interface**: Emoji indicators and status display
- **Dual Management**: Separate tracking of managed vs. all entries
- **Advanced Features**: Search, test, bulk operations
- **Auto-QoL**: Automatic DNS flushing and validation
- **Safety First**: Non-destructive editing with clear markers

## 📜 License

This project is provided as-is for educational and personal use. Use responsibly and ensure you have proper authorization to modify system files.

## ⚠️ Disclaimer

This tool modifies system files and requires administrator privileges. Always:
- **Create backups** before making changes
- **Test thoroughly** in a safe environment first  
- **Understand the implications** of blocking websites
- **Use responsibly** and respect others' access needs

---

**Made with ❤️ for better internet control and productivity**
