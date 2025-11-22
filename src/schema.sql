DROP DATABASE IF EXISTS VoughtDB;
CREATE DATABASE VoughtDB;
USE VoughtDB;


-- Core dimension tables (no dependencies)
CREATE TABLE Universe (
    universe_id INT PRIMARY KEY AUTO_INCREMENT,
    universe_name VARCHAR(255) NOT NULL UNIQUE,
    first_member_id INT,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
CONSTRAINT chk_universe_status CHECK (status IN ('active', 'inactive', 'quarantined'))  
);

CREATE TABLE InvestmentTier (
    tier_id INT PRIMARY KEY AUTO_INCREMENT,
    minimum_investment DECIMAL(10, 2) NOT NULL,
    commission_rate DECIMAL(5, 2) NOT NULL,
    max_recruits_allowed INT NOT NULL DEFAULT 7,
    tier_benefits VARCHAR(500)
);

-- Participant table (depends on Universe)
CREATE TABLE Participant (
    participant_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    universe_id INT NOT NULL,
    planet VARCHAR(100) NOT NULL DEFAULT 'Earth',
    country VARCHAR(100) NOT NULL,
    city_id INT,
    FOREIGN KEY (universe_id) REFERENCES Universe(universe_id) ON UPDATE CASCADE ON DELETE CASCADE
);
-- Employee table (depends on Participant)
CREATE TABLE Employee (
    participant_id INT PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    access_level INT NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    CHECK (salary > 0),
    CHECK (status IN ('active', 'on_leave', 'terminated')),
    FOREIGN KEY (participant_id) REFERENCES Participant(participant_id) ON DELETE CASCADE
);






-- Member table (depends on Participant and InvestmentTier)
CREATE TABLE Member (
    participant_id INT PRIMARY KEY,
    tier_level INT NOT NULL,
    join_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    recruiter_id INT, -- Nullable to allow SET NULL
    total_recruits INT DEFAULT 0,
    CHECK (status IN ('active', 'suspended', 'terminated')),
    
    FOREIGN KEY (participant_id) REFERENCES Participant(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
        
    FOREIGN KEY (tier_level) REFERENCES InvestmentTier(tier_id) 
        ON UPDATE CASCADE,
        
    FOREIGN KEY (recruiter_id) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL -- If recruiter leaves, recruit stays but has no recruiter
);

-- Portals table (depends on Universe and Employee)
CREATE TABLE Portals (
    portal_id INT PRIMARY KEY AUTO_INCREMENT,
    source_universe_id INT NOT NULL,
    target_universe_id INT NOT NULL,
    engineer_id INT, -- Nullable to allow SET NULL
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    CHECK (status IN ('active', 'maintenance', 'closed')),
    
    FOREIGN KEY (source_universe_id) REFERENCES Universe(universe_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
        
    FOREIGN KEY (target_universe_id) REFERENCES Universe(universe_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
        
    FOREIGN KEY (engineer_id) REFERENCES Employee(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL -- If engineer is fired, portal record remains
);

-- Portal Calibration table (depends on Portals and Employee)
CREATE TABLE PortalCalibration (
    portal_id INT NOT NULL,
    calibration_code VARCHAR(100) NOT NULL,
    engineer_id INT, -- Nullable
    calibration_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (portal_id, calibration_code),
    FOREIGN KEY (portal_id) REFERENCES Portals(portal_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE, -- If portal is removed, calibrations are irrelevant
        
    FOREIGN KEY (engineer_id) REFERENCES Employee(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL
);







-- Transaction table (depends on Member)
CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    from_member_id INT, -- Nullable to keep history even if member deleted
    to_member_id INT,   -- Nullable
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'completed',
    CHECK (status IN ('pending', 'completed', 'failed')),
    
    FOREIGN KEY (from_member_id) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL, -- Keep financial record even if member is deleted
        
    FOREIGN KEY (to_member_id) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL
);

-- Recruitment Event table (depends on Member)
CREATE TABLE RecruitmentEvent (
    recruiter_id INT, -- Nullable
    recruit_id INT NOT NULL,
    recruitment_date DATE NOT NULL,
    recruitment_method VARCHAR(100),
    
    PRIMARY KEY (recruit_id),
    
    FOREIGN KEY (recruiter_id) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL, -- History remains if recruiter is deleted
        
    FOREIGN KEY (recruit_id) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

-- Marketing Campaign tables
CREATE TABLE MarketingCampaign (
    program_id INT PRIMARY KEY AUTO_INCREMENT,
    program_code VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE MarketingCampaign_MembersInvolved (
    program_id INT NOT NULL,
    members_involved INT NOT NULL,
    PRIMARY KEY (program_id,members_involved),
    FOREIGN KEY (program_id) REFERENCES MarketingCampaign(program_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
        
    FOREIGN KEY (members_involved) REFERENCES Member(participant_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);







CREATE TABLE MarketingCampaignAdditional (
    program_code VARCHAR(50) PRIMARY KEY,
    universe_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    budget DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'planned',
    CHECK (status IN ('planned', 'active', 'paused', 'completed', 'ended')),
    
    FOREIGN KEY (program_code) REFERENCES MarketingCampaign(program_code) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
        
    FOREIGN KEY (universe_id) REFERENCES Universe(universe_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

-- Update Universe table with first_member_id foreign key
ALTER TABLE Universe
ADD CONSTRAINT fk_universe_first_member
FOREIGN KEY (first_member_id) REFERENCES Member(participant_id)
ON UPDATE CASCADE
ON DELETE SET NULL; -- If the first member quits, the Universe table doesn't break
