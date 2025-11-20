USE VoughDB;

-- Disable foreign key checks temporarily for easier insertion
SET FOREIGN_KEY_CHECKS = 0;

-- Clear existing data (in reverse order of dependencies)
TRUNCATE TABLE MarketingCampaignAdditional;
TRUNCATE TABLE MarketingCampaign_MembersInvolved;
TRUNCATE TABLE MarketingCampaign;
TRUNCATE TABLE RecruitmentEvent;
TRUNCATE TABLE Transaction;
TRUNCATE TABLE PortalCalibration;
TRUNCATE TABLE Portals;
TRUNCATE TABLE Member;
TRUNCATE TABLE Employee;
TRUNCATE TABLE Participant;
TRUNCATE TABLE InvestmentTier;
TRUNCATE TABLE Universe;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- STEP 1: Insert Investment Tiers (Highest to Lowest: 1-7)
-- =====================================================
INSERT INTO InvestmentTier (tier_id, minimum_investment, commission_rate, max_recruits_allowed, tier_benefits) VALUES
(1, 100000.00, 25.00, 7, 'Diamond Tier: Exclusive access to multiversal summits, 25% commission on all downline'),
(2, 50000.00, 20.00, 7, 'Platinum Tier: Priority portal access, 20% commission rate'),
(3, 25000.00, 15.00, 7, 'Gold Tier: Enhanced recruitment bonuses, 15% commission rate'),
(4, 10000.00, 12.00, 7, 'Silver Tier: Standard benefits package, 12% commission rate'),
(5, 5000.00, 10.00, 7, 'Bronze Tier: Basic recruitment tools, 10% commission rate'),
(6, 2500.00, 8.00, 7, 'Copper Tier: Entry-level benefits, 8% commission rate'),
(7, 1000.00, 5.00, 7, 'Iron Tier: Starter package, 5% commission rate');

-- =====================================================
-- STEP 2: Insert Universes (7 Universes from Phase 1)
-- =====================================================
INSERT INTO Universe (universe_id, universe_name, first_member_id, status) VALUES
(1, 'Friends Universe', NULL, 'active'),
(2, 'The Big Bang Theory Universe', NULL, 'active'),
(3, 'Breaking Bad Universe', NULL, 'active'),
(4, 'Harry Potter Universe', NULL, 'active'),
(5, 'Family Guy Universe', NULL, 'active'),
(6, 'Marvel Cinematic Universe', NULL, 'active'),
(7, 'Invincible Universe', NULL, 'active');

-- =====================================================
-- STEP 3: Insert Tier 1 Members (7 Founding Members - 1 per Universe)
-- =====================================================

