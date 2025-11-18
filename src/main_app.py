import mysql.connector
from mysql.connector import Error
from datetime import date
import sys

# IMPORT CONFIGURATION
try:
    import db_config
except ImportError:
    print("[!] Error: 'db_config.py' not found. Please create it with your DB credentials.")
    sys.exit(1)

# ==============================================================================
# 1. DATABASE CONNECTIVITY
# ==============================================================================
def get_db_connection():
    """
    Establishes a secure connection to the VoughtDB using credentials
    from the db_config.py file.
    """
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
        print(f"\n[!] Database Connection Error: {e}")
        print(f"    Check your credentials in 'db_config.py' and ensure MySQL is running.")
        return None

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def execute_read_query(title, sql, params=None):
    """
    Executes a SELECT query and prints the results in a CLI-friendly format.
    Enforces SQL Purity and Parameterization.
    """
    conn = get_db_connection()
    if not conn: return

    cursor = conn.cursor()
    try:
        print_header(title)
        cursor.execute(sql, params)
        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        if not rows:
            print("No records found matching your criteria.")
        else:
            col_fmt = " | ".join([f"{col}" for col in columns])
            print(col_fmt)
            print("-" * (len(col_fmt) + 10))
            
            for row in rows:
                row_display = [str(item) if item is not None else 'NULL' for item in row]
                print(" | ".join(row_display))
                
    except Error as e:
        print(f"[!] SQL Error: {e}")
    finally:
        cursor.close()
        conn.close()

