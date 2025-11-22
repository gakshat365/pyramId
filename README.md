# VoughDB - Database Management System

A GUI-based database management application for Vought International's pyramid scheme system, built with Python and MySQL.

## Features

- **Dual Theme Support**: Dark and light modes with custom color schemes
- **Parameterized Queries**: 17 pre-built queries across multiple categories
- **Database Reset**: One-click database initialization with sample data
- **Interactive Results**: Gridded table view with collapsible query categories

## Supported Queries

| Query | Description |
|-------|-------------|
| **Members by Tier & Time Period** | Filter members by tier level and join date range |
| **Active Participant Names & Contacts** | View all active participants with basic details |
| **Total Revenue by Tier & Year** | Calculate total revenue for a specific tier and year |
| **Highest Revenue Member by Tier & Period** | Find top earning member in tier and date range |
| **Lowest Revenue Member by Tier & Period** | Find lowest earning member in tier and date range |
| **Members Recruited in Time Range** | List all members recruited between two dates |
| **Search Participants by Name** | Find participants by first or last name pattern |
| **View All Members** | Display complete member roster with details |
| **View Orphaned Members** | Show members without recruiters (tier 2+) |
| **View All Recruitment Events** | Display recruitment history with methods |
| **View All Transactions** | Show financial transaction records |
| **Recruitment Count per Manager** | Count recruits per manager in date range |
| **Transaction Value per Finance Manager** | Sum transaction values by finance manager |
| **Revenue Breakdown by Tier & Recruit Count** | Analyze revenue distribution across tiers |
| **Insert New Member** | Add new member with tier and recruiter |
| **Record Recruitment Event** | Log a new recruitment with method details |
| **Delete Member** | Remove member from database |

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. **Configure Database** (`src/db_config.py`):
   - Update MySQL credentials (host, user, password)

2. **Initialize Database**:
   - Run the app and click **Start/Reset** button, or
   - Manually execute:
     - `src/schema.sql` - Creates VoughDB database and 12 tables
     - `src/populate.sql` - Loads sample data (147 members across 7 universes)

3. **Run Application** (`src/main_app.py`):
   ```bash
   cd src
   python main_app.py
   ```

## Database Schema

The system tracks:
- Multi-universe participants and members
- Recruitment hierarchies with tier levels
- Financial transactions and investments
- Portal networks between universes
- Marketing campaigns
- Employee management

## Usage

1. Launch the application
2. Click **Start/Reset** to initialize/reset the database
3. Select queries from the sidebar
4. Input parameters when prompted
5. View results in the main panel
6. Toggle themes with ☀/🌙 button