-- Universe 1: Friends - Joey Tribbiani
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(1, 'Joey', 'Tribbiani', '1968-01-09', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(1, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 2: Big Bang Theory - Rajesh Koothrappali
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(2, 'Rajesh', 'Koothrappali', '1981-10-06', 2, 'Earth', 'India', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(2, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 3: Breaking Bad - Hank Schrader
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(3, 'Hank', 'Schrader', '1966-03-17', 3, 'Earth', 'USA', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(3, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 4: Harry Potter - Neville Longbottom
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(4, 'Neville', 'Longbottom', '1980-07-30', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(4, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 5: Family Guy - Peter Griffin
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(5, 'Peter', 'Griffin', '1966-09-15', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(5, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 6: Marvel - Thor
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(6, 'Thor', 'Odinson', '964-01-01', 6, 'Asgard', 'Asgard', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(6, 1, '2023-01-15', 'active', NULL, 4);

-- Universe 7: Invincible - Immortal
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(7, 'Abraham', 'Lincoln', '1809-02-12', 7, 'Earth', 'USA', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(7, 1, '2023-01-15', 'active', NULL, 4);

-- =====================================================
-- STEP 4: Update Universe table with first_member_id
-- =====================================================
UPDATE Universe SET first_member_id = 1 WHERE universe_id = 1;
UPDATE Universe SET first_member_id = 2 WHERE universe_id = 2;
UPDATE Universe SET first_member_id = 3 WHERE universe_id = 3;
UPDATE Universe SET first_member_id = 4 WHERE universe_id = 4;
UPDATE Universe SET first_member_id = 5 WHERE universe_id = 5;
UPDATE Universe SET first_member_id = 6 WHERE universe_id = 6;
UPDATE Universe SET first_member_id = 7 WHERE universe_id = 7;

-- =====================================================
-- STEP 5: Insert Tier 2 Members (28 Members - 4 per Tier 1 Member)
-- =====================================================

-- Joey's Recruits (Friends Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(8, 'Chandler', 'Bing', '1968-04-08', 1, 'Earth', 'USA', 1),
(9, 'Ross', 'Geller', '1967-10-18', 1, 'Earth', 'USA', 1),
(10, 'Monica', 'Geller', '1969-03-22', 1, 'Earth', 'USA', 1),
(11, 'Phoebe', 'Buffay', '1968-02-16', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(8, 2, '2023-03-01', 'active', 1, 4),
(9, 2, '2023-03-05', 'active', 1, 4),
(10, 2, '2023-03-10', 'active', 1, 4),
(11, 2, '2023-03-15', 'active', 1, 4);

-- Rajesh's Recruits (Big Bang Theory Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(12, 'Sheldon', 'Cooper', '1980-02-26', 2, 'Earth', 'USA', 2),
(13, 'Leonard', 'Hofstadter', '1980-05-17', 2, 'Earth', 'USA', 2),
(14, 'Howard', 'Wolowitz', '1981-03-01', 2, 'Earth', 'USA', 2),
(15, 'Bernadette', 'Rostenkowski', '1984-12-12', 2, 'Earth', 'USA', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(12, 2, '2023-03-01', 'active', 2, 4),
(13, 2, '2023-03-05', 'active', 2, 4),
(14, 2, '2023-03-10', 'active', 2, 4),
(15, 2, '2023-03-15', 'active', 2, 4);

-- Hank's Recruits (Breaking Bad Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(16, 'Walter', 'White', '1958-09-07', 3, 'Earth', 'USA', 3),
(17, 'Jesse', 'Pinkman', '1984-09-24', 3, 'Earth', 'USA', 3),
(18, 'Skyler', 'White', '1970-08-11', 3, 'Earth', 'USA', 3),
(19, 'Saul', 'Goodman', '1960-11-12', 3, 'Earth', 'USA', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(16, 2, '2023-03-01', 'active', 3, 4),
(17, 2, '2023-03-05', 'active', 3, 4),
(18, 2, '2023-03-10', 'active', 3, 4),
(19, 2, '2023-03-15', 'active', 3, 4);

-- Neville's Recruits (Harry Potter Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(20, 'Harry', 'Potter', '1980-07-31', 4, 'Earth', 'United Kingdom', 4),
(21, 'Hermione', 'Granger', '1979-09-19', 4, 'Earth', 'United Kingdom', 4),
(22, 'Ron', 'Weasley', '1980-03-01', 4, 'Earth', 'United Kingdom', 4),
(23, 'Luna', 'Lovegood', '1981-02-13', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(20, 2, '2023-03-01', 'active', 4, 4),
(21, 2, '2023-03-05', 'active', 4, 4),
(22, 2, '2023-03-10', 'active', 4, 4),
(23, 2, '2023-03-15', 'active', 4, 4);

-- Peter's Recruits (Family Guy Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(24, 'Lois', 'Griffin', '1968-02-18', 5, 'Earth', 'USA', 5),
(25, 'Glenn', 'Quagmire', '1948-03-25', 5, 'Earth', 'USA', 5),
(26, 'Cleveland', 'Brown', '1966-02-07', 5, 'Earth', 'USA', 5),
(27, 'Joe', 'Swanson', '1963-11-17', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(24, 2, '2023-03-01', 'active', 5, 4),
(25, 2, '2023-03-05', 'active', 5, 4),
(26, 2, '2023-03-10', 'active', 5, 4),
(27, 2, '2023-03-15', 'active', 5, 4);

-- Thor's Recruits (Marvel Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(28, 'Loki', 'Laufeyson', '965-01-01', 6, 'Jotunheim', 'Asgard', 6),
(29, 'Tony', 'Stark', '1970-05-29', 6, 'Earth', 'USA', 6),
(30, 'Steve', 'Rogers', '1918-07-04', 6, 'Earth', 'USA', 6),
(31, 'Natasha', 'Romanoff', '1984-11-22', 6, 'Earth', 'Russia', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(28, 2, '2023-03-01', 'active', 6, 4),
(29, 2, '2023-03-05', 'active', 6, 4),
(30, 2, '2023-03-10', 'active', 6, 4),
(31, 2, '2023-03-15', 'active', 6, 4);

-- Immortal's Recruits (Invincible Universe) - 4 members
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(32, 'Mark', 'Grayson', '2001-03-19', 7, 'Earth', 'USA', 7),
(33, 'Nolan', 'Grayson', '1982-06-15', 7, 'Viltrum', 'Viltrum Empire', 7),
(34, 'Debbie', 'Grayson', '1975-08-22', 7, 'Earth', 'USA', 7),
(35, 'Atom', 'Eve', '2001-07-29', 7, 'Earth', 'USA', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(32, 2, '2023-03-01', 'active', 7, 4),
(33, 2, '2023-03-05', 'active', 7, 4),
(34, 2, '2023-03-10', 'active', 7, 4),
(35, 2, '2023-03-15', 'active', 7, 4);

-- =====================================================
-- STEP 6: Insert Tier 3 Members (112 Members - 4 per Tier 2 Member)
-- =====================================================

-- Chandler's Recruits (Friends Universe - Tier 3) - participant_id 36-39
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(36, 'Janice', 'Hosenstein', '1969-05-12', 1, 'Earth', 'USA', 1),
(37, 'Richard', 'Burke', '1950-11-20', 1, 'Earth', 'USA', 1),
(38, 'Mike', 'Hannigan', '1968-08-30', 1, 'Earth', 'USA', 1),
(39, 'Gunther', 'Central-Perk', '1962-03-10', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(36, 3, '2023-06-01', 'active', 8, 0),
(37, 3, '2023-06-10', 'active', 8, 0),
(38, 3, '2023-06-20', 'active', 8, 0),
(39, 3, '2023-07-01', 'active', 8, 0);

-- Ross's Recruits (Friends Universe - Tier 3) - participant_id 40-43
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(40, 'Rachel', 'Green', '1969-05-05', 1, 'Earth', 'USA', 1),
(41, 'Emily', 'Waltham', '1970-02-14', 1, 'Earth', 'United Kingdom', 1),
(42, 'Carol', 'Willick', '1965-07-19', 1, 'Earth', 'USA', 1),
(43, 'Julie', 'Johnson', '1968-11-28', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(40, 3, '2023-06-05', 'active', 9, 0),
(41, 3, '2023-06-15', 'active', 9, 0),
(42, 3, '2023-06-25', 'active', 9, 0),
(43, 3, '2023-07-05', 'active', 9, 0);

-- Monica's Recruits (Friends Universe - Tier 3) - participant_id 44-47
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(44, 'Paul', 'Stevens', '1948-09-22', 1, 'Earth', 'USA', 1),
(45, 'Pete', 'Becker', '1965-04-15', 1, 'Earth', 'USA', 1),
(46, 'Fun Bobby', 'Reynolds', '1967-06-30', 1, 'Earth', 'USA', 1),
(47, 'Tommy', 'Martinez', '1969-12-08', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(44, 3, '2023-07-10', 'active', 10, 0),
(45, 3, '2023-07-20', 'active', 10, 0),
(46, 3, '2023-08-01', 'active', 10, 0),
(47, 3, '2023-08-10', 'active', 10, 0);

-- Phoebe's Recruits (Friends Universe - Tier 3) - participant_id 48-51
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(48, 'David', 'Scientist', '1966-10-12', 1, 'Earth', 'USA', 1),
(49, 'Ursula', 'Buffay', '1968-02-16', 1, 'Earth', 'USA', 1),
(50, 'Gary', 'Officer', '1960-08-04', 1, 'Earth', 'USA', 1),
(51, 'Ryan', 'Navy', '1972-01-29', 1, 'Earth', 'USA', 1);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(48, 3, '2023-08-15', 'active', 11, 0),
(49, 3, '2023-08-25', 'active', 11, 0),
(50, 3, '2023-09-05', 'active', 11, 0),
(51, 3, '2023-09-15', 'active', 11, 0);

-- Sheldon's Recruits (Big Bang Theory Universe - Tier 3) - participant_id 52-55
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(52, 'Amy', 'Farrah Fowler', '1979-12-17', 2, 'Earth', 'USA', 2),
(53, 'Stuart', 'Bloom', '1981-05-21', 2, 'Earth', 'USA', 2),
(54, 'Barry', 'Kripke', '1980-11-30', 2, 'Earth', 'USA', 2),
(55, 'Leslie', 'Winkle', '1981-03-14', 2, 'Earth', 'USA', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(52, 3, '2023-09-20', 'active', 12, 0),
(53, 3, '2023-10-01', 'active', 12, 0),
(54, 3, '2023-10-15', 'active', 12, 0),
(55, 3, '2023-11-01', 'active', 12, 0);

-- Leonard's Recruits (Big Bang Theory Universe - Tier 3) - participant_id 56-59
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(56, 'Penny', 'Hofstadter', '1985-11-30', 2, 'Earth', 'USA', 2),
(57, 'Priya', 'Koothrappali', '1983-09-18', 2, 'Earth', 'India', 2),
(58, 'Stephanie', 'Barnett', '1982-06-25', 2, 'Earth', 'USA', 2),
(59, 'Joyce', 'Kim', '1981-04-07', 2, 'Earth', 'USA', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(56, 3, '2023-11-10', 'active', 13, 0),
(57, 3, '2023-11-20', 'active', 13, 0),
(58, 3, '2023-12-01', 'active', 13, 0),
(59, 3, '2023-12-15', 'active', 13, 0);

-- Howard's Recruits (Big Bang Theory Universe - Tier 3) - participant_id 60-63
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(60, 'Debbie', 'Wolowitz', '1952-03-10', 2, 'Earth', 'USA', 2),
(61, 'Christy', 'Vanderbel', '1982-07-22', 2, 'Earth', 'USA', 2),
(62, 'Emily', 'Sweeney', '1985-01-16', 2, 'Earth', 'USA', 2),
(63, 'Dmitri', 'Rezinov', '1975-09-05', 2, 'Earth', 'Russia', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(60, 3, '2024-01-05', 'active', 14, 0),
(61, 3, '2024-01-15', 'active', 14, 0),
(62, 3, '2024-01-25', 'active', 14, 0),
(63, 3, '2024-02-05', 'active', 14, 0);

-- Bernadette's Recruits (Big Bang Theory Universe - Tier 3) - participant_id 64-67
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(64, 'Dan', 'Rostenkowski', '1950-08-12', 2, 'Earth', 'USA', 2),
(65, 'Mike', 'Rostenkowski', '1955-11-03', 2, 'Earth', 'USA', 2),
(66, 'Glenn', 'Childs', '1978-05-19', 2, 'Earth', 'USA', 2),
(67, 'Marissa', 'Johnson', '1983-02-28', 2, 'Earth', 'USA', 2);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(64, 3, '2024-02-10', 'active', 15, 0),
(65, 3, '2024-02-20', 'active', 15, 0),
(66, 3, '2025-01-15', 'active', 15, 0),
(67, 3, '2025-06-10', 'active', 15, 0);

-- Walter's Recruits (Breaking Bad Universe - Tier 3) - participant_id 68-71
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(68, 'Walter', 'White Jr', '1993-07-08', 3, 'Earth', 'USA', 3),
(69, 'Gus', 'Fring', '1958-04-26', 3, 'Earth', 'Chile', 3),
(70, 'Mike', 'Ehrmantraut', '1944-09-05', 3, 'Earth', 'USA', 3),
(71, 'Lydia', 'Rodarte-Quayle', '1978-11-14', 3, 'Earth', 'USA', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(68, 3, '2025-01-15', 'active', 16, 0),
(69, 3, '2024-05-01', 'active', 16, 0),
(70, 3, '2025-06-10', 'active', 16, 0),
(71, 3, '2024-07-05', 'active', 16, 0);

-- Jesse's Recruits (Breaking Bad Universe - Tier 3) - participant_id 72-75
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(72, 'Badger', 'Mayhew', '1984-06-18', 3, 'Earth', 'USA', 3),
(73, 'Skinny', 'Pete', '1983-12-07', 3, 'Earth', 'USA', 3),
(74, 'Jane', 'Margolis', '1982-04-15', 3, 'Earth', 'USA', 3),
(75, 'Andrea', 'Cantillo', '1984-10-22', 3, 'Earth', 'USA', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(72, 3, '2025-01-15', 'active', 17, 0),
(73, 3, '2024-05-01', 'active', 17, 0),
(74, 3, '2025-06-10', 'active', 17, 0),
(75, 3, '2024-07-05', 'active', 17, 0);

-- Skyler's Recruits (Breaking Bad Universe - Tier 3) - participant_id 76-79
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(76, 'Marie', 'Schrader', '1968-08-15', 3, 'Earth', 'USA', 3),
(77, 'Ted', 'Beneke', '1965-03-22', 3, 'Earth', 'USA', 3),
(78, 'Francesca', 'Liddy', '1975-11-09', 3, 'Earth', 'USA', 3),
(79, 'Huell', 'Babineaux', '1970-07-27', 3, 'Earth', 'USA', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(76, 3, '2025-01-15', 'active', 18, 0),
(77, 3, '2024-05-01', 'active', 18, 0),
(78, 3, '2025-06-10', 'active', 18, 0),
(79, 3, '2024-07-05', 'active', 18, 0);

-- Saul's Recruits (Breaking Bad Universe - Tier 3) - participant_id 80-83
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(80, 'Kim', 'Wexler', '1968-02-13', 3, 'Earth', 'USA', 3),
(81, 'Chuck', 'McGill', '1944-01-08', 3, 'Earth', 'USA', 3),
(82, 'Nacho', 'Varga', '1983-05-19', 3, 'Earth', 'USA', 3),
(83, 'Lalo', 'Salamanca', '1974-09-30', 3, 'Earth', 'Mexico', 3);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(80, 3, '2025-01-15', 'active', 19, 0),
(81, 3, '2024-05-01', 'active', 19, 0),
(82, 3, '2025-06-10', 'active', 19, 0),
(83, 3, '2024-07-05', 'active', 19, 0);

-- Harry's Recruits (Harry Potter Universe - Tier 3) - participant_id 84-87
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(84, 'Ginny', 'Weasley', '1981-08-11', 4, 'Earth', 'United Kingdom', 4),
(85, 'Cho', 'Chang', '1979-04-07', 4, 'Earth', 'United Kingdom', 4),
(86, 'Cedric', 'Diggory', '1977-09-30', 4, 'Earth', 'United Kingdom', 4),
(87, 'Dean', 'Thomas', '1980-06-27', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(84, 3, '2025-01-15', 'active', 20, 0),
(85, 3, '2024-05-01', 'active', 20, 0),
(86, 3, '2025-06-10', 'active', 20, 0),
(87, 3, '2024-07-05', 'active', 20, 0);

-- Hermione's Recruits (Harry Potter Universe - Tier 3) - participant_id 88-91
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(88, 'Viktor', 'Krum', '1976-08-15', 4, 'Earth', 'Bulgaria', 4),
(89, 'Cormac', 'McLaggen', '1979-11-22', 4, 'Earth', 'United Kingdom', 4),
(90, 'Lavender', 'Brown', '1980-04-03', 4, 'Earth', 'United Kingdom', 4),
(91, 'Parvati', 'Patil', '1980-09-19', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(88, 3, '2025-01-15', 'active', 21, 0),
(89, 3, '2024-05-01', 'active', 21, 0),
(90, 3, '2025-06-10', 'active', 21, 0),
(91, 3, '2024-07-05', 'active', 21, 0);

-- Ron's Recruits (Harry Potter Universe - Tier 3) - participant_id 92-95
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(92, 'Fred', 'Weasley', '1978-04-01', 4, 'Earth', 'United Kingdom', 4),
(93, 'George', 'Weasley', '1978-04-01', 4, 'Earth', 'United Kingdom', 4),
(94, 'Percy', 'Weasley', '1976-08-22', 4, 'Earth', 'United Kingdom', 4),
(95, 'Bill', 'Weasley', '1970-11-29', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(92, 3, '2025-01-15', 'active', 22, 0),
(93, 3, '2024-05-01', 'active', 22, 0),
(94, 3, '2025-06-10', 'active', 22, 0),
(95, 3, '2024-07-05', 'active', 22, 0);

-- Luna's Recruits (Harry Potter Universe - Tier 3) - participant_id 96-99
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(96, 'Seamus', 'Finnigan', '1980-07-12', 4, 'Earth', 'Ireland', 4),
(97, 'Colin', 'Creevey', '1981-05-20', 4, 'Earth', 'United Kingdom', 4),
(98, 'Dennis', 'Creevey', '1983-09-01', 4, 'Earth', 'United Kingdom', 4),
(99, 'Ernie', 'Macmillan', '1980-02-17', 4, 'Earth', 'United Kingdom', 4);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(96, 3, '2025-01-15', 'active', 23, 0),
(97, 3, '2024-05-01', 'active', 23, 0),
(98, 3, '2025-06-10', 'active', 23, 0),
(99, 3, '2024-07-05', 'active', 23, 0);

-- Lois's Recruits (Family Guy Universe - Tier 3) - participant_id 100-103
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(100, 'Meg', 'Griffin', '1983-03-23', 5, 'Earth', 'USA', 5),
(101, 'Chris', 'Griffin', '1985-10-25', 5, 'Earth', 'USA', 5),
(102, 'Stewie', 'Griffin', '2005-09-11', 5, 'Earth', 'USA', 5),
(103, 'Brian', 'Griffin', '1999-04-19', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(100, 3, '2025-01-15', 'active', 24, 0),
(101, 3, '2024-05-01', 'active', 24, 0),
(102, 3, '2025-06-10', 'active', 24, 0),
(103, 3, '2024-07-05', 'active', 24, 0);

-- Quagmire's Recruits (Family Guy Universe - Tier 3) - participant_id 104-107
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(104, 'Ida', 'Davis', '1946-12-15', 5, 'Earth', 'USA', 5),
(105, 'Jillian', 'Russell', '1982-06-08', 5, 'Earth', 'USA', 5),
(106, 'Cheryl', 'Tiegs', '1947-09-25', 5, 'Earth', 'USA', 5),
(107, 'Joan', 'Quagmire', '1930-01-10', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(104, 3, '2025-01-15', 'active', 25, 0),
(105, 3, '2024-05-01', 'active', 25, 0),
(106, 3, '2025-06-10', 'active', 25, 0),
(107, 3, '2024-07-05', 'active', 25, 0);

-- Cleveland's Recruits (Family Guy Universe - Tier 3) - participant_id 108-111
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(108, 'Donna', 'Tubbs', '1968-07-29', 5, 'Earth', 'USA', 5),
(109, 'Loretta', 'Brown', '1965-05-16', 5, 'Earth', 'USA', 5),
(110, 'Rallo', 'Tubbs', '2005-12-04', 5, 'Earth', 'USA', 5),
(111, 'Roberta', 'Tubbs', '1991-02-20', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(108, 3, '2025-01-15', 'active', 26, 0),
(109, 3, '2024-05-01', 'active', 26, 0),
(110, 3, '2025-06-10', 'active', 26, 0),
(111, 3, '2024-07-05', 'active', 26, 0);

-- Joe's Recruits (Family Guy Universe - Tier 3) - participant_id 112-115
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(112, 'Bonnie', 'Swanson', '1964-08-18', 5, 'Earth', 'USA', 5),
(113, 'Kevin', 'Swanson', '1988-11-07', 5, 'Earth', 'USA', 5),
(114, 'Susie', 'Swanson', '2005-04-20', 5, 'Earth', 'USA', 5),
(115, 'Joe', 'Swanson Jr', '2006-01-25', 5, 'Earth', 'USA', 5);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(112, 3, '2025-01-15', 'active', 27, 0),
(113, 3, '2024-05-01', 'active', 27, 0),
(114, 3, '2025-06-10', 'active', 27, 0),
(115, 3, '2024-07-05', 'active', 27, 0);

-- Loki's Recruits (Marvel Universe - Tier 3) - participant_id 116-119
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(116, 'Sylvie', 'Laufeydottir', '982-06-15', 6, 'Asgard', 'Asgard', 6),
(117, 'Mobius', 'Mobius', '1975-03-20', 6, 'Earth', 'USA', 6),
(118, 'Hela', 'Odinsdottir', '800-10-01', 6, 'Hel', 'Asgard', 6),
(119, 'Valkyrie', 'Brunnhilde', '1000-05-12', 6, 'Asgard', 'Asgard', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(116, 3, '2025-01-15', 'active', 28, 0),
(117, 3, '2024-05-01', 'active', 28, 0),
(118, 3, '2025-06-10', 'active', 28, 0),
(119, 3, '2024-07-05', 'active', 28, 0);

-- Tony's Recruits (Marvel Universe - Tier 3) - participant_id 120-123
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(120, 'Pepper', 'Potts', '1974-02-14', 6, 'Earth', 'USA', 6),
(121, 'James', 'Rhodes', '1968-10-06', 6, 'Earth', 'USA', 6),
(122, 'Happy', 'Hogan', '1969-07-30', 6, 'Earth', 'USA', 6),
(123, 'Obadiah', 'Stane', '1950-04-15', 6, 'Earth', 'USA', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(120, 3, '2025-01-15', 'active', 29, 0),
(121, 3, '2024-05-01', 'active', 29, 0),
(122, 3, '2025-06-10', 'active', 29, 0),
(123, 3, '2024-07-05', 'active', 29, 0);

-- Steve's Recruits (Marvel Universe - Tier 3) - participant_id 124-127
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(124, 'Bucky', 'Barnes', '1917-03-10', 6, 'Earth', 'USA', 6),
(125, 'Sam', 'Wilson', '1978-09-23', 6, 'Earth', 'USA', 6),
(126, 'Peggy', 'Carter', '1921-04-09', 6, 'Earth', 'United Kingdom', 6),
(127, 'Sharon', 'Carter', '1985-08-16', 6, 'Earth', 'USA', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(124, 3, '2025-01-15', 'active', 30, 0),
(125, 3, '2024-05-01', 'active', 30, 0),
(126, 3, '2025-06-10', 'active', 30, 0),
(127, 3, '2024-07-05', 'active', 30, 0);

-- Natasha's Recruits (Marvel Universe - Tier 3) - participant_id 128-131
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(128, 'Clint', 'Barton', '1971-01-07', 6, 'Earth', 'USA', 6),
(129, 'Yelena', 'Belova', '1988-03-22', 6, 'Earth', 'Russia', 6),
(130, 'Alexei', 'Shostakov', '1954-11-19', 6, 'Earth', 'Russia', 6),
(131, 'Melina', 'Vostokoff', '1962-06-02', 6, 'Earth', 'Russia', 6);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(128, 3, '2025-01-15', 'active', 31, 0),
(129, 3, '2024-05-01', 'active', 31, 0),
(130, 3, '2025-06-10', 'active', 31, 0),
(131, 3, '2024-07-05', 'active', 31, 0);

-- Mark's Recruits (Invincible Universe - Tier 3) - participant_id 132-135
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(132, 'William', 'Clockwell', '2001-06-18', 7, 'Earth', 'USA', 7),
(133, 'Amber', 'Bennett', '2001-11-24', 7, 'Earth', 'USA', 7),
(134, 'Rex', 'Sloan', '1995-04-08', 7, 'Earth', 'USA', 7),
(135, 'Kate', 'Cha', '1997-09-14', 7, 'Earth', 'USA', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(132, 3, '2025-01-15', 'active', 32, 0),
(133, 3, '2024-05-01', 'active', 32, 0),
(134, 3, '2025-06-10', 'active', 32, 0),
(135, 3, '2024-07-05', 'active', 32, 0);

-- Nolan's Recruits (Invincible Universe - Tier 3) - participant_id 136-139
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(136, 'Conquest', 'Viltrumite', '1200-01-01', 7, 'Viltrum', 'Viltrum Empire', 7),
(137, 'Thragg', 'Viltrumite', '800-01-01', 7, 'Viltrum', 'Viltrum Empire', 7),
(138, 'Anissa', 'Viltrumite', '1100-07-15', 7, 'Viltrum', 'Viltrum Empire', 7),
(139, 'Lucan', 'Viltrumite', '950-03-22', 7, 'Viltrum', 'Viltrum Empire', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(136, 3, '2025-01-15', 'active', 33, 0),
(137, 3, '2024-05-01', 'active', 33, 0),
(138, 3, '2025-06-10', 'active', 33, 0),
(139, 3, '2024-07-05', 'active', 33, 0);

-- Debbie's Recruits (Invincible Universe - Tier 3) - participant_id 140-143
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(140, 'Art', 'Rosebaum', '1945-05-10', 7, 'Earth', 'USA', 7),
(141, 'Cecil', 'Stedman', '1965-08-19', 7, 'Earth', 'USA', 7),
(142, 'Donald', 'Ferguson', '1972-03-25', 7, 'Earth', 'USA', 7),
(143, 'Fiona', 'Mills', '1976-11-08', 7, 'Earth', 'USA', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(140, 3, '2025-01-15', 'active', 34, 0),
(141, 3, '2024-05-01', 'active', 34, 0),
(142, 3, '2025-06-10', 'active', 34, 0),
(143, 3, '2024-07-05', 'active', 34, 0);

-- Atom Eve's Recruits (Invincible Universe - Tier 3) - participant_id 144-147
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(144, 'Robot', 'Rudy', '1998-02-14', 7, 'Earth', 'USA', 7),
(145, 'Monster Girl', 'Amanda', '1985-09-07', 7, 'Earth', 'USA', 7),
(146, 'Black Samson', 'Mark', '1980-12-20', 7, 'Earth', 'USA', 7),
(147, 'Bulletproof', 'Zandale', '1995-06-30', 7, 'Earth', 'USA', 7);

INSERT INTO Member (participant_id, tier_level, join_date, status, recruiter_id, total_recruits) VALUES
(144, 3, '2025-01-15', 'active', 35, 0),
(145, 3, '2024-05-01', 'active', 35, 0),
(146, 3, '2025-06-10', 'active', 35, 0),
(147, 3, '2024-07-05', 'active', 35, 0);

-- =====================================================
-- STEP 7: Insert Employees for Portal Management & Operations
-- =====================================================

-- Add Vought employees (not members of the pyramid)
INSERT INTO Participant (participant_id, first_name, last_name, date_of_birth, universe_id, planet, country, city_id) VALUES
(148, 'Stan', 'Edgar', '1960-05-12', 6, 'Earth', 'USA', 6),
(149, 'Sister', 'Sage', '1990-03-15', 6, 'Earth', 'USA', 6),
(150, 'Ashley', 'Barrett', '1985-11-22', 6, 'Earth', 'USA', 6),
(151, 'Madelyn', 'Stillwell', '1975-09-08', 6, 'Earth', 'USA', 6),
(152, 'Victoria', 'Neuman', '1988-04-17', 6, 'Earth', 'USA', 6),
(153, 'Adam', 'Bourke', '1982-06-25', 6, 'Earth', 'USA', 6),
(154, 'Seth', 'Reed', '1979-11-14', 6, 'Earth', 'USA', 6),
(155, 'Robert', 'Singer', '1968-03-22', 6, 'Earth', 'USA', 6),
(156, 'Alastair', 'Adana', '1985-07-19', 6, 'Earth', 'USA', 6),
(157, 'Cameron', 'Coleman', '1992-12-05', 6, 'Earth', 'USA', 6),
(158, 'Grace', 'Mallory', '1955-08-30', 6, 'Earth', 'USA', 6),
(159, 'Hugh', 'Campbell Sr', '1960-02-18', 6, 'Earth', 'USA', 6),
(160, 'Jonah', 'Vogelbaum', '1948-10-11', 6, 'Earth', 'USA', 6),
(161, 'Barbara', 'Vogelbaum', '1952-05-27', 6, 'Earth', 'USA', 6),
(162, 'Greg', 'Mallory', '1950-01-15', 6, 'Earth', 'USA', 6);

INSERT INTO Employee (participant_id, role, access_level, hire_date, salary, status) VALUES
(148, 'CEO', 1, '2010-01-01', 5000000.00, 'active'),
(149, 'Chief Strategist', 1, '2023-06-15', 2500000.00, 'active'),
(150, 'Multiversal Systems Engineer', 3, '2020-03-10', 180000.00, 'active'),
(151, 'Senior VP of Hero Management', 2, '2015-07-01', 450000.00, 'active'),
(152, 'Head of Bureau of Superhuman Affairs', 2, '2022-01-10', 350000.00, 'active'),
(153, 'Multiversal Systems Engineer', 4, '2021-05-15', 165000.00, 'active'),
(154, 'Portal Maintenance Engineer', 4, '2019-09-20', 145000.00, 'active'),
(155, 'Finance Manager', 4, '2018-03-12', 200000.00, 'active'),
(156, 'Recruitment Manager', 4, '2020-11-08', 120000.00, 'active'),
(157, 'Communications Director', 5, '2021-08-22', 95000.00, 'active'),
(158, 'Security Operations Manager', 2, '2012-04-05', 280000.00, 'active'),
(159, 'HR Administrator', 5, '2017-06-18', 85000.00, 'active'),
(160, 'Chief Scientist', 1, '2008-02-01', 650000.00, 'active'),
(161, 'Research Director', 2, '2011-09-14', 420000.00, 'active'),
(162, 'Operations Director', 2, '2013-12-20', 380000.00, 'active');

-- =====================================================
-- STEP 8: Insert Portals Between All Universe Combinations
-- Total: 42 bidirectional portals (7 universes × 6 connections each = 42)
-- =====================================================

-- Portals from Universe 1 (Friends) to all others
INSERT INTO Portals (portal_id, source_universe_id, target_universe_id, engineer_id, status, cost) VALUES
(1, 1, 2, 150, 'active', 50000.00),
(2, 1, 3, 153, 'active', 50000.00),
(3, 1, 4, 150, 'active', 50000.00),
(4, 1, 5, 154, 'active', 50000.00),
(5, 1, 6, 153, 'active', 50000.00),
(6, 1, 7, 150, 'active', 50000.00),

-- Portals from Universe 2 (Big Bang Theory) to all others
(7, 2, 1, 154, 'active', 50000.00),
(8, 2, 3, 150, 'active', 50000.00),
(9, 2, 4, 153, 'active', 50000.00),
(10, 2, 5, 154, 'active', 50000.00),
(11, 2, 6, 150, 'active', 50000.00),
(12, 2, 7, 153, 'active', 50000.00),

-- Portals from Universe 3 (Breaking Bad) to all others
(13, 3, 1, 154, 'active', 50000.00),
(14, 3, 2, 150, 'active', 50000.00),
(15, 3, 4, 153, 'active', 50000.00),
(16, 3, 5, 154, 'active', 50000.00),
(17, 3, 6, 150, 'active', 50000.00),
(18, 3, 7, 153, 'active', 50000.00),

-- Portals from Universe 4 (Harry Potter) to all others
(19, 4, 1, 154, 'active', 50000.00),
(20, 4, 2, 153, 'active', 50000.00),
(21, 4, 3, 150, 'active', 50000.00),
(22, 4, 5, 154, 'active', 50000.00),
(23, 4, 6, 153, 'active', 50000.00),
(24, 4, 7, 150, 'active', 50000.00),

-- Portals from Universe 5 (Family Guy) to all others
(25, 5, 1, 154, 'active', 50000.00),
(26, 5, 2, 150, 'active', 50000.00),
(27, 5, 3, 153, 'active', 50000.00),
(28, 5, 4, 154, 'active', 50000.00),
(29, 5, 6, 150, 'active', 50000.00),
(30, 5, 7, 153, 'active', 50000.00),

-- Portals from Universe 6 (Marvel) to all others
(31, 6, 1, 154, 'active', 50000.00),
(32, 6, 2, 153, 'active', 50000.00),
(33, 6, 3, 150, 'active', 50000.00),
(34, 6, 4, 154, 'active', 50000.00),
(35, 6, 5, 153, 'active', 50000.00),
(36, 6, 7, 150, 'active', 50000.00),

-- Portals from Universe 7 (Invincible) to all others
(37, 7, 1, 154, 'active', 50000.00),
(38, 7, 2, 150, 'active', 50000.00),
(39, 7, 3, 153, 'active', 50000.00),
(40, 7, 4, 154, 'active', 50000.00),
(41, 7, 5, 150, 'active', 50000.00),
(42, 7, 6, 153, 'active', 50000.00),

-- Inactive/Under Maintenance Portals
(43, 1, 6, 153, 'closed', 50000.00),
(44, 2, 7, 154, 'maintenance', 50000.00),
(45, 3, 5, 150, 'closed', 50000.00),
(46, 4, 2, 153, 'maintenance', 50000.00),
(47, 5, 3, 154, 'closed', 50000.00),
(48, 6, 4, 150, 'maintenance', 50000.00),
(49, 7, 4, 153, 'closed', 50000.00);

-- =====================================================
-- STEP 9: Insert Portal Calibration Records
-- =====================================================

-- Calibrations for key portals by different engineers
INSERT INTO PortalCalibration (portal_id, calibration_code, engineer_id, calibration_timestamp) VALUES
(1, 'CAL-2024-001', 150, '2023-01-10 08:30:00'),
(1, 'CAL-2024-045', 153, '2025-06-15 14:20:00'),
(5, 'CAL-2024-002', 150, '2023-01-12 09:15:00'),
(10, 'CAL-2024-003', 154, '2023-01-15 10:45:00'),
(15, 'CAL-2024-004', 150, '2023-01-18 11:30:00'),
(20, 'CAL-2024-005', 153, '2023-02-01 13:00:00'),
(25, 'CAL-2024-006', 154, '2023-02-05 15:45:00'),
(30, 'CAL-2024-007', 150, '2023-02-10 09:00:00'),
(35, 'CAL-2024-008', 153, '2023-02-15 10:30:00'),
(36, 'CAL-2024-009', 150, '2023-02-20 14:15:00'),
(40, 'CAL-2024-010', 154, '2024-04-15 08:45:00'),
(42, 'CAL-2024-011', 153, '2024-05-01 16:20:00'),
(12, 'CAL-2024-012', 150, '2024-06-10 11:00:00'),
(18, 'CAL-2024-013', 154, '2024-07-05 13:30:00'),
(22, 'CAL-2024-014', 153, '2024-08-01 09:45:00');

-- =====================================================
-- STEP 10: Insert Recruitment Events
-- =====================================================

-- Recruitment events for all Tier 2 members (recruited by Tier 1)
INSERT INTO RecruitmentEvent (recruiter_id, recruit_id, recruitment_date, recruitment_method) VALUES
(1, 8, '2023-03-01', 'personal'),
(1, 9, '2023-03-05', 'personal'),
(1, 10, '2023-03-10', 'referral'),
(1, 11, '2023-03-15', 'personal'),
(2, 12, '2023-03-01', 'personal'),
(2, 13, '2023-03-05', 'referral'),
(2, 14, '2023-03-10', 'personal'),
(2, 15, '2023-03-15', 'personal'),
(3, 16, '2023-03-01', 'personal'),
(3, 17, '2023-03-05', 'personal'),
(3, 18, '2023-03-10', 'referral'),
(3, 19, '2023-03-15', 'personal'),
(4, 20, '2023-03-01', 'personal'),
(4, 21, '2023-03-05', 'personal'),
(4, 22, '2023-03-10', 'referral'),
(4, 23, '2023-03-15', 'marketing'),
(5, 24, '2023-03-01', 'personal'),
(5, 25, '2023-03-05', 'personal'),
(5, 26, '2023-03-10', 'referral'),
(5, 27, '2023-03-15', 'personal'),
(6, 28, '2023-03-01', 'portal'),
(6, 29, '2023-03-05', 'personal'),
(6, 30, '2023-03-10', 'personal'),
(6, 31, '2023-03-15', 'portal'),
(7, 32, '2023-03-01', 'personal'),
(7, 33, '2023-03-05', 'portal'),
(7, 34, '2023-03-10', 'personal'),
(7, 35, '2023-03-15', 'personal');

-- Recruitment events for all Tier 3 members (recruited by Tier 2)
INSERT INTO RecruitmentEvent (recruiter_id, recruit_id, recruitment_date, recruitment_method) VALUES
(8, 36, '2025-01-15', 'personal'),
(8, 37, '2024-05-01', 'referral'),
(8, 38, '2025-06-10', 'personal'),
(8, 39, '2024-07-05', 'personal'),
(9, 40, '2025-01-15', 'personal'),
(9, 41, '2024-05-01', 'referral'),
(9, 42, '2025-06-10', 'personal'),
(9, 43, '2024-07-05', 'marketing'),
(10, 44, '2025-01-15', 'personal'),
(10, 45, '2024-05-01', 'personal'),
(10, 46, '2025-06-10', 'referral'),
(10, 47, '2024-07-05', 'personal'),
(11, 48, '2025-01-15', 'personal'),
(11, 49, '2024-05-01', 'personal'),
(11, 50, '2025-06-10', 'referral'),
(11, 51, '2024-07-05', 'personal'),
(12, 52, '2025-01-15', 'personal'),
(12, 53, '2024-05-01', 'marketing'),
(12, 54, '2025-06-10', 'personal'),
(12, 55, '2024-07-05', 'referral'),
(13, 56, '2025-01-15', 'personal'),
(13, 57, '2024-05-01', 'portal'),
(13, 58, '2025-06-10', 'personal'),
(13, 59, '2024-07-05', 'referral'),
(14, 60, '2025-01-15', 'personal'),
(14, 61, '2024-05-01', 'personal'),
(14, 62, '2025-06-10', 'referral'),
(14, 63, '2024-07-05', 'portal'),
(15, 64, '2025-01-15', 'personal'),
(15, 65, '2024-05-01', 'personal'),
(15, 66, '2025-06-10', 'referral'),
(15, 67, '2024-07-05', 'personal'),
(16, 68, '2025-01-15', 'personal'),
(16, 69, '2024-05-01', 'personal'),
(16, 70, '2025-06-10', 'referral'),
(16, 71, '2024-07-05', 'personal'),
(17, 72, '2025-01-15', 'personal'),
(17, 73, '2024-05-01', 'personal'),
(17, 74, '2025-06-10', 'personal'),
(17, 75, '2024-07-05', 'referral'),
(18, 76, '2025-01-15', 'personal'),
(18, 77, '2024-05-01', 'referral'),
(18, 78, '2025-06-10', 'marketing'),
(18, 79, '2024-07-05', 'personal'),
(19, 80, '2025-01-15', 'personal'),
(19, 81, '2024-05-01', 'personal'),
(19, 82, '2025-06-10', 'referral'),
(19, 83, '2024-07-05', 'portal'),
(20, 84, '2025-01-15', 'personal'),
(20, 85, '2024-05-01', 'referral'),
(20, 86, '2025-06-10', 'personal'),
(20, 87, '2024-07-05', 'marketing'),
(21, 88, '2025-01-15', 'portal'),
(21, 89, '2024-05-01', 'personal'),
(21, 90, '2025-06-10', 'referral'),
(21, 91, '2024-07-05', 'personal'),
(22, 92, '2025-01-15', 'personal'),
(22, 93, '2024-05-01', 'personal'),
(22, 94, '2025-06-10', 'referral'),
(22, 95, '2024-07-05', 'personal'),
(23, 96, '2025-01-15', 'personal'),
(23, 97, '2024-05-01', 'marketing'),
(23, 98, '2025-06-10', 'personal'),
(23, 99, '2024-07-05', 'referral'),
(24, 100, '2025-01-15', 'personal'),
(24, 101, '2024-05-01', 'personal'),
(24, 102, '2025-06-10', 'personal'),
(24, 103, '2024-07-05', 'referral'),
(25, 104, '2025-01-15', 'personal'),
(25, 105, '2024-05-01', 'referral'),
(25, 106, '2025-06-10', 'personal'),
(25, 107, '2024-07-05', 'personal'),
(26, 108, '2025-01-15', 'personal'),
(26, 109, '2024-05-01', 'personal'),
(26, 110, '2025-06-10', 'referral'),
(26, 111, '2024-07-05', 'personal'),
(27, 112, '2025-01-15', 'personal'),
(27, 113, '2024-05-01', 'referral'),
(27, 114, '2025-06-10', 'personal'),
(27, 115, '2024-07-05', 'personal'),
(28, 116, '2025-01-15', 'portal'),
(28, 117, '2024-05-01', 'portal'),
(28, 118, '2025-06-10', 'personal'),
(28, 119, '2024-07-05', 'personal'),
(29, 120, '2025-01-15', 'personal'),
(29, 121, '2024-05-01', 'personal'),
(29, 122, '2025-06-10', 'referral'),
(29, 123, '2024-07-05', 'personal'),
(30, 124, '2025-01-15', 'personal'),
(30, 125, '2024-05-01', 'personal'),
(30, 126, '2025-06-10', 'portal'),
(30, 127, '2024-07-05', 'referral'),
(31, 128, '2025-01-15', 'personal'),
(31, 129, '2024-05-01', 'portal'),
(31, 130, '2025-06-10', 'portal'),
(31, 131, '2024-07-05', 'personal'),
(32, 132, '2025-01-15', 'personal'),
(32, 133, '2024-05-01', 'referral'),
(32, 134, '2025-06-10', 'personal'),
(32, 135, '2024-07-05', 'personal'),
(33, 136, '2025-01-15', 'portal'),
(33, 137, '2024-05-01', 'portal'),
(33, 138, '2025-06-10', 'portal'),
(33, 139, '2024-07-05', 'personal'),
(34, 140, '2025-01-15', 'personal'),
(34, 141, '2024-05-01', 'referral'),
(34, 142, '2025-06-10', 'personal'),
(34, 143, '2024-07-05', 'personal'),
(35, 144, '2025-01-15', 'personal'),
(35, 145, '2024-05-01', 'personal'),
(35, 146, '2025-06-10', 'referral'),
(35, 147, '2024-07-05', 'personal');

-- =====================================================
-- STEP 11: Insert Transactions
-- =====================================================

-- Initial investment transactions from Tier 1 members
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(1, 1, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(2, 2, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(3, 3, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(4, 4, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(5, 5, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(6, 6, NULL, 'investment', 100000.00, '2023-01-15', 'completed'),
(7, 7, NULL, 'investment', 100000.00, '2023-01-15', 'completed');

-- Investment transactions from Tier 2 members
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(8, 8, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(9, 9, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(10, 10, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(11, 11, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(12, 12, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(13, 13, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(14, 14, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(15, 15, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(16, 16, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(17, 17, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(18, 18, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(19, 19, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(20, 20, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(21, 21, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(22, 22, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(23, 23, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(24, 24, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(25, 25, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(26, 26, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(27, 27, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(28, 28, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(29, 29, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(30, 30, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(31, 31, NULL, 'investment', 50000.00, '2023-03-15', 'completed'),
(32, 32, NULL, 'investment', 50000.00, '2023-03-01', 'completed'),
(33, 33, NULL, 'investment', 50000.00, '2023-03-05', 'completed'),
(34, 34, NULL, 'investment', 50000.00, '2023-03-10', 'completed'),
(35, 35, NULL, 'investment', 50000.00, '2023-03-15', 'completed');

-- Commission payments from Tier 2 to Tier 1 recruiters
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(36, NULL, 1, 'commission', 10000.00, '2023-03-20', 'completed'),
(37, NULL, 2, 'commission', 10000.00, '2023-03-20', 'completed'),
(38, NULL, 3, 'commission', 10000.00, '2023-03-20', 'completed'),
(39, NULL, 4, 'commission', 10000.00, '2023-03-20', 'completed'),
(40, NULL, 5, 'commission', 10000.00, '2023-03-20', 'completed'),
(41, NULL, 6, 'commission', 10000.00, '2023-03-20', 'completed'),
(42, NULL, 7, 'commission', 10000.00, '2023-03-20', 'completed');

-- Sample investment transactions from Tier 3 members
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(43, 36, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(44, 40, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(45, 44, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(46, 48, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(47, 52, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(48, 56, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(49, 60, NULL, 'investment', 25000.00, '2025-01-15', 'completed'),
(50, 64, NULL, 'investment', 25000.00, '2025-01-15', 'completed');

-- Commission payments from Tier 3 to Tier 2 recruiters
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(51, NULL, 8, 'commission', 3750.00, '2024-09-10', 'completed'),
(52, NULL, 9, 'commission', 3750.00, '2024-09-10', 'completed'),
(53, NULL, 10, 'commission', 3750.00, '2024-09-10', 'completed'),
(54, NULL, 12, 'commission', 3750.00, '2024-09-10', 'completed'),
(55, NULL, 16, 'commission', 3750.00, '2024-09-10', 'completed'),
(56, NULL, 20, 'commission', 3750.00, '2024-09-10', 'completed');

-- Bonus transactions for top performers
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(57, NULL, 1, 'bonus', 5000.00, '2025-01-01', 'completed'),
(58, NULL, 6, 'bonus', 5000.00, '2025-01-01', 'completed'),
(59, NULL, 4, 'bonus', 3500.00, '2025-01-01', 'completed'),
(60, NULL, 8, 'bonus', 2000.00, '2025-01-05', 'completed'),
(61, NULL, 12, 'bonus', 2000.00, '2025-01-05', 'completed');

-- Some pending transactions
INSERT INTO Transaction (transaction_id, from_member_id, to_member_id, transaction_type, amount, transaction_date, status) VALUES
(62, 68, NULL, 'investment', 25000.00, '2025-10-10', 'pending'),
(63, 72, NULL, 'investment', 25000.00, '2025-10-12', 'pending'),
(64, NULL, 16, 'commission', 2500.00, '2025-10-15', 'pending');

-- =====================================================
-- STEP 12: Insert Marketing Campaigns
-- =====================================================

INSERT INTO MarketingCampaign (program_id, program_code) VALUES
(1, 'MULTIV-2024-Q1'),
(2, 'HEROES-2024-Q1'),
(3, 'COSMIC-2024-Q2'),
(4, 'WIZARD-2024-Q1'),
(5, 'FAMILY-2024-Q2'),
(6, 'SCIENCE-2024-Q1'),
(7, 'SUPER-2024-Q2');

INSERT INTO MarketingCampaignAdditional (program_code, universe_id, name, budget, start_date, end_date, status) VALUES
('MULTIV-2024-Q1', 1, 'Friends Forever Investment Drive', 75000.00, '2023-01-01', '2023-03-31', 'completed'),
('HEROES-2024-Q1', 6, 'Avengers Assemble Wealth Campaign', 150000.00, '2023-01-15', '2023-04-15', 'completed'),
('COSMIC-2024-Q2', 6, 'Asgardian Prosperity Initiative', 120000.00, '2024-04-01', '2024-06-30', 'completed'),
('WIZARD-2024-Q1', 4, 'Magical Investment Opportunities', 90000.00, '2024-02-01', '2024-04-30', 'completed'),
('FAMILY-2024-Q2', 5, 'Quahog Financial Freedom', 60000.00, '2024-04-01', '2024-06-30', 'completed'),
('SCIENCE-2024-Q1', 2, 'Big Brain Big Returns', 80000.00, '2024-01-20', '2024-04-20', 'completed'),
('SUPER-2024-Q2', 7, 'Invincible Investment Strategy', 100000.00, '2025-04-15', '2025-07-15', 'active');

-- Members involved in marketing campaigns
INSERT INTO MarketingCampaign_MembersInvolved (program_id, members_involved) VALUES
(1, 1), (1, 8), (1, 9), (1, 11),
(2, 6), (2, 28), (2, 29), (2, 30), (2, 31),
(3, 6), (3, 28), (3, 116), (3, 119),
(4, 4), (4, 20), (4, 21), (4, 23),
(5, 5), (5, 24), (5, 25),
(6, 2), (6, 12), (6, 13), (6, 53),
(7, 7), (7, 32), (7, 35), (7, 134);

-- =====================================================
-- DATA POPULATION COMPLETE
-- =====================================================

SELECT 'Database population completed successfully!' AS Status;
SELECT COUNT(*) AS Total_Universes FROM Universe;
SELECT COUNT(*) AS Total_Participants FROM Participant;
SELECT COUNT(*) AS Total_Members FROM Member;
SELECT COUNT(*) AS Total_Employees FROM Employee;
SELECT COUNT(*) AS Total_Portals FROM Portals;
SELECT tier_level, COUNT(*) AS member_count FROM Member GROUP BY tier_level ORDER BY tier_level;

