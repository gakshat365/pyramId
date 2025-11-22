import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# IMPORT CONFIGURATION
try:
    import db_config
except ImportError:
    print("[!] Error: 'db_config.py' not found.")
    sys.exit(1)

# ==============================================================================
# DATABASE CONNECTIVITY
# ==============================================================================
def get_db_connection():
    """Establishes a secure connection to the VoughDB"""
    config = {
        'host': db_config.DB_HOST,
        'user': db_config.DB_USER,
        'password': db_config.DB_PASSWORD,
        'database': db_config.DB_NAME
    }
    
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Connection failed: {e}")
        return None

def execute_query(sql, params=None):
    """Execute a query and return results"""
    conn = get_db_connection()
    if not conn:
        return None, None
    
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        results = cursor.fetchall()
        return columns, results
    except Error as e:
        messagebox.showerror("Query Error", f"Error: {e}")
        return None, None
    finally:
        cursor.close()
        conn.close()

def execute_update(sql, params=None):
    """Execute an UPDATE/INSERT/DELETE query"""
    conn = get_db_connection()
    if not conn:
        return False, "Connection failed"
    
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        rows_affected = cursor.rowcount
        return True, f"Success! {rows_affected} row(s) affected."
    except Error as e:
        conn.rollback()
        return False, f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def execute_sql_file(file_path):
    """Execute all SQL statements from a file"""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    config = {
        'host': db_config.DB_HOST,
        'user': db_config.DB_USER,
        'password': db_config.DB_PASSWORD,
    }
    
    conn = None
    cursor = None
    
    try:
        # Connect without specifying database for schema.sql
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Read and execute the SQL file
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        for statement in statements:
            try:
                cursor.execute(statement)
                # Fetch results if any (for SELECT statements)
                if cursor.description:
                    cursor.fetchall()
            except Error as stmt_error:
                # Skip empty or comment-only statements
                if statement and not statement.startswith('--'):
                    raise stmt_error
        
        conn.commit()
        return True, f"Successfully executed {file_path}"
    except Error as e:
        if conn:
            conn.rollback()
        return False, f"Error executing {file_path}: {e}"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Unexpected error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==============================================================================
# QUERY DEFINITIONS - All Parameterized
# ==============================================================================

