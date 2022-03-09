-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 09, 2022 at 03:58 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.4.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `comp5327test`
--

-- --------------------------------------------------------

--
-- Table structure for table `Booking`
--

CREATE TABLE `Booking` (
  `booking_id` int(20) NOT NULL,
  `Slot_id` int(20) NOT NULL,
  `Username` varchar(20) NOT NULL,
  `apply_date_time` varchar(20) NOT NULL,
  `Cancel` varchar(3) NOT NULL,
  `Cancel_date_time` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Booking`
--

INSERT INTO `Booking` (`booking_id`, `Slot_id`, `Username`, `apply_date_time`, `Cancel`, `Cancel_date_time`) VALUES
(4, 3, 'test', '2022-03-01 23:05:32', 'Yes', '2022-03-01 23:07:32'),
(5, 1, 'test', '2022-03-01 23:06:10', '', ''),
(6, 2, 'test', '2022-03-01 23:33:06', '', ''),
(7, 4, 'test', '2022-03-01 23:37:04', '', ''),
(8, 4, 'test2', '2022-03-01 23:40:39', '', ''),
(9, 1, 'test2', '2022-03-03 15:59:50', '', ''),
(17, 6, 'test2', '2022-03-03 19:57:07', '', ''),
(24, 8, 'test', '2022-03-06 00:43:07', 'Yes', '2022-03-07 19:46:26'),
(27, 6, 'test', '2022-03-07 15:05:51', 'Yes', '2022-03-07 19:46:26'),
(28, 5, 'test', '2022-03-07 19:37:27', 'Yes', '2022-03-07 19:46:26'),
(29, 8, 'test', '2022-03-07 19:56:23', '', ''),
(30, 5, 'test', '2022-03-07 20:37:46', 'Yes', '2022-03-07 23:51:32'),
(31, 6, 'test', '2022-03-07 23:21:11', '', ''),
(32, 5, 'test', '2022-03-07 23:52:03', 'Yes', '2022-03-08 00:20:01'),
(33, 9, 'test', '2022-03-08 17:39:57', '', ''),
(34, 5, 'test', '2022-03-08 18:06:16', 'Yes', '2022-03-08 18:17:06'),
(35, 5, 'test', '2022-03-09 20:30:55', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `TImeslot`
--

CREATE TABLE `TImeslot` (
  `slot_id` int(20) NOT NULL,
  `date` varchar(10) NOT NULL,
  `time_slot` varchar(10) NOT NULL,
  `vacancy` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `TImeslot`
--

INSERT INTO `TImeslot` (`slot_id`, `date`, `time_slot`, `vacancy`) VALUES
(1, '2022-03-01', '10am-12pm', 2),
(2, '2022-03-01', '12pm-2pm', 30),
(3, '2022-03-01', '2pm-4pm', 10),
(4, '2022-03-02', '2pm-4pm', 30),
(5, '2022-03-11', '2pm-3pm', 0),
(6, '2022-03-11', '3pm-4pm', 1),
(7, '2022-03-06', '8pm-10pm', 2),
(8, '2022-03-07', '8pm-10pm', 4),
(9, '2022-03-11', '4pm-5pm', 9);

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `Username` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `First_name` varchar(20) NOT NULL,
  `Last_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`Username`, `Password`, `First_name`, `Last_name`) VALUES
('test', 'test', 'Testperson1', 'Chan'),
('test2', 'test2', 'Tai Man', 'Chan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Booking`
--
ALTER TABLE `Booking`
  ADD PRIMARY KEY (`booking_id`),
  ADD UNIQUE KEY `booking_id` (`booking_id`),
  ADD KEY `Username` (`Username`),
  ADD KEY `Slot_id` (`Slot_id`);

--
-- Indexes for table `TImeslot`
--
ALTER TABLE `TImeslot`
  ADD PRIMARY KEY (`slot_id`),
  ADD UNIQUE KEY `slot_id` (`slot_id`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`Username`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Booking`
--
ALTER TABLE `Booking`
  MODIFY `booking_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `TImeslot`
--
ALTER TABLE `TImeslot`
  MODIFY `slot_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Booking`
--
ALTER TABLE `Booking`
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`Username`) REFERENCES `User` (`Username`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`Slot_id`) REFERENCES `TImeslot` (`slot_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
