import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
import sys

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

# ==============================================================================
# QUERY DEFINITIONS - Simple but Exhaustive
# ==============================================================================

QUERIES = {
    "Overview": {
        "Database Summary": """
            SELECT 'Total Universes' as Metric, COUNT(*) as Value FROM Universe
            UNION ALL SELECT 'Total Participants', COUNT(*) FROM Participant
            UNION ALL SELECT 'Total Members', COUNT(*) FROM Member
            UNION ALL SELECT 'Active Members', COUNT(*) FROM Member WHERE status = 'active'
            UNION ALL SELECT 'Total Employees', COUNT(*) FROM Employee
            UNION ALL SELECT 'Total Portals', COUNT(*) FROM Portals
            UNION ALL SELECT 'Total Transactions', COUNT(*) FROM Transaction;
        """,
        "Members by Tier": """
            SELECT 
                m.tier_level as Tier,
                COUNT(*) as Total_Members,
                it.commission_rate as Commission_Rate,
                it.minimum_investment as Min_Investment
            FROM Member m
            JOIN InvestmentTier it ON m.tier_level = it.tier_id
            GROUP BY m.tier_level
            ORDER BY m.tier_level;
        """,
        "Universe Statistics": """
            SELECT 
                u.universe_name as Universe,
                COUNT(DISTINCT p.participant_id) as Total_Participants,
                COUNT(DISTINCT m.participant_id) as Members,
                u.status as Status
            FROM Universe u
            LEFT JOIN Participant p ON u.universe_id = p.universe_id
            LEFT JOIN Member m ON p.participant_id = m.participant_id
            GROUP BY u.universe_id
            ORDER BY Members DESC;
        """
    },
    
    "Members": {
        "All Members": """
            SELECT 
                p.participant_id as ID,
                CONCAT(p.first_name, ' ', p.last_name) as Name,
                u.universe_name as Universe,
                m.tier_level as Tier,
                m.total_recruits as Recruits,
                m.join_date as Joined,
                m.status as Status
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            ORDER BY m.tier_level, m.join_date
            LIMIT 50;
        """,
        "Top 20 Recruiters": """
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) as Name,
                u.universe_name as Universe,
                m.tier_level as Tier,
                m.total_recruits as Recruits
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE m.total_recruits > 0
            ORDER BY m.total_recruits DESC
            LIMIT 20;
        """,
        "Tier 1 Founders": """
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) as Founder,
                u.universe_name as Universe,
                m.total_recruits as Recruits,
                m.join_date as Founded
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            WHERE m.tier_level = 1
            ORDER BY u.universe_name;
        """,
        "Recent Recruits": """
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) as Name,
                u.universe_name as Universe,
                m.tier_level as Tier,
                m.join_date as Joined
            FROM Member m
            JOIN Participant p ON m.participant_id = p.participant_id
            JOIN Universe u ON p.universe_id = u.universe_id
            ORDER BY m.join_date DESC
            LIMIT 20;
        """
    },
    
    "Finances": {
        "Transaction Summary": """
            SELECT 
                transaction_type as Type,
                COUNT(*) as Count,
                SUM(amount) as Total,
                ROUND(AVG(amount), 2) as Average
            FROM Transaction
            GROUP BY transaction_type
            ORDER BY Total DESC;
        """,
        "Top Commission Earners": """
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) as Member,
                m.tier_level as Tier,
                SUM(t.amount) as Total_Commission
            FROM Transaction t
            JOIN Member m ON t.to_member_id = m.participant_id
            JOIN Participant p ON m.participant_id = p.participant_id
            WHERE t.transaction_type = 'commission'
            GROUP BY m.participant_id
            ORDER BY Total_Commission DESC
            LIMIT 15;
        """,
        "Investment by Tier": """
            SELECT 
                m.tier_level as Tier,
                COUNT(DISTINCT t.from_member_id) as Investors,
                SUM(t.amount) as Total_Investment
            FROM Transaction t
            JOIN Member m ON t.from_member_id = m.participant_id
            WHERE t.transaction_type = 'investment'
            GROUP BY m.tier_level
            ORDER BY m.tier_level;
        """,
        "Recent Transactions": """
            SELECT 
                t.transaction_id as ID,
                t.transaction_type as Type,
                t.amount as Amount,
                t.transaction_date as Date,
                t.status as Status
            FROM Transaction t
            ORDER BY t.transaction_date DESC
            LIMIT 30;
        """
    },
    
    "Portals": {
        "All Portals": """
            SELECT 
                p.portal_id as ID,
                u1.universe_name as From_Universe,
                u2.universe_name as To_Universe,
                p.status as Status,
                p.cost as Cost
            FROM Portals p
            JOIN Universe u1 ON p.source_universe_id = u1.universe_id
            JOIN Universe u2 ON p.target_universe_id = u2.universe_id
            ORDER BY u1.universe_name;
        """,
        "Portal Status": """
            SELECT 
                status as Status,
                COUNT(*) as Count,
                SUM(cost) as Total_Cost
            FROM Portals
            GROUP BY status;
        """,
        "Recent Calibrations": """
            SELECT 
                pc.calibration_code as Code,
                u1.universe_name as Source,
                u2.universe_name as Target,
                pc.calibration_timestamp as Timestamp
            FROM PortalCalibration pc
            JOIN Portals po ON pc.portal_id = po.portal_id
            JOIN Universe u1 ON po.source_universe_id = u1.universe_id
            JOIN Universe u2 ON po.target_universe_id = u2.universe_id
            ORDER BY pc.calibration_timestamp DESC
            LIMIT 20;
        """
    },
    
    "Employees": {
        "All Employees": """
            SELECT 
                e.participant_id as ID,
                CONCAT(p.first_name, ' ', p.last_name) as Name,
                e.role as Role,
                e.access_level as Level,
                e.salary as Salary,
                e.status as Status
            FROM Employee e
            JOIN Participant p ON e.participant_id = p.participant_id
            ORDER BY e.access_level, e.salary DESC;
        """,
        "By Access Level": """
            SELECT 
                e.access_level as Level,
                COUNT(*) as Count,
                ROUND(AVG(e.salary), 2) as Avg_Salary
            FROM Employee e
            GROUP BY e.access_level
            ORDER BY e.access_level;
        """,
        "Engineers": """
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) as Engineer,
                e.role as Role,
                COUNT(DISTINCT po.portal_id) as Portals_Managed
            FROM Employee e
            JOIN Participant p ON e.participant_id = p.participant_id
            LEFT JOIN Portals po ON e.participant_id = po.engineer_id
            WHERE e.role LIKE '%Engineer%'
            GROUP BY e.participant_id
            ORDER BY Portals_Managed DESC;
        """
    },
    
    "Campaigns": {
        "All Campaigns": """
            SELECT 
                mc.program_id as ID,
                mc.program_code as Code,
                mca.name as Campaign_Name,
                mca.budget as Budget,
                mca.status as Status
            FROM MarketingCampaign mc
            JOIN MarketingCampaignAdditional mca ON mc.program_code = mca.program_code
            ORDER BY mca.start_date DESC;
        """,
        "Active Campaigns": """
            SELECT 
                mca.name as Campaign,
                u.universe_name as Universe,
                mca.budget as Budget,
                mca.start_date as Started,
                mca.end_date as Ends
            FROM MarketingCampaignAdditional mca
            JOIN MarketingCampaign mc ON mca.program_code = mc.program_code
            JOIN Universe u ON mca.universe_id = u.universe_id
            WHERE mca.status = 'active';
        """
    },
    
    "Analytics": {
        "Recruitment Efficiency": """
            SELECT 
                u.universe_name as Universe,
                COUNT(DISTINCT m.participant_id) as Total_Members,
                COUNT(DISTINCT re.recruit_id) as Total_Recruits,
                ROUND(AVG(m.total_recruits), 2) as Avg_Recruits_Per_Member,
                MAX(m.total_recruits) as Max_Recruits
            FROM Universe u
            LEFT JOIN Participant p ON u.universe_id = p.universe_id
            LEFT JOIN Member m ON p.participant_id = m.participant_id
            LEFT JOIN RecruitmentEvent re ON m.participant_id = re.recruiter_id
            GROUP BY u.universe_id
            ORDER BY Total_Members DESC;
        """,
        "Tier Performance": """
            SELECT 
                it.tier_id as Tier,
                COUNT(m.participant_id) as Member_Count,
                it.minimum_investment as Min_Investment,
                it.commission_rate as Commission_Rate,
                SUM(m.total_recruits) as Total_Recruits,
                ROUND(AVG(m.total_recruits), 2) as Avg_Recruits
            FROM InvestmentTier it
            LEFT JOIN Member m ON it.tier_id = m.tier_level
            GROUP BY it.tier_id
            ORDER BY it.tier_id;
        """,
        "Portal Usage Analysis": """
            SELECT 
                u.universe_name as Universe,
                COUNT(DISTINCT CASE WHEN p.status = 'active' THEN p.portal_id END) as Active_Portals,
                COUNT(DISTINCT CASE WHEN p.status = 'maintenance' THEN p.portal_id END) as Maintenance,
                COUNT(DISTINCT CASE WHEN p.status = 'closed' THEN p.portal_id END) as Closed,
                COUNT(DISTINCT pc.calibration_code) as Total_Calibrations
            FROM Universe u
            LEFT JOIN Portals p ON u.universe_id = p.source_universe_id
            LEFT JOIN PortalCalibration pc ON p.portal_id = pc.portal_id
            GROUP BY u.universe_id
            ORDER BY Active_Portals DESC;
        """,
        "Revenue by Universe": """
            SELECT 
                u.universe_name as Universe,
                COUNT(DISTINCT t.transaction_id) as Transaction_Count,
                SUM(CASE WHEN t.transaction_type = 'investment' THEN t.amount ELSE 0 END) as Total_Investment,
                SUM(CASE WHEN t.transaction_type = 'commission' THEN t.amount ELSE 0 END) as Total_Commission,
                SUM(CASE WHEN t.transaction_type = 'bonus' THEN t.amount ELSE 0 END) as Total_Bonus
            FROM Universe u
            LEFT JOIN Participant p ON u.universe_id = p.universe_id
            LEFT JOIN Member m ON p.participant_id = m.participant_id
            LEFT JOIN Transaction t ON m.participant_id = t.from_member_id OR m.participant_id = t.to_member_id
            GROUP BY u.universe_id
            ORDER BY Total_Investment DESC;
        """,
        "Monthly Growth": """
            SELECT 
                DATE_FORMAT(join_date, '%Y-%m') as Month,
                COUNT(*) as New_Members,
                SUM(COUNT(*)) OVER (ORDER BY DATE_FORMAT(join_date, '%Y-%m')) as Cumulative_Members
            FROM Member
            GROUP BY DATE_FORMAT(join_date, '%Y-%m')
            ORDER BY Month DESC
            LIMIT 12;
        """
    },
    
    "Modify": {
        "Activate Member": """
            UPDATE Member 
            SET status = 'active' 
            WHERE participant_id = ? AND status = 'suspended';
        """,
        "Suspend Member": """
            UPDATE Member 
            SET status = 'suspended' 
            WHERE participant_id = ? AND status = 'active';
        """,
        "Update Member Tier": """
            UPDATE Member 
            SET tier_level = ? 
            WHERE participant_id = ?;
        """,
        "Activate Portal": """
            UPDATE Portals 
            SET status = 'active' 
            WHERE portal_id = ? AND status IN ('maintenance', 'closed');
        """,
        "Close Portal": """
            UPDATE Portals 
            SET status = 'closed' 
            WHERE portal_id = ? AND status = 'active';
        """,
        "Set Portal Maintenance": """
            UPDATE Portals 
            SET status = 'maintenance' 
            WHERE portal_id = ? AND status = 'active';
        """,
        "Update Portal Cost": """
            UPDATE Portals 
            SET cost = ? 
            WHERE portal_id = ?;
        """,
        "Complete Pending Transaction": """
            UPDATE Transaction 
            SET status = 'completed' 
            WHERE transaction_id = ? AND status = 'pending';
        """,
        "Cancel Transaction": """
            UPDATE Transaction 
            SET status = 'cancelled' 
            WHERE transaction_id = ? AND status = 'pending';
        """,
        "Update Employee Salary": """
            UPDATE Employee 
            SET salary = ? 
            WHERE participant_id = ?;
        """,
        "Change Employee Status": """
            UPDATE Employee 
            SET status = 'inactive' 
            WHERE participant_id = ? AND status = 'active';
        """,
        "Update Campaign Status": """
            UPDATE MarketingCampaignAdditional 
            SET status = ? 
            WHERE program_code = ?;
        """,
        "Increment Member Recruits": """
            UPDATE Member 
            SET total_recruits = total_recruits + 1 
            WHERE participant_id = ?;
        """,
        "Update Universe Status": """
            UPDATE Universe 
            SET status = ? 
            WHERE universe_id = ?;
        """,
        "Assign Portal Engineer": """
            UPDATE Portals 
            SET engineer_id = ? 
            WHERE portal_id = ?;
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
        
        self.create_widgets()
    
    def create_widgets(self):
        theme = self.get_theme()
        
        # Header
        self.header_frame = tk.Frame(self.root, bg=theme['header_bg'], height= 100)
        self.header_frame.pack(fill='x')
        self.header_frame.pack_propagate(False)
        
        # Title container for better visibility
        title_container = tk.Frame(self.header_frame, bg=theme['header_bg'])
        title_container.pack(side='left', fill='both', expand=True)
        
        self.title_label = tk.Label(
            title_container,
            text="Vought International",
            font=('Segoe UI', 30, 'bold'),
            bg=theme['header_bg'],
            fg='#ffffff'
        )
        self.title_label.pack(pady=(15, 2))
        
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
        
        # Add query buttons with collapsible categories
        for category, queries in QUERIES.items():
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
                is_modify = category == "Modify"
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
    
    def handle_query(self, query, query_name, category, is_modify):
        """Handle both SELECT and UPDATE queries"""
        if is_modify:
            self.execute_modify_query(query, query_name, category)
        else:
            self.execute_and_display(query, query_name, category)
    
    def execute_modify_query(self, query, query_name, category):
        """Execute UPDATE query with parameter input"""
        theme = self.get_theme()
        self.category_label.config(text=category)
        self.query_title_label.config(text=query_name)
        
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        
        # Count parameters needed
        param_count = query.count('?')
        
        if param_count == 0:
            # No parameters needed, execute directly
            success, message = execute_update(query)
            messagebox.showinfo("Result", message)
            return
        
        # Create input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Enter Parameters - {query_name}")
        dialog.geometry("450x350")
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
                params = tuple(entry.get() for entry in entries)
                if not all(params):
                    messagebox.showwarning("Missing Parameters", "Please fill all fields")
                    return
                
                success, message = execute_update(query, params)
                dialog.destroy()
                messagebox.showinfo("Result", message)
                
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
            "Activate Member": ["Member ID"],
            "Suspend Member": ["Member ID"],
            "Update Member Tier": ["New Tier (1-7)", "Member ID"],
            "Activate Portal": ["Portal ID"],
            "Close Portal": ["Portal ID"],
            "Set Portal Maintenance": ["Portal ID"],
            "Update Portal Cost": ["New Cost", "Portal ID"],
            "Complete Pending Transaction": ["Transaction ID"],
            "Cancel Transaction": ["Transaction ID"],
            "Update Employee Salary": ["New Salary", "Employee ID"],
            "Change Employee Status": ["Employee ID"],
            "Update Campaign Status": ["New Status", "Program Code"],
            "Increment Member Recruits": ["Member ID"],
            "Update Universe Status": ["New Status", "Universe ID"],
            "Assign Portal Engineer": ["Engineer ID", "Portal ID"]
        }
        
        if query_name in labels_map:
            return labels_map[query_name]
        
        # Default labels
        return [f"Parameter {i+1}" for i in range(param_count)]
    
    def execute_and_display(self, query, query_name, category):
        """Execute query and display results"""
        self.category_label.config(text=category)
        self.query_title_label.config(text=query_name)
        
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        
        # Execute query
        columns, results = execute_query(query)
        
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
