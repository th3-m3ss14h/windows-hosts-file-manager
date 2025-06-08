#!/usr/bin/env python3
"""
Hosts File Manager - A comprehensive wizard for managing website blocking via hosts file
Requires administrator privileges to modify the hosts file.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import socket
from pathlib import Path
from datetime import datetime

class HostsManager:
    def __init__(self):
        self.hosts_path = Path("C:/Windows/System32/drivers/etc/hosts")
        self.blocked_sites = []  # Sites managed by this program
        self.all_blocked_sites = []  # All 0.0.0.0 entries in hosts file
        self.marker_start = "# === START HOSTS MANAGER ENTRIES ==="
        self.marker_end = "# === END HOSTS MANAGER ENTRIES ==="
        self.load_current_blocks()

    def is_admin(self):
        """Check if script is running with administrator privileges"""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()

    def load_current_blocks(self):
        """Load currently blocked sites from hosts file"""
        if not self.hosts_path.exists():
            print("Hosts file not found!")
            return

        try:
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            in_our_section = False
            
            for line in lines:
                line_stripped = line.strip()
                
                # Check if we're in our managed section
                if line_stripped == self.marker_start:
                    in_our_section = True
                    continue
                elif line_stripped == self.marker_end:
                    in_our_section = False
                    continue
                
                # Process 0.0.0.0 entries
                if line_stripped.startswith('0.0.0.0') and not line_stripped.startswith('#'):
                    parts = line_stripped.split()
                    if len(parts) >= 2:
                        site = parts[1]
                        
                        # Add to all blocked sites
                        if site not in self.all_blocked_sites:
                            self.all_blocked_sites.append(site)
                        
                        # Add to our managed sites if in our section
                        if in_our_section and site not in self.blocked_sites:
                            # Don't add www variants to our main list if base domain exists
                            if site.startswith('www.'):
                                base_site = site[4:]
                                if base_site not in self.blocked_sites:
                                    continue
                            self.blocked_sites.append(site)

        except Exception as e:
            print(f"Error reading hosts file: {e}")

    def add_site(self, site):
        """Add a site to the block list"""
        # Clean up the site input
        site = site.strip().lower()
        if site.startswith('http://') or site.startswith('https://'):
            site = site.split('://', 1)[1]
        if site.startswith('www.'):
            site = site[4:]
        if '/' in site:
            site = site.split('/')[0]

        # Validate domain
        if not self.is_valid_domain(site):
            print(f"Invalid domain format: {site}")
            return False

        if site not in self.blocked_sites:
            self.blocked_sites.append(site)
            print(f"✓ Added {site} to block list")
            return True
        else:
            print(f"⚠ {site} is already in the block list")
            return False

    def add_multiple_sites(self):
        """Add multiple sites at once"""
        print("\nEnter websites to block (one per line, empty line to finish):")
        print("Examples: facebook.com, www.youtube.com, https://twitter.com")
        print("Enter 'done' or empty line to finish")
        
        added_count = 0
        while True:
            site = input("Site: ").strip()
            if not site or site.lower() == 'done':
                break
            if self.add_site(site):
                added_count += 1
        
        print(f"\n✓ Added {added_count} new sites to block list")

    def remove_site(self, site):
        """Remove a site from the block list"""
        site = site.strip().lower()
        if site in self.blocked_sites:
            self.blocked_sites.remove(site)
            print(f"✓ Removed {site} from block list")
            return True
        else:
            print(f"⚠ {site} is not in the block list")
            return False

    def is_valid_domain(self, domain):
        """Basic domain validation"""
        if not domain or len(domain) > 253:
            return False
        if domain.startswith('.') or domain.endswith('.'):
            return False
        parts = domain.split('.')
        if len(parts) < 2:
            return False
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not all(c.isalnum() or c == '-' for c in part):
                return False
            if part.startswith('-') or part.endswith('-'):
                return False
        return True

    def list_blocked_sites(self, show_all=False):
        """Display blocked sites"""
        if show_all:
            if not self.all_blocked_sites:
                print("No sites are blocked in the hosts file.")
            else:
                print(f"\n📋 All blocked sites in hosts file ({len(self.all_blocked_sites)} total):")
                for i, site in enumerate(sorted(self.all_blocked_sites), 1):
                    managed_marker = " 🔧" if site in self.blocked_sites or site[4:] in self.blocked_sites else ""
                    print(f"{i:3d}. {site}{managed_marker}")
                print("\n🔧 = Managed by this program")
        else:
            if not self.blocked_sites:
                print("No sites are currently managed by this program.")
            else:
                print(f"\n📋 Sites managed by this program ({len(self.blocked_sites)} total):")
                for i, site in enumerate(sorted(self.blocked_sites), 1):
                    print(f"{i:3d}. {site}")

    def search_sites(self):
        """Search for sites in the block list"""
        search_term = input("Enter search term: ").strip().lower()
        if not search_term:
            return

        matches = [site for site in self.blocked_sites if search_term in site.lower()]
        all_matches = [site for site in self.all_blocked_sites if search_term in site.lower()]

        print(f"\n🔍 Search results for '{search_term}':")
        if matches:
            print(f"Managed sites ({len(matches)}):")
            for site in matches:
                print(f"  🔧 {site}")
        
        other_matches = [site for site in all_matches if site not in matches and site[4:] not in matches]
        if other_matches:
            print(f"Other blocked sites ({len(other_matches)}):")
            for site in other_matches:
                print(f"  📝 {site}")

    def test_site_blocking(self):
        """Test if a site is being blocked"""
        site = input("Enter site to test: ").strip()
        if not site:
            return

        # Clean up the site input
        if site.startswith('http://') or site.startswith('https://'):
            site = site.split('://', 1)[1]
        if '/' in site:
            site = site.split('/')[0]

        try:
            ip = socket.gethostbyname(site)
            if ip == "0.0.0.0":
                print(f"✅ {site} is blocked (resolves to 0.0.0.0)")
            else:
                print(f"❌ {site} is NOT blocked (resolves to {ip})")
        except socket.gaierror:
            print(f"❓ Cannot resolve {site} (may be blocked or invalid)")

    def flush_dns(self):
        """Flush DNS cache"""
        try:
            print("🔄 Flushing DNS cache...")
            result = subprocess.run(['ipconfig', '/flushdns'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("✅ DNS cache flushed successfully!")
            else:
                print(f"❌ Error flushing DNS: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running ipconfig: {e}")

    def update_hosts_file(self):
        """Update the hosts file with current block list"""
        if not self.is_admin():
            print("\n❌ Administrator privileges required to modify hosts file!")
            print("Please run this script as administrator.")
            return False

        try:
            # Read current hosts file
            original_content = []
            if self.hosts_path.exists():
                with open(self.hosts_path, 'r', encoding='utf-8') as f:
                    original_content = f.readlines()

            # Remove our existing section
            filtered_content = []
            in_our_section = False
            
            for line in original_content:
                line_stripped = line.strip()
                if line_stripped == self.marker_start:
                    in_our_section = True
                elif line_stripped == self.marker_end:
                    in_our_section = False
                    continue
                elif not in_our_section:
                    filtered_content.append(line)

            # Create new content with our blocks
            new_content = filtered_content
            
            if self.blocked_sites:
                # Ensure there's a newline before our section
                if new_content and not new_content[-1].endswith('\n'):
                    new_content.append('\n')
                
                new_content.append(f"\n{self.marker_start}\n")
                new_content.append(f"# Added by Hosts Manager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                for site in sorted(self.blocked_sites):
                    new_content.append(f"0.0.0.0 {site}\n")
                    # Also block www variant if not already a www site
                    if not site.startswith('www.'):
                        new_content.append(f"0.0.0.0 www.{site}\n")
                
                new_content.append(f"{self.marker_end}\n")

            # Write to temporary file first
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
                temp_file.writelines(new_content)
                temp_path = temp_file.name

            # Replace original file
            shutil.move(temp_path, str(self.hosts_path))
            print(f"\n✅ Hosts file updated successfully!")
            print(f"📊 {len(self.blocked_sites)} sites are now blocked")
            
            # Auto-flush DNS
            self.flush_dns()
            return True

        except Exception as e:
            print(f"❌ Error updating hosts file: {e}")
            return False

    def show_menu(self):
        """Display the main menu"""
        admin_status = "👑 ADMIN" if self.is_admin() else "⚠ USER"
        managed_count = len(self.blocked_sites)
        total_count = len(self.all_blocked_sites)
        
        print("\n" + "="*60)
        print("              🛡️  HOSTS FILE MANAGER  🛡️")
        print("="*60)
        print(f"Status: {admin_status} | Managed: {managed_count} | Total Blocked: {total_count}")
        print("-"*60)
        print(" 1. 📝 Add single site to block")
        print(" 2. 📝 Add multiple sites to block")
        print(" 3. 🗑️  Remove site from block list")
        print(" 4. 📋 List managed sites")
        print(" 5. 📋 List ALL blocked sites")
        print(" 6. 🔍 Search blocked sites")
        print(" 7. 🧪 Test if site is blocked")
        print(" 8. 💾 Update hosts file")
        print(" 9. 🔄 Flush DNS cache")
        print("10. 💾 Backup hosts file")
        print("11. 📊 Show hosts file stats")
        print("12. ❌ Exit")
        print("-"*60)

    def show_stats(self):
        """Show statistics about the hosts file"""
        try:
            stats = self.hosts_path.stat()
            file_size = stats.st_size
            mod_time = datetime.fromtimestamp(stats.st_mtime)
            
            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            empty_lines = sum(1 for line in lines if not line.strip())
            
            print(f"\n📊 Hosts File Statistics:")
            print(f"📍 Location: {self.hosts_path}")
            print(f"📏 File size: {file_size:,} bytes")
            print(f"🕐 Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📄 Total lines: {total_lines:,}")
            print(f"💬 Comment lines: {comment_lines:,}")
            print(f"📋 Empty lines: {empty_lines:,}")
            print(f"🚫 Total blocked sites: {len(self.all_blocked_sites):,}")
            print(f"🔧 Managed by this tool: {len(self.blocked_sites):,}")
            
        except Exception as e:
            print(f"❌ Error reading stats: {e}")

    def backup_hosts(self):
        """Create a backup of the current hosts file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.hosts_path.parent / f"hosts_backup_{timestamp}.txt"
            shutil.copy2(str(self.hosts_path), str(backup_path))
            print(f"✅ Hosts file backed up to: {backup_path}")
        except Exception as e:
            print(f"❌ Error creating backup: {e}")

    def run(self):
        """Main program loop"""
        print("🛡️ Hosts File Manager - Website Blocking Tool")
        print("This tool helps you block websites by modifying your hosts file.")
        
        if not self.is_admin():
            print("\n⚠️  WARNING: Not running as administrator!")
            print("You can manage your block list, but updating the hosts file requires admin rights.")

        while True:
            self.show_menu()
            
            try:
                choice = input("\n💬 Enter your choice (1-12): ").strip()
                
                if choice == '1':
                    site = input("🌐 Enter website to block (e.g., example.com): ").strip()
                    if site:
                        self.add_site(site)
                    else:
                        print("❌ Please enter a valid website.")
                
                elif choice == '2':
                    self.add_multiple_sites()
                
                elif choice == '3':
                    self.list_blocked_sites()
                    if self.blocked_sites:
                        site = input("\n🗑️ Enter website to unblock: ").strip()
                        if site:
                            self.remove_site(site)
                
                elif choice == '4':
                    self.list_blocked_sites(show_all=False)
                
                elif choice == '5':
                    self.list_blocked_sites(show_all=True)
                
                elif choice == '6':
                    self.search_sites()
                
                elif choice == '7':
                    self.test_site_blocking()
                
                elif choice == '8':
                    if self.blocked_sites:
                        print(f"\n📝 This will update your hosts file with {len(self.blocked_sites)} blocked sites.")
                        confirm = input("Continue? (y/N): ").lower()
                        if confirm == 'y':
                            self.update_hosts_file()
                    else:
                        print("❌ No sites in block list to update.")
                
                elif choice == '9':
                    self.flush_dns()
                
                elif choice == '10':
                    self.backup_hosts()
                
                elif choice == '11':
                    self.show_stats()
                
                elif choice == '12':
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-12.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    manager = HostsManager()
    manager.run()
