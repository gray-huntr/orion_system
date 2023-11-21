-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 19, 2023 at 11:28 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `orion_hospital`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointmentId` varchar(10) NOT NULL,
  `patientId` varchar(10) NOT NULL,
  `roomNo` varchar(10) DEFAULT NULL,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `status` varchar(25) NOT NULL DEFAULT 'Booked',
  `category` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointmentId`, `patientId`, `roomNo`, `time`, `status`, `category`) VALUES
('A1', 'P1', '2', '2023-11-10 10:00:00', 'Booked', 'online'),
('A2', 'P5', '1', '2023-11-09 18:56:14', 'attending', 'walk-in'),
('A3', 'P7', '2', '2023-11-20 10:00:00', 'Discharged', 'online'),
('A4', 'P6', '4', '2023-11-19 23:02:10', 'Discharged', 'walk-in');

-- --------------------------------------------------------

--
-- Table structure for table `billing`
--

CREATE TABLE `billing` (
  `billingid` int(10) NOT NULL,
  `patientId` varchar(10) NOT NULL,
  `appointmentid` varchar(10) NOT NULL,
  `test_cost` varchar(1000) NOT NULL,
  `total` int(15) NOT NULL,
  `cashier_id` varchar(10) DEFAULT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billing`
--

INSERT INTO `billing` (`billingid`, `patientId`, `appointmentid`, `test_cost`, `total`, `cashier_id`, `date`) VALUES
(1, 'P1', 'A1', 'CT scan= KSH: 500', 500, 'S4', '2023-11-10'),
(2, 'P5', 'A2', 'Blood test = KSH: 200\r\nCT scan = KSH: 500\r\nBlood count = KSH: 350', 1050, 'S4', '2023-11-10'),
(3, 'P6', 'A4', 'Blood test = KSH: 200\r\nBlood count = KSH: 350', 550, 'S4', '2023-11-20'),
(4, 'P7', 'A3', 'Blood test = KSH: 200\r\nBlood count = KSH: 350', 550, 'S4', '2023-11-20');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patientId` varchar(10) NOT NULL,
  `fullname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` varchar(15) NOT NULL,
  `id_number` varchar(15) NOT NULL,
  `password` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `DOB` date NOT NULL,
  `blood_group` varchar(5) NOT NULL,
  `status` varchar(10) DEFAULT 'Active',
  `firstLogin` int(5) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`patientId`, `fullname`, `email`, `number`, `id_number`, `password`, `gender`, `DOB`, `blood_group`, `status`, `firstLogin`) VALUES
('P1', 'lennox kulecho', 'lenox@gmail.com', '0123456789', '36748903456', '1234', 'male', '2013-10-16', 'O+', 'Active', 0),
('P2', 'lenny', 'lenny@gmail.com', '0113354678', '324567788', 'Patient@orion', 'male', '2007-06-19', 'AB+', 'Active', 1),
('P3', 'Tristan joe', 'tj@gmail.com', '077654389', '6582390984', 'Orion@patient', 'Male', '2006-11-13', 'B+', 'Active', 1),
('P4', 'Kai karo', 'kk@gmail.com', '07243567890', '9867342556', 'Orion@patient', 'Male', '2015-11-24', 'O+', 'Active', 1),
('P5', 'Micheal gift', 'mgift@gmail.com', '07231564849', '245698688', 'Patient@orion', 'male', '2023-01-04', 'O-', 'Active', 1),
('P6', 'ALfred kimani', 'akimani@gmail.com', '0784623739', '345456565', '1234', 'Male', '2006-10-20', 'B+', 'Active', 0),
('P7', 'Stacy muthoni', 'smuthoni@gmail.com', '079859439', '4543334795', '1234', 'Female', '2021-10-24', 'AB+', 'Active', 0),
('P8', 'Joy wambui', 'jwambui@gmail.com', '07234567890', '3212345678', 'Patient@orion', 'Female', '2023-02-21', 'A-', 'Active', 1),
('P9', 'Micheal scott', 'mscott@gmail.com', '0723145768', '9874462', 'Patient@orion', 'Male', '2009-06-05', 'A+', 'Active', 1);

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `roomid` int(10) NOT NULL,
  `category` varchar(15) NOT NULL,
  `status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`roomid`, `category`, `status`) VALUES
(1, 'online', 'occupied'),
(2, 'online', 'occupied'),
(3, 'walk-in', 'occupied'),
(4, 'walk-in', 'occupied'),
(5, 'admission', 'available'),
(6, 'admission', 'available');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staffId` varchar(10) NOT NULL,
  `fullname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` varchar(15) NOT NULL,
  `password` varchar(50) NOT NULL,
  `category` varchar(15) NOT NULL,
  `firstLogin` int(10) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staffId`, `fullname`, `email`, `number`, `password`, `category`, `firstLogin`) VALUES
('S1', 'Abdullahi raman', 'araman@gmail.com', '0123456789', '1234', 'Doctor', 0),
('S2', 'Hillary kenyatta', 'hillarykenyatta@gmail.com', '012345678', '1234', 'Receptionist', 0),
('S3', 'Steve Orito', 'Sorito@gmail.com', '0735642786', '12345', 'Pharmacist', 0),
('S4', 'Ruhiya temko', 'rtemko@gmail.com', '078965432', '1234', 'Cashier', 0),
('S5', 'Frosty stush', 'fstush@gmail.com', '0112345673', '1234', 'Admin', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE `tests` (
  `test_id` int(11) NOT NULL,
  `test_name` varchar(50) NOT NULL,
  `test_cost` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tests`
