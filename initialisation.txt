-- Core dimension tables (no dependencies)
CREATE TABLE Universe (
    universe_id INT PRIMARY KEY AUTO_INCREMENT,
    universe_name VARCHAR(255) NOT NULL,
    first_member_id INT,
    status VARCHAR(50)
);

CREATE TABLE InvestmentTier (
    tier_id INT PRIMARY KEY AUTO_INCREMENT,
    minimum_investment DECIMAL(10, 2) NOT NULL,
    commission_rate DECIMAL(5, 2) NOT NULL,
    max_recruits_allowed INT,
    tier_benefits VARCHAR(500)
);

-- Participant table (depends on Universe)
CREATE TABLE Participant (
    participant_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    universe_id INT NOT NULL,
    planet VARCHAR(100),
    country VARCHAR(100),
    city_id INT,
    FOREIGN KEY (universe_id) REFERENCES Universe(universe_id)
);

-- Employee table (depends on Participant)
CREATE TABLE Employee (
    participant_id INT PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    access_level INT,
    hire_date DATE,
    salary DECIMAL(10, 2),
    status VARCHAR(50),
    FOREIGN KEY (participant_id) REFERENCES Participant(participant_id) ON DELETE CASCADE
);




-- Member table (depends on Participant and InvestmentTier)
CREATE TABLE Member (
    participant_id INT PRIMARY KEY,
    tier_level INT NOT NULL,
    join_date DATE,
    status VARCHAR(50),
    recruiter_id INT,
    total_recruits INT DEFAULT 0,
    FOREIGN KEY (participant_id) REFERENCES Participant(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (tier_level) REFERENCES InvestmentTier(tier_id),
    FOREIGN KEY (recruiter_id) REFERENCES Member(participant_id)
);

-- Portals table (depends on Universe and Employee)
CREATE TABLE Portals (
    portal_id INT PRIMARY KEY AUTO_INCREMENT,
    source_universe_id INT NOT NULL,
    target_universe_id INT NOT NULL,
    engineer_id INT NOT NULL,
    status VARCHAR(50),
    cost DECIMAL(10, 2),
    FOREIGN KEY (source_universe_id) REFERENCES Universe(universe_id),
    FOREIGN KEY (target_universe_id) REFERENCES Universe(universe_id),
    FOREIGN KEY (engineer_id) REFERENCES Employee(participant_id)
);

-- Portal Calibration table (depends on Portals and Employee)
CREATE TABLE PortalCalibration (
    portal_id INT NOT NULL,
    calibration_code VARCHAR(100),
    engineer_id INT NOT NULL,
    calibration_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (portal_id, calibration_code),
    FOREIGN KEY (portal_id) REFERENCES Portals(portal_id),
    FOREIGN KEY (engineer_id) REFERENCES Employee(participant_id)
);







-- Transaction table (depends on Member)
CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    from_member_id INT NOT NULL,
    to_member_id INT NOT NULL,
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (from_member_id) REFERENCES Member(participant_id),
    FOREIGN KEY (to_member_id) REFERENCES Member(participant_id)
);

-- Recruitment Event table (depends on Member)
CREATE TABLE RecruitmentEvent (
    recruiter_id INT NOT NULL,
    recruit_id INT NOT NULL,
    recruitment_date DATE,
    recruitment_method VARCHAR(100),
    PRIMARY KEY (recruiter_id, recruit_id),
    FOREIGN KEY (recruiter_id) REFERENCES Member(participant_id),
    FOREIGN KEY (recruit_id) REFERENCES Member(participant_id)
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
    FOREIGN KEY (program_id) REFERENCES MarketingCampaign(program_id),
    FOREIGN KEY (members_involved) REFERENCES Member(participant_id)
);







CREATE TABLE MarketingCampaignAdditional (
    program_code VARCHAR(50) PRIMARY KEY,
    universe_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    budget DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (program_code) REFERENCES MarketingCampaign(program_code),
    FOREIGN KEY (universe_id) REFERENCES Universe(universe_id)
);

-- Update Universe table with first_member_id foreign key
ALTER TABLE Universe
ADD CONSTRAINT fk_universe_first_member
FOREIGN KEY (first_member_id) REFERENCES Member(participant_id);