QUERIES = {
    "Retrieval - Selection": {
        "Members by Tier & Time Period": """
            SELECT 
                m.participant_id as Member_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Member_Name,
                m.tier_level as Tier,
                m.total_recruits as Total_Recruits,
                m.join_date as Join_Date,
                u.universe_name as Universe
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE m.tier_level = %s 
            AND m.join_date BETWEEN %s AND %s
            ORDER BY m.join_date DESC;
        """
    },
    
    "Retrieval - Projection": {
        "Active Participant Names & Contacts": """
            SELECT 
                p.participant_id as ID,
                CONCAT(p.first_name, ' ', p.last_name) as Full_Name,
                p.date_of_birth as DOB,
                u.universe_name as Universe,
                p.planet as Planet,
                p.country as Country
            FROM Participant p
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE p.participant_id IN (
                SELECT participant_id FROM Member WHERE status = 'active'
            )
            ORDER BY p.last_name, p.first_name;
        """
    },
    
    "Retrieval - Aggregate SUM": {
        "Total Revenue by Tier & Year": """
            SELECT 
                SUM(t.amount) as Total_Revenue,
                COUNT(t.transaction_id) as Transaction_Count
            FROM Transaction t
            JOIN Member m ON t.from_member_id = m.participant_id
            WHERE m.tier_level = %s
            AND YEAR(t.transaction_date) = %s
            AND t.transaction_type = 'investment'
            AND t.status = 'completed';
        """
    },
    
    "Retrieval - Aggregate MAX": {
        "Highest Revenue Member by Tier & Period": """
            SELECT 
                m.participant_id as Member_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Member_Name,
                m.tier_level as Tier,
                SUM(t.amount) as Total_Revenue
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Transaction t ON m.participant_id = t.from_member_id
            WHERE m.tier_level = %s
            AND t.transaction_date BETWEEN %s AND %s
            AND t.status = 'completed'
            GROUP BY m.participant_id
            ORDER BY Total_Revenue DESC
            LIMIT 1;
        """
    },
    
    "Retrieval - Aggregate MIN": {
        "Lowest Revenue Member by Tier & Period": """
            SELECT 
                m.participant_id as Member_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Member_Name,
                m.tier_level as Tier,
                SUM(t.amount) as Total_Revenue
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Transaction t ON m.participant_id = t.from_member_id
            WHERE m.tier_level = %s
            AND t.transaction_date BETWEEN %s AND %s
            AND t.status = 'completed'
            GROUP BY m.participant_id
            ORDER BY Total_Revenue ASC
            LIMIT 1;
        """
    },
    
    "Retrieval - Time Range": {
        "Members Recruited in Time Range": """
            SELECT 
                re.recruit_id as Recruited_Member_ID,
                CONCAT(p1.first_name, ' ', p1.last_name) as Recruited_Member_Name,
                m.tier_level as Tier,
                re.recruitment_date as Recruitment_Date,
                re.recruiter_id as Recruiter_ID,
                CONCAT(p2.first_name, ' ', p2.last_name) as Recruiter_Name,
                re.recruitment_method as Method
            FROM RecruitmentEvent re
            JOIN Member m ON re.recruit_id = m.participant_id
            JOIN Participant p1 ON re.recruit_id = p1.participant_id
            LEFT JOIN Participant p2 ON re.recruiter_id = p2.participant_id
            WHERE re.recruitment_date BETWEEN %s AND %s
            ORDER BY re.recruitment_date DESC;
        """
    },
    
    "Retrieval - Search": {
        "Search Participants by Name": """
            SELECT 
                p.participant_id as ID,
                CONCAT(p.first_name, ' ', p.last_name) as Full_Name,
                p.date_of_birth as DOB,
                u.universe_name as Universe,
                p.country as Country
            FROM Participant p
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE CONCAT(p.first_name, ' ', p.last_name) LIKE CONCAT('%%', %s, '%%')
            ORDER BY p.last_name, p.first_name;
        """
    },
    
    "Retrieval - View Tables": {
        "View All Members": """
            SELECT 
                m.participant_id as Member_ID,
                m.tier_level as Tier,
                m.total_recruits as Total_Recruits,
                m.join_date as Join_Date,
                m.status as Status
            FROM Member m
            ORDER BY m.tier_level, m.join_date;
        """,
        "View Orphaned Members": """
            SELECT 
                m.participant_id as Orphaned_Member_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Member_Name,
                m.tier_level as Tier,
                m.join_date as Join_Date,
                m.status as Status,
                u.universe_name as Universe
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE m.recruiter_id IS NULL
            AND m.tier_level > 1
            ORDER BY m.join_date;
        """,
        "View All Recruitment Events": """
            SELECT 
                re.recruit_id as Recruited_Member_ID,
                CONCAT(p1.first_name, ' ', p1.last_name) as Recruited_Member_Name,
                re.recruiter_id as Recruiter_ID,
                CONCAT(p2.first_name, ' ', p2.last_name) as Recruiter_Name,
                re.recruitment_date as Recruitment_Date,
                re.recruitment_method as Method
            FROM RecruitmentEvent re
            JOIN Participant p1 ON re.recruit_id = p1.participant_id
            LEFT JOIN Participant p2 ON re.recruiter_id = p2.participant_id
            ORDER BY re.recruitment_date DESC;
        """,
        "View All Transactions": """
            SELECT 
                t.transaction_id as Transaction_ID,
                t.from_member_id as From_Member,
                t.to_member_id as To_Member,
                t.amount as Amount,
                t.transaction_type as Type,
                t.transaction_date as Date,
                t.status as Status
            FROM Transaction t
            ORDER BY t.transaction_date DESC;
        """
    },
    
    "Analysis Reports": {
        "Recruitment Count per Manager": """
            SELECT 
                e.participant_id as Manager_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Manager_Name,
                e.role as Role,
                COUNT(re.recruit_id) as Total_Recruitments
            FROM Employee e
            JOIN Participant p ON e.participant_id = p.participant_id
            LEFT JOIN RecruitmentEvent re ON re.recruitment_date BETWEEN %s AND %s
            WHERE e.role LIKE '%%Recruitment%%'
            GROUP BY e.participant_id
            ORDER BY Total_Recruitments DESC;
        """,
        "Transaction Value per Finance Manager": """
            SELECT 
                e.participant_id as Manager_ID,
                CONCAT(p.first_name, ' ', p.last_name) as Manager_Name,
                e.role as Role,
                COUNT(t.transaction_id) as Transaction_Count,
                SUM(t.amount) as Total_Value
            FROM Employee e
            JOIN Participant p ON e.participant_id = p.participant_id
            LEFT JOIN Transaction t ON t.transaction_date BETWEEN %s AND %s
            WHERE e.role LIKE '%%Finance%%'
            GROUP BY e.participant_id
            ORDER BY Total_Value DESC;
        """,
        "Revenue Breakdown by Tier & Recruit Count": """
            SELECT 
                m.tier_level as Tier,
                COUNT(m.participant_id) as Member_Count,
                SUM(m.total_recruits) as Total_Recruits,
                SUM(t.amount) as Total_Revenue,
                ROUND(AVG(t.amount), 2) as Avg_Revenue_Per_Member
            FROM Member m
            LEFT JOIN Transaction t ON m.participant_id = t.from_member_id 
                AND t.status = 'completed'
                AND t.transaction_type = 'investment'
            GROUP BY m.tier_level
            ORDER BY m.tier_level;
        """
    },
    
    "Modification - Insert": {
        "Insert New Member": """
            INSERT INTO Member (participant_id, tier_level, recruiter_id, total_recruits, join_date, status)
            VALUES (%s, %s, %s, 0, CURDATE(), 'active');
        """,
        "Record Recruitment Event": """
            INSERT INTO RecruitmentEvent (recruit_id, recruiter_id, recruitment_date, recruitment_method)
            VALUES (%s, %s, CURDATE(), %s);
        """
    },
    
    "Modification - Delete": {
        "Delete Member": """
            DELETE FROM Member 
            WHERE participant_id = %s;
        """
    }
}