def execute_write_query(title, sql, params):
    """
    Executes INSERT, UPDATE, DELETE queries.
    """
    conn = get_db_connection()
    if not conn: return False

    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
        print(f"\n[+] Success: {title}")
        print(f"    Rows affected: {cursor.rowcount}")
        return True
    except Error as e:
        conn.rollback()
        print(f"\n[!] Operation Failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ==============================================================================
# 3. FUNCTIONAL REQUIREMENTS IMPLEMENTATION
# ==============================================================================

# --- 3.1 RETRIEVAL OPERATIONS ---

def req_selection_recent_recruiters():
    # 3.1.1 Selection
    sql = """
    SELECT DISTINCT p.first_name, p.last_name, m.tier_level, re.recruitment_date
    FROM Member m
    JOIN Participant p ON m.participant_id = p.participant_id
    JOIN RecruitmentEvent re ON m.participant_id = re.recruiter_id
    WHERE m.tier_level = 1 
    AND re.recruitment_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
    """
    execute_read_query("RECENT LEVEL 1 RECRUITERS (Last 1 Year)", sql)

def req_projection_active_participants():
    # 3.1.2 Projection
    sql = """
    SELECT p.participant_id, p.first_name, p.last_name, u.universe_name, p.planet, p.country
    FROM Participant p
    JOIN Member m ON p.participant_id = m.participant_id
    JOIN Universe u ON p.universe_id = u.universe_id
    WHERE m.status = 'active'
    LIMIT 20;
    """
    execute_read_query("ACTIVE PARTICIPANTS (Showing first 20)", sql)

def req_aggregate_sum_revenue():
    # 3.1.3(a) Aggregate Sum
    sql = """
    SELECT SUM(t.amount) AS total_revenue_level_2
    FROM Member m
    JOIN Transaction t ON m.participant_id = t.to_member_id
    WHERE m.tier_level = 2 AND t.transaction_type = 'investment';
    """
    execute_read_query("TOTAL REVENUE: LEVEL 2 MEMBERS", sql)

def req_aggregate_max_min_revenue():
    # 3.1.3(b/c) Aggregate Max/Min
    print_header("LEVEL 3 REVENUE ANALYSIS")
    
    sql_max = """
    SELECT p.first_name, p.last_name, SUM(t.amount) as total_yield
    FROM Member m
    JOIN Participant p ON m.participant_id = p.participant_id
    JOIN Transaction t ON m.participant_id = t.to_member_id
    WHERE m.tier_level = 3 AND t.transaction_type = 'investment'
    GROUP BY m.participant_id
    ORDER BY total_yield DESC LIMIT 1;
    """
    
    sql_min = """
    SELECT p.first_name, p.last_name, SUM(t.amount) as total_yield
    FROM Member m
    JOIN Participant p ON m.participant_id = p.participant_id
    JOIN Transaction t ON m.participant_id = t.to_member_id
    WHERE m.tier_level = 3 AND t.transaction_type = 'investment'
    GROUP BY m.participant_id
    ORDER BY total_yield ASC LIMIT 1;
    """
    
    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_max)
        max_res = cursor.fetchone()
        cursor.execute(sql_min)
        min_res = cursor.fetchone()
        
        print(f"Highest Yielding Member: {max_res[0]} {max_res[1]} (${max_res[2]})" if max_res else "No data found.")
        print(f"Lowest Yielding Member:  {min_res[0]} {min_res[1]} (${min_res[2]})" if min_res else "No data found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def req_search_participant():
    # 3.1.4 Search
    term = input("\nEnter name to search (e.g., 'Stark'): ")
    sql = """
    SELECT p.participant_id, p.first_name, p.last_name, m.status, u.universe_name 
    FROM Participant p
    LEFT JOIN Member m ON p.participant_id = m.participant_id
    LEFT JOIN Universe u ON p.universe_id = u.universe_id
    WHERE p.first_name LIKE %s OR p.last_name LIKE %s;
    """
    execute_read_query(f"SEARCH RESULTS FOR '{term}'", sql, (f"%{term}%", f"%{term}%"))

# --- 3.2 ANALYSIS REPORTS ---

def report_manager_performance():
    # 3.2(1) Manager Performance
    sql = """
    SELECT e.participant_id, p.first_name, p.last_name, COUNT(re.recruit_id) AS recruitments_managed
    FROM Employee e
    JOIN Participant p ON e.participant_id = p.participant_id
    JOIN Member m ON e.participant_id = m.participant_id
    JOIN RecruitmentEvent re ON m.participant_id = re.recruiter_id
    WHERE e.role LIKE '%Recruitment Manager%'
    GROUP BY e.participant_id, p.first_name, p.last_name
    ORDER BY recruitments_managed DESC;
    """
    execute_read_query("PERFORMANCE: RECRUITMENT MANAGERS", sql)

def report_revenue_breakdown():
    # 3.2(3) Revenue Breakdown
    sql = """
    SELECT 
        m.tier_level, 
        COUNT(DISTINCT m.participant_id) AS total_members,
        SUM(m.total_recruits) AS total_downline_recruits,
        SUM(t.amount) AS total_revenue_generated
    FROM Member m
    JOIN Transaction t ON m.participant_id = t.to_member_id
    WHERE t.transaction_type = 'investment'
    GROUP BY m.tier_level
    ORDER BY total_revenue_generated DESC;
    """
    execute_read_query("REVENUE BREAKDOWN BY TIER", sql)

# --- 3.3 MODIFICATION OPERATIONS ---

def mod_insert_recruit():
    # 3.3(a) Insert
    print_header("REGISTER NEW RECRUIT")
    conn = get_db_connection()
    if not conn: return

    try:
        cursor = conn.cursor()
        recruiter_id = input("Enter Recruiter ID: ")
        
        # Constraint Check
        check_sql = """
        SELECT m.total_recruits, p.universe_id 
        FROM Member m 
        JOIN Participant p ON m.participant_id = p.participant_id 
        WHERE m.participant_id = %s
        """
        cursor.execute(check_sql, (recruiter_id,))
        result = cursor.fetchone()
        
        if not result:
            print("[!] Error: Recruiter ID not found.")
            return
        if result[0] >= 7:
            print("[!] Error: Recruiter has reached maximum limit (7).")
            return
            
        universe_id = result[1]
        fname = input("First Name: ")
        lname = input("Last Name: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        planet = input("Planet: ")
        country = input("Country: ")
        
        conn.start_transaction()
        
        # Insert Participant
        sql_part = "INSERT INTO Participant (first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES (%s, %s, %s, %s, %s, %s, 1)"
        cursor.execute(sql_part, (fname, lname, dob, universe_id, planet, country))
        new_id = cursor.lastrowid
        
        # Insert Member (Tier 9 default)
        sql_mem = "INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES (%s, 9, CURDATE(), 'active', %s, 0)"
        cursor.execute(sql_mem, (new_id, recruiter_id))
        
        # Update Recruiter
        cursor.execute("UPDATE Member SET total_recruits = total_recruits + 1 WHERE participant_id = %s", (recruiter_id,))
        
        # Log Event
        cursor.execute("INSERT INTO RecruitmentEvent (recruiter_id, recruit_id, recruitment_date, recruitment_method) VALUES (%s, %s, CURDATE(), 'personal')", (recruiter_id, new_id))

        conn.commit()
        print(f"\n[+] Success: Added {fname} {lname} (ID: {new_id})")
        
    except Error as e:
        conn.rollback()
        print(f"\n[!] Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()

def mod_update_tier():
    # 3.3(b) Update
    print_header("PROMOTE MEMBER")
    member_id = input("Enter Member ID to promote: ")
    new_tier = input("Enter new Investment Tier ID (1-10): ")
    
    if not new_tier.isdigit() or not (1 <= int(new_tier) <= 10):
        print("[!] Invalid Tier.")
        return

    sql = "UPDATE Member SET tier_level = %s WHERE participant_id = %s"
    execute_write_query(f"Member {member_id} Promoted", sql, (new_tier, member_id))

def mod_delete_member():
    # 3.3(c) Delete
    print_header("TERMINATE MEMBER")
    member_id = input("Enter Member ID to terminate: ")
    confirm = input(f"Are you sure you want to delete ID {member_id}? (y/n): ")
    
    if confirm.lower() == 'y':
        sql = "DELETE FROM Participant WHERE participant_id = %s"
        execute_write_query(f"Member {member_id} Terminated", sql, (member_id,))
    else:
        print("Cancelled.")

# ==============================================================================
# 2. USER INTERFACE
# ==============================================================================
def main_menu():
    while True:
        print("\n" + "="*50)
        print(" VOUGHT INTERNATIONAL: PYRAMID SCHEME MANAGER")
        print("="*50)
        print(" 1. View Recent Level 1 Recruiters")
        print(" 2. View Active Participants")
        print(" 3. View Total Revenue (Level 2)")
        print(" 4. View Top/Bottom Earners (Level 3)")
        print(" 5. Search for Participant")
        print("-" * 50)
        print(" 6. Report: Manager Performance")
        print(" 7. Report: Revenue Breakdown by Tier")
        print("-" * 50)
        print(" 8. Register New Recruit (INSERT)")
        print(" 9. Promote Member (UPDATE)")
        print(" 10. Terminate Member (DELETE)")
        print(" 0. Exit")
        
        choice = input("\nEnter Selection: ")
        
        if choice == '1': req_selection_recent_recruiters()
        elif choice == '2': req_projection_active_participants()
        elif choice == '3': req_aggregate_sum_revenue()
        elif choice == '4': req_aggregate_max_min_revenue()
        elif choice == '5': req_search_participant()
        elif choice == '6': report_manager_performance()
        elif choice == '7': report_revenue_breakdown()
        elif choice == '8': mod_insert_recruit()
        elif choice == '9': mod_update_tier()
        elif choice == '10': mod_delete_member()
        elif choice == '0': break
        else: print("Invalid option.")

if __name__ == "__main__":
    # Validate connection before starting
    if get_db_connection():
        main_menu()
    else:
        print("System Start Failed.")