--

INSERT INTO `tests` (`test_id`, `test_name`, `test_cost`) VALUES
(1, 'Blood test', 200),
(2, 'CT scan', 500),
(3, 'Blood count', 350),
(4, 'X-ray', 1000),
(5, 'Medical test', 350),
(6, 'MRI', 750),
(7, 'Colonoscopy', 500),
(8, 'Urinalysis', 350),
(9, 'Endoscopy', 1000),
(10, 'Ultrasonography', 850);

-- --------------------------------------------------------

--
-- Table structure for table `treatment`
--

CREATE TABLE `treatment` (
  `treatmentid` varchar(10) NOT NULL,
  `patientId` varchar(10) NOT NULL,
  `appointmentid` varchar(10) NOT NULL,
  `symptoms` varchar(1000) NOT NULL,
  `admission_date` date NOT NULL DEFAULT current_timestamp(),
  `discharge_date` date DEFAULT NULL,
  `roomno` int(10) NOT NULL,
  `diagnosis` varchar(1000) NOT NULL,
  `prescription` varchar(1000) NOT NULL,
  `test_done` varchar(1000) NOT NULL,
  `doctorid` varchar(10) NOT NULL,
  `pharmacist_id` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `treatment`
--

INSERT INTO `treatment` (`treatmentid`, `patientId`, `appointmentid`, `symptoms`, `admission_date`, `discharge_date`, `roomno`, `diagnosis`, `prescription`, `test_done`, `doctorid`, `pharmacist_id`) VALUES
('T1', 'P1', 'A1', 'Headache\r\nJoint pains\r\nvomiting', '2023-11-09', NULL, 2, 'Malaria', 'flu gone', 'CT scan                    ', 'S1', 'S3'),
('T2', 'P5', 'A2', 'Headache\r\nfever\r\nfeeling cold', '2023-11-10', '2023-11-10', 2, 'pneumonia', 'piriton', 'Blood test\r\nCT scan\r\nBlood count', 'S1', NULL),
('T3', 'P6', 'A4', 'Joint pains\r\nstomach aches\r\ndiahrrea', '2023-11-20', '2023-11-20', 4, 'Malaria\r\npneumonia', 'piriton', 'Blood test\r\nBlood count', 'S1', 'S3'),
('T4', 'P7', 'A3', 'random stuff\r\nrandom stuu', '2023-11-20', '2023-11-20', 2, 'something happened', 'medicine\r\nmedicine\r\nmedicine', 'Blood test\r\nBlood count', 'S1', 'S3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointmentId`);

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`billingid`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patientId`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`roomid`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staffId`);

--
-- Indexes for table `tests`
--
ALTER TABLE `tests`
  ADD PRIMARY KEY (`test_id`);

--
-- Indexes for table `treatment`
--
ALTER TABLE `treatment`
  ADD PRIMARY KEY (`treatmentid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `billingid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `roomid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tests`
--
ALTER TABLE `tests`
  MODIFY `test_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