# ==============================================================================
# GUI APPLICATION
# ==============================================================================

class VoughtDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vought International - Database Management System")
        self.root.state('zoomed')  # Start maximized
        self.root.configure(bg='#f0f0f0')
        
        # User role - will be set by login
        self.user_role = None  # 'administrator', 'technician', 'member'
        
        # Theme system
        self.is_dark_mode = True
        self.themes = {
            'dark': {
                'bg': '#0f172a',
                'fg': '#ffffff',
                'sidebar_bg': '#1e293b',
                'button_bg': '#334155',
                'button_hover': '#475569',
                'button_fg': '#f8fafc',
                'accent': '#3b82f6',
                'muted': '#64748b',
                'header_bg': '#020617',
                'results_bg': '#1e293b',
                'entry_bg': '#334155',
                'entry_fg': '#f8fafc',
                'tree_bg': '#1e293b',
                'tree_fg': '#e2e8f0',
                'tree_select': '#1e40af',
                'dialog_bg': '#1e293b'
            },
            'light': {
                'bg': '#faf8f5',
                'fg': '#2c2416',
                'sidebar_bg': '#f5f1eb',
                'button_bg': '#e8e2d8',
                'button_hover': '#d4cbbe',
                'button_fg': '#2c2416',
                'accent': '#8b7355',
                'muted': '#6b5d4f',
                'header_bg': '#8b7355',
                'results_bg': '#fefdfb',
                'entry_bg': '#ffffff',
                'entry_fg': '#2c2416',
                'tree_bg': '#ffffff',
                'tree_fg': '#2c2416',
                'tree_select': '#d4cbbe',
                'dialog_bg': '#f5f1eb'
            }
        }
        
        # Test connection
        if not get_db_connection():
            messagebox.showerror("Connection Failed", "Unable to connect to database")
            self.root.destroy()
            return
        
        # Show role selection dialog
        self.show_role_selection()
    
    def show_role_selection(self):
        """Show role selection dialog at startup"""
        theme = self.get_theme()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Select User Role")
        dialog.configure(bg=theme['dialog_bg'])
        
        # Set size first
        dialog_width = 400
        dialog_height = 450
        
        # Get screen dimensions
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 2) - (dialog_height // 2)
        
        # Set geometry with size and position
        dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Prevent closing without selection
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Header
        header = tk.Frame(dialog, bg=theme['sidebar_bg'])
        header.pack(fill='x', pady=(0, 30))
        
        tk.Label(
            header,
            text="Select Your Role",
            font=('Segoe UI', 18, 'bold'),
            bg=theme['sidebar_bg'],
            fg=theme['fg']
        ).pack(pady=20)
        
        # Role buttons
        roles_frame = tk.Frame(dialog, bg=theme['dialog_bg'])
        roles_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        def select_role(role):
            self.user_role = role
            dialog.destroy()
            self.create_widgets()
        
        # Administrator button
        admin_btn = tk.Button(
            roles_frame,
            text="Administrator",
            command=lambda: select_role('administrator'),
            bg='#dc2626',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=15
        )
        admin_btn.pack(fill='x', pady=10)
        
        tk.Label(
            roles_frame,
            text="Full access to all queries and database operations",
            font=('Segoe UI', 9),
            bg=theme['dialog_bg'],
            fg=theme['muted']
        ).pack(pady=(0, 15))
        
        # Technician button
        tech_btn = tk.Button(
            roles_frame,
            text="Technical Staff",
            command=lambda: select_role('technician'),
            bg='#2563eb',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=15
        )
        tech_btn.pack(fill='x', pady=10)
        
        tk.Label(
            roles_frame,
            text="Access to portal and transaction queries",
            font=('Segoe UI', 9),
            bg=theme['dialog_bg'],
            fg=theme['muted']
        ).pack(pady=(0, 15))
        
        # Member button
        member_btn = tk.Button(
            roles_frame,
            text="Member",
            command=lambda: select_role('member'),
            bg='#16a34a',
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            pady=15
        )
        member_btn.pack(fill='x', pady=10)
        
        tk.Label(
            roles_frame,
            text="View-only access to member-relevant queries",
            font=('Segoe UI', 9),
            bg=theme['dialog_bg'],
            fg=theme['muted']
        ).pack(pady=(0, 15))
        
        self.root.wait_window(dialog)
    
    def filter_queries_by_role(self):
        """Filter queries based on user role"""
        if self.user_role == 'administrator':
            return QUERIES
        
        elif self.user_role == 'technician':
            # Technician: Portal and Transaction queries only
            filtered = {}
            
            # Add View Tables category with portal and transaction queries
            filtered["Retrieval - View Tables"] = {
                "View All Transactions": QUERIES["Retrieval - View Tables"]["View All Transactions"]
            }
            
            # Add Analysis Reports
            filtered["Analysis Reports"] = {
                "Transaction Value per Finance Manager": QUERIES["Analysis Reports"]["Transaction Value per Finance Manager"]
            }
            
            return filtered
        
        elif self.user_role == 'member':
            # Member: View-only relevant queries (no tier information)
            filtered = {}
            
            # Projection queries
            filtered["Retrieval - Projection"] = QUERIES["Retrieval - Projection"]
            
            # Search queries
            filtered["Retrieval - Search"] = QUERIES["Retrieval - Search"]
            
            # View recruitment events only
            filtered["Retrieval - View Tables"] = {
                "View All Recruitment Events": QUERIES["Retrieval - View Tables"]["View All Recruitment Events"]
            }
            
            return filtered
        
        return QUERIES
    
    def create_widgets(self):
        theme = self.get_theme()
        
        # Header
        self.header_frame = tk.Frame(self.root, bg=theme['header_bg'], height= 100)
        self.header_frame.pack(fill='x')
        self.header_frame.pack_propagate(False)
        
        # Title container for better visibility
        title_container = tk.Frame(self.header_frame, bg=theme['header_bg'])
        title_container.pack(side='left', fill='both', expand=True)
        
        # Role indicator
        role_display = {
            'administrator': '👑 Administrator',
            'technician': '🔧 Technical Staff',
            'member': '👤 Member'
        }
        
        tk.Label(
            title_container,
            text=role_display.get(self.user_role, ''),
            font=('Segoe UI', 10),
            bg=theme['header_bg'],
            fg='#94a3b8'
        ).pack(pady=(10, 0), anchor='w', padx=20)
        
        self.title_label = tk.Label(
            title_container,
            text="Vought International",
            font=('Segoe UI', 30, 'bold'),
            bg=theme['header_bg'],
            fg='#ffffff'
        )
        self.title_label.pack(pady=(5, 2), padx=20)
        
        self.subtitle_label = tk.Label(
            title_container,
            text="Database Management System",
            font=('Segoe UI', 15),
            bg=theme['header_bg'],
            fg='#e2e8f0' if self.is_dark_mode else '#f5f1eb'
        )
        self.subtitle_label.pack()
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            self.header_frame,
            text="☀" if self.is_dark_mode else "🌙",
            command=self.toggle_theme,
            bg=theme['button_bg'],
            fg='#ffffff' if self.is_dark_mode else '#2c2416',
            font=('Segoe UI', 20),
            relief='flat',
            cursor='hand2',
            borderwidth=0,
            width=3,
            height=1
        )
        self.theme_btn.pack(side='right', padx=20)
        
        # Start/Reset button (Administrator only)
        if self.user_role == 'administrator':
            self.reset_btn = tk.Button(
                self.header_frame,
                text="Start/Reset",
                command=self.reset_database,
                bg='#dc2626' if self.is_dark_mode else '#b91c1c',
                fg='#ffffff',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                cursor='hand2',
                borderwidth=0,
                padx=15,
                pady=8
            )
            self.reset_btn.pack(side='right', padx=10)
        
        # Main container
        self.main_container = tk.Frame(self.root, bg=theme['bg'])
        self.main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left sidebar
        self.sidebar_frame = tk.Frame(self.main_container, bg=theme['sidebar_bg'], width=280)
        self.sidebar_frame.pack(side='left', fill='y', padx=0)
        self.sidebar_frame.pack_propagate(False)
        
        self.sidebar_title = tk.Label(
            self.sidebar_frame,
            text="QUERIES",
            font=('Segoe UI', 18, 'bold'),
            bg=theme['sidebar_bg'],
            fg=theme['muted']
        )
        self.sidebar_title.pack(pady=20, padx=20, anchor='w')
        
        # Canvas with scrollbar
        self.canvas = tk.Canvas(self.sidebar_frame, bg=theme['sidebar_bg'], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=theme['sidebar_bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=280)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Store category frames for collapse/expand
        self.category_frames = {}
        
        # Get filtered queries based on role
        queries_to_display = self.filter_queries_by_role()
        
        # Add query buttons with collapsible categories
        for category, queries in queries_to_display.items():
            # Category header (clickable)
            cat_frame = tk.Frame(self.scrollable_frame, bg=theme['sidebar_bg'])
            cat_frame.pack(fill='x', pady=(0, 2))
            
            # Arrow and label in header
            header_frame = tk.Frame(cat_frame, bg=theme['sidebar_bg'], cursor='hand2')
            header_frame.pack(fill='x', padx=12)
            
            arrow_label = tk.Label(
                header_frame,
                text="▸",
                font=('Segoe UI', 12),
                bg=theme['sidebar_bg'],
                fg=theme['muted'],
                width=2
            )
            arrow_label.pack(side='left')
            
            cat_label = tk.Label(
                header_frame,
                text=category,
                font=('Segoe UI', 12, 'bold'),
                bg=theme['sidebar_bg'],
                fg=theme['fg'],
                anchor='w',
                pady=10
            )
            cat_label.pack(side='left', fill='x', expand=True, padx=(8, 0))
            
            # Container for query buttons (collapsible)
            queries_container = tk.Frame(cat_frame, bg=theme['sidebar_bg'])
            # Don't pack initially - start collapsed
            
            # Store references
            self.category_frames[category] = {
                'arrow': arrow_label,
                'container': queries_container,
                'expanded': False
            }
            
            # Add queries to container
            for query_name, query_sql in queries.items():
                # Determine if it's a modification query (INSERT, UPDATE, DELETE)
                is_modify = any(keyword in query_sql.upper()[:20] for keyword in ['INSERT', 'UPDATE', 'DELETE'])
                
                btn = tk.Button(
                    queries_container,
                    text=query_name,
                    font=('Segoe UI', 11),
                    bg=theme['sidebar_bg'],
                    fg=theme['button_fg'],
                    anchor='w',
                    padx=40,
                    pady=10,
                    relief='flat',
                    cursor='hand2',
                    borderwidth=0,
                    command=lambda q=query_sql, n=query_name, c=category, m=is_modify: self.handle_query(q, n, c, m)
                )
                btn.pack(fill='x')
                btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=theme['button_hover']))
                btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=theme['sidebar_bg']))
            
            # Bind click to toggle
            def make_toggle(cat):
                return lambda e: self.toggle_category(cat)
            
            header_frame.bind('<Button-1>', make_toggle(category))
            arrow_label.bind('<Button-1>', make_toggle(category))
            cat_label.bind('<Button-1>', make_toggle(category))
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Right side - Results
        self.results_frame = tk.Frame(self.main_container, bg=theme['results_bg'])
        self.results_frame.pack(side='right', fill='both', expand=True)
        
        # Results header
        results_header = tk.Frame(self.results_frame, bg=theme['results_bg'])
        results_header.pack(fill='x', padx=32, pady=24)
        
        self.category_label = tk.Label(
            results_header,
            text="Welcome",
            font=('Segoe UI', 11),
            bg=theme['results_bg'],
            fg=theme['muted']
        )
        self.category_label.pack(anchor='w')
        
        self.query_title_label = tk.Label(
            results_header,
            text="Select a query from the sidebar",
            font=('Segoe UI', 24, 'bold'),
            bg=theme['results_bg'],
            fg=theme['fg']
        )
        self.query_title_label.pack(anchor='w', pady=(4, 0))
        
        # Separator
        separator = tk.Frame(self.results_frame, height=1, bg=theme['muted'])
        separator.pack(fill='x', padx=32)
        
        # Treeview
        tree_frame = tk.Frame(self.results_frame, bg=theme['tree_bg'], relief='flat', borderwidth=0)
        tree_frame.pack(fill='both', expand=True, padx=32, pady=24)
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            show='headings'
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        tree_scroll_y.pack(side='right', fill='y')
        tree_scroll_x.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.apply_tree_theme()
    
    def get_theme(self):
        """Get current theme colors"""
        return self.themes['dark'] if self.is_dark_mode else self.themes['light']
    
    def apply_tree_theme(self):
        """Apply theme to treeview"""
        theme = self.get_theme()
        self.style.configure("Treeview",
                       background=theme['tree_bg'],
                       foreground=theme['tree_fg'],
                       rowheight=38,
                       fieldbackground=theme['tree_bg'],
                       borderwidth=1,
                       font=('Segoe UI', 11))
        self.style.configure("Treeview.Heading",
                       background=theme['results_bg'],
                       foreground=theme['muted'],
                       borderwidth=1,
                       relief='raised',
                       font=('Segoe UI', 12, 'bold'))
        self.style.map('Treeview',
                 background=[('selected', theme['tree_select'])],
                 foreground=[('selected', theme['tree_fg'] if self.is_dark_mode else '#2c2416')])
    
    def toggle_category(self, category):
        """Collapse or expand a category"""
        cat_info = self.category_frames[category]
        
        if cat_info['expanded']:
            # Collapse
            cat_info['container'].pack_forget()
            cat_info['arrow'].config(text="▸")
            cat_info['expanded'] = False
        else:
            # Expand
            cat_info['container'].pack(fill='x')
            cat_info['arrow'].config(text="▾")
            cat_info['expanded'] = True
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.is_dark_mode = not self.is_dark_mode
        theme = self.get_theme()
        
        # Update root background
        self.root.configure(bg=theme['bg'])
        
        # Update header
        self.header_frame.configure(bg=theme['header_bg'])
        self.title_label.configure(bg=theme['header_bg'], fg='#ffffff')
        self.subtitle_label.configure(bg=theme['header_bg'], fg='#e2e8f0' if self.is_dark_mode else '#f5f1eb')
        self.theme_btn.configure(
            text="☀" if self.is_dark_mode else "🌙",
            bg=theme['button_bg'],
            fg='#ffffff' if self.is_dark_mode else '#2c2416'
        )
        
        # Update reset button (if exists - administrator only)
        if hasattr(self, 'reset_btn'):
            self.reset_btn.configure(
                bg='#dc2626' if self.is_dark_mode else '#b91c1c'
            )
        
        # Update main container
        self.main_container.configure(bg=theme['bg'])
        
        # Update sidebar
        self.sidebar_frame.configure(bg=theme['sidebar_bg'])
        self.sidebar_title.configure(bg=theme['sidebar_bg'], fg=theme['muted'])
        self.canvas.configure(bg=theme['sidebar_bg'])
        self.scrollable_frame.configure(bg=theme['sidebar_bg'])
        
        # Update categories and buttons
        for category, cat_info in self.category_frames.items():
            cat_info['arrow'].master.master.configure(bg=theme['sidebar_bg'])
            cat_info['arrow'].master.configure(bg=theme['sidebar_bg'])
            cat_info['arrow'].configure(bg=theme['sidebar_bg'], fg=theme['muted'])
            
            # Update category label
            for child in cat_info['arrow'].master.winfo_children():
                if isinstance(child, tk.Label) and child != cat_info['arrow']:
                    child.configure(bg=theme['sidebar_bg'], fg=theme['fg'])
            
            # Update query buttons in container
            cat_info['container'].configure(bg=theme['sidebar_bg'])
            for btn in cat_info['container'].winfo_children():
                if isinstance(btn, tk.Button):
                    btn.configure(bg=theme['sidebar_bg'], fg=theme['button_fg'])
                    # Rebind hover events with new theme
                    btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=theme['button_hover']))
                    btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=theme['sidebar_bg']))
        
        # Update results area
        self.results_frame.configure(bg=theme['results_bg'])
        for child in self.results_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=theme['results_bg'])
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.configure(bg=theme['results_bg'])
                        if subchild == self.category_label:
                            subchild.configure(fg=theme['muted'])
                        elif subchild == self.query_title_label:
                            subchild.configure(fg=theme['fg'])
        
        # Update treeview
        self.apply_tree_theme()
    
    def reset_database(self):
        """Execute schema.sql and populate.sql to reset the database"""
        # Confirm with user
        confirm = messagebox.askyesno(
            "Reset Database",
            "This will DROP and recreate the VoughDB database. All existing data will be lost! Do you want to continue?"
        )
        
        if not confirm:
            return
        
        # Get the directory where main_app.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(script_dir, 'schema.sql')
        populate_path = os.path.join(script_dir, 'populate.sql')
        
        # Execute schema.sql (creates database and tables)
        success, message = execute_sql_file(schema_path)
        if not success:
            messagebox.showerror("Schema Error", message)
            return
        
        # Execute populate.sql (loads data into VoughDB)
        success, message = execute_sql_file(populate_path)
        if not success:
            messagebox.showerror("Populate Error", message)
            return
        
        messagebox.showinfo("Success", "Database has been reset successfully!Schema and sample data loaded.")
        
        # Clear any existing results
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def handle_query(self, query, query_name, category, is_modify):
        """Handle both SELECT and UPDATE queries - all are now parameterized"""
        # Count parameters needed
        param_count = query.count('%s')
        
        if param_count == 0:
            # No parameters needed, execute directly
            if is_modify:
                success, message = execute_update(query)
                messagebox.showinfo("Result", message)
            else:
                self.execute_and_display(query, query_name, category, None)
        else:
            # Show parameter input dialog
            self.show_parameter_dialog(query, query_name, category, is_modify, param_count)
    
    def show_parameter_dialog(self, query, query_name, category, is_modify, param_count):
        """Show parameter input dialog for any query"""
        theme = self.get_theme()
        self.category_label.config(text=category)
        self.query_title_label.config(text=query_name)
        
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        
        # Create input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Enter Parameters - {query_name}")
        
        # Adjust dialog size based on parameter count
        dialog_height = 200 + (param_count * 80)
        dialog.geometry(f"500x{dialog_height}")
        dialog.configure(bg=theme['dialog_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=theme['dialog_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Header
        header = tk.Frame(dialog, bg=theme['sidebar_bg'])
        header.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            header,
            text=f"Enter Parameters",
            font=('Segoe UI', 16, 'bold'),
            bg=theme['sidebar_bg'],
            fg=theme['fg']
        ).pack(pady=20, padx=20, anchor='w')
        
        tk.Label(
            header,
            text=query_name,
            font=('Segoe UI', 11),
            bg=theme['sidebar_bg'],
            fg=theme['muted']
        ).pack(padx=20, anchor='w')
        
        # Create parameter entries
        entries = []
        param_labels = self.get_parameter_labels(query_name, param_count)
        
        entries_frame = tk.Frame(dialog, bg=theme['dialog_bg'])
        entries_frame.pack(fill='x', padx=20)
        
        for i, label in enumerate(param_labels):
            frame = tk.Frame(entries_frame, bg=theme['dialog_bg'])
            frame.pack(pady=8, fill='x')
            
            tk.Label(
                frame,
                text=f"{label}",
                font=('Segoe UI', 11),
                bg=theme['dialog_bg'],
                fg=theme['muted']
            ).pack(anchor='w', pady=(0, 4))
            
            entry = tk.Entry(
                frame, 
                font=('Segoe UI', 12),
                relief='solid',
                borderwidth=1,
                bg=theme['entry_bg'],
                fg=theme['entry_fg']
            )
            entry.pack(fill='x', ipady=6)
            entries.append(entry)
        
        def execute():
            try:
                params = list(entry.get().strip() for entry in entries)
                if not all(param != '' for param in params):
                    messagebox.showwarning("Missing Parameters", "Please fill all fields")
                    return
                
                # Handle special case for Insert New Member - convert '0' or 'NULL' to None for recruiter_id
                if query_name == "Insert New Member" and len(params) >= 3:
                    if params[2] == '0' or params[2].upper() == 'NULL':
                        params[2] = None
                
                # Handle special case for Record Recruitment Event - convert '0' or 'NULL' to None for recruiter_id
                if query_name == "Record Recruitment Event" and len(params) >= 2:
                    if params[1] == '0' or params[1].upper() == 'NULL':
                        params[1] = None
                
                params = tuple(params)
                dialog.destroy()
                
                if is_modify:
                    # Execute modification query
                    success, message = execute_update(query, params)
                    messagebox.showinfo("Result", message)
                else:
                    # Execute retrieval query and display results
                    self.execute_and_display(query, query_name, category, params)
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = tk.Frame(dialog, bg=theme['dialog_bg'])
        btn_frame.pack(pady=24)
        
        execute_btn_bg = theme['accent'] if self.is_dark_mode else theme['header_bg']
        tk.Button(
            btn_frame,
            text="Execute",
            command=execute,
            bg=execute_btn_bg,
            fg='#ffffff',
            font=('Segoe UI', 12, 'bold'),
            padx=32,
            pady=12,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        ).pack(side='left', padx=5)
        
        cancel_btn_bg = theme['button_bg']
        cancel_btn_fg = theme['muted']
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=cancel_btn_bg,
            fg=cancel_btn_fg,
            font=('Segoe UI', 12),
            padx=32,
            pady=12,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        ).pack(side='left', padx=5)
    
    def get_parameter_labels(self, query_name, param_count):
        """Return friendly labels for parameters"""
        labels_map = {
            # Retrieval - Selection
            "Members by Tier & Time Period": ["Tier Level (1-7)", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            
            # Retrieval - Aggregate SUM
            "Total Revenue by Tier & Year": ["Tier Level (1-7)", "Year (YYYY)"],
            
            # Retrieval - Aggregate MAX
            "Highest Revenue Member by Tier & Period": ["Tier Level (1-7)", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            
            # Retrieval - Aggregate MIN
            "Lowest Revenue Member by Tier & Period": ["Tier Level (1-7)", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            
            # Retrieval - Time Range
            "Members Recruited in Time Range": ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            
            # Retrieval - Search
            "Search Participants by Name": ["Name or Partial Name"],
            
            # Analysis Reports
            "Recruitment Count per Manager": ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            "Transaction Value per Finance Manager": ["Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
            
            # Modification - Insert
            "Insert New Member": ["Participant ID", "Tier Level (1-7)", "Recruiter ID (0 or NULL if none)"],
            "Record Recruitment Event": ["Recruit ID (New Member)", "Recruiter ID (0 or NULL if none)", "Recruitment Method"],
            
            # Modification - Delete
            "Delete Member": ["Member Participant ID to Delete"]
        }
        
        if query_name in labels_map:
            return labels_map[query_name]
        
        # Default labels
        return [f"Parameter {i+1}" for i in range(param_count)]
    
    def execute_and_display(self, query, query_name, category, params=None):
        """Execute query and display results"""
        self.category_label.config(text=category)
        self.query_title_label.config(text=query_name)
        
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        
        # Execute query
        columns, results = execute_query(query, params)
        
        if columns is None:
            return
        
        # Configure columns
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=150, anchor='w')
        
        # Insert data
        if results:
            for row in results:
                self.tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("No Results", "Query returned no results.")

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = VoughtDatabaseGUI(root)
    root.mainloop()
