-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 26, 2025 at 09:34 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `slms_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `b_Id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `main_genre` varchar(100) DEFAULT NULL,
  `sub_genre` varchar(100) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  `available_stock` int(11) NOT NULL CHECK (`available_stock` >= 0),
  `total_stock` int(11) NOT NULL CHECK (`total_stock` >= `available_stock` and `total_stock` > 0),
  `price` decimal(8,2) DEFAULT NULL CHECK (`price` >= 0),
  `aggregate_rating` decimal(2,1) DEFAULT 0.0 CHECK (`aggregate_rating` between 0.0 and 5.0),
  `daily_late_fine` decimal(4,2) DEFAULT 0.50 CHECK (`daily_late_fine` >= 0.00)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`b_Id`, `title`, `author`, `main_genre`, `sub_genre`, `language`, `available_stock`, `total_stock`, `price`, `aggregate_rating`, `daily_late_fine`) VALUES
(1, 'It Ends with Us', 'Colleen Hoover', 'Romance', 'Contemporary', 'English', 8, 10, 499.00, 4.5, 10.00),
(2, 'The Hound of the Baskervilles', 'Arthur Conan Doyle', 'Mystery', 'Detective Fiction', 'English', 6, 7, 299.00, 4.7, 15.00),
(3, '1984', 'George Orwell', 'Dystopian', 'Political Fiction', 'English', 6, 8, 350.00, 4.8, 12.00),
(4, 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 'Historical Fiction', 'English', 7, 10, 400.00, 4.9, 15.00),
(5, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'Tragedy', 'English', 4, 6, 320.00, 4.6, 10.00),
(6, 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 'Adventure', 'English', 10, 12, 550.00, 4.9, 20.00),
(7, 'The Fault in Our Stars', 'John Green', 'Romance', 'Young Adult', 'English', 9, 10, 450.00, 4.4, 10.00),
(8, 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'Adventure', 'English', 6, 8, 499.00, 4.8, 15.00),
(9, 'Pride and Prejudice', 'Jane Austen', 'Classic', 'Romance', 'English', 4, 7, 375.00, 4.7, 10.00),
(10, 'The Alchemist', 'Paulo Coelho', 'Philosophical', 'Adventure', 'English', 7, 9, 425.00, 4.6, 12.00);

-- --------------------------------------------------------

--
-- Table structure for table `librarian`
--

CREATE TABLE `librarian` (
  `u_Id` int(11) NOT NULL,
  `address` text DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `date_created` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `librarian`
--

INSERT INTO `librarian` (`u_Id`, `address`, `phone`, `date_created`) VALUES
(101, '123 Library St, Mumbai', '9876543210', '2023-01-15'),
(102, '45 Book Ave, Delhi', '9123456789', '2022-07-10');

-- --------------------------------------------------------

--
-- Table structure for table `loan_record`
--

CREATE TABLE `loan_record` (
  `loan_id` int(11) NOT NULL,
  `u_Id` int(11) NOT NULL,
  `b_Id` int(11) NOT NULL,
  `librarian_id` int(11) DEFAULT NULL,
  `issue_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `due_date` date NOT NULL,
  `return_date` timestamp NULL DEFAULT NULL,
  `fine_amount` decimal(6,2) DEFAULT 0.00 CHECK (`fine_amount` >= 0.00),
  `loan_status` enum('Active','Returned - On Time','Returned - Late','Lost') NOT NULL
) ;

--
-- Dumping data for table `loan_record`
--

INSERT INTO `loan_record` (`loan_id`, `u_Id`, `b_Id`, `librarian_id`, `issue_date`, `due_date`, `return_date`, `fine_amount`, `loan_status`) VALUES
(1, 1, 1, 101, '2025-09-01 04:30:00', '2025-09-10', '2025-09-12 10:00:00', 20.00, 'Returned - Late'),
(2, 1, 3, 102, '2025-09-15 04:00:00', '2025-09-25', '2025-09-25 11:30:00', 0.00, 'Returned - On Time'),
(3, 2, 2, 101, '2025-10-01 05:30:00', '2025-10-10', '2025-10-22 09:45:37', 180.00, 'Returned - Late'),
(4, 3, 4, 102, '2025-09-20 08:30:00', '2025-09-30', '2025-09-29 10:30:00', 0.00, 'Returned - On Time'),
(5, 4, 5, 101, '2025-08-01 03:30:00', '2025-08-10', '2025-08-15 04:30:00', 50.00, 'Returned - Late'),
(6, 4, 6, 102, '2025-09-05 06:30:00', '2025-09-15', NULL, 0.00, 'Active'),
(7, 4, 7, 101, '2025-07-01 04:30:00', '2025-07-10', '2025-07-15 04:30:00', 500.00, 'Lost'),
(8, 1, 9, NULL, '2025-10-22 06:49:00', '2025-11-05', NULL, 0.00, 'Active'),
(9, 1, 10, NULL, '2025-10-22 06:49:17', '2025-11-05', NULL, 0.00, 'Active'),
(10, 2, 6, NULL, '2025-10-24 06:43:44', '2025-11-07', '2025-10-24 06:53:41', 0.00, 'Returned - On Time'),
(11, 2, 3, NULL, '2025-10-26 07:37:50', '2025-11-05', '2025-10-26 07:38:40', 0.00, 'Returned - On Time'),
(12, 2, 3, NULL, '2025-10-26 07:40:24', '2025-11-05', '2025-10-26 07:40:41', 0.00, 'Returned - On Time'),
(13, 2, 3, NULL, '2025-10-26 07:44:36', '2025-11-05', '2025-10-26 07:44:40', 0.00, 'Returned - On Time'),
(14, 2, 6, NULL, '2025-10-26 07:49:08', '2025-11-05', '2025-10-26 07:49:13', 0.00, 'Returned - On Time'),
(15, 2, 1, NULL, '2025-10-26 07:51:53', '2025-11-05', '2025-10-26 07:52:05', 0.00, 'Returned - On Time'),
(16, 2, 3, NULL, '2025-10-26 08:04:35', '2025-11-05', '2025-10-26 08:04:43', 0.00, 'Returned - On Time');

-- --------------------------------------------------------

--
-- Table structure for table `personal_rating`
--

CREATE TABLE `personal_rating` (
  `u_Id` int(11) NOT NULL,
  `b_Id` int(11) NOT NULL,
  `rating_value` decimal(2,1) NOT NULL,
  `rating_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personal_rating`
--

INSERT INTO `personal_rating` (`u_Id`, `b_Id`, `rating_value`, `rating_date`) VALUES
(2, 1, 3.2, '2025-10-26 07:52:11'),
(2, 2, 4.6, '2025-10-22 09:45:48'),
(2, 3, 4.9, '2025-10-26 08:04:55'),
(2, 6, 4.3, '2025-10-26 07:49:18');

-- --------------------------------------------------------

--
-- Table structure for table `reader`
--

CREATE TABLE `reader` (
  `u_Id` int(11) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `date_joined` date NOT NULL DEFAULT curdate(),
  `current_loan_count` int(11) DEFAULT 0 CHECK (`current_loan_count` >= 0),
  `overdue_fines` decimal(6,2) DEFAULT 0.00 CHECK (`overdue_fines` >= 0.00),
  `user_remark` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reader`
--

INSERT INTO `reader` (`u_Id`, `phone`, `date_joined`, `current_loan_count`, `overdue_fines`, `user_remark`) VALUES
(1, '9876543210', '2024-02-15', 4, 0.00, 'Active reader, always returns books on time.'),
(2, '9123456789', '2023-09-10', 0, 181.50, 'Recently returned a book late, fine cleared.'),
(3, '9988776655', '2024-05-21', 0, 0.00, 'Prefers e-books and light novels.'),
(4, '9001122334', '2022-12-30', 3, 5.00, 'Occasionally delays returns due to travel.');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `u_Id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `role` enum('Reader','Librarian','Admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`u_Id`, `name`, `email`, `password`, `date_of_birth`, `role`) VALUES
(1, 'Alice Johnson', 'alice.johnson@gmail.com', 'ReaderPass123', '1992-05-15', 'Reader'),
(2, 'David Williams', 'david.williams@gmail.com', 'ReaderPass456', '1995-02-18', 'Reader'),
(3, 'Eva Green', 'eva.green@gmail.com', 'ReaderPass789', '1990-07-10', 'Reader'),
(4, 'Frank Miller', 'frank.miller@gmail.com', 'FrankPass001', '1983-12-05', 'Reader'),
(5, 'Adiy Rahman', 'adiy.rahman@gmail.com', 'AdminPass123', '2004-04-14', 'Admin'),
(101, 'Sarah Thompson', 'sarah.thompson@gmail.com', 'LibPass001', '1985-03-12', 'Librarian'),
(102, 'Michael Brown', 'michael.brown@gmail.com', 'LibPass002', '1978-08-25', 'Librarian');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`b_Id`);

--
-- Indexes for table `librarian`
--
ALTER TABLE `librarian`
  ADD PRIMARY KEY (`u_Id`);

--
-- Indexes for table `loan_record`
--
ALTER TABLE `loan_record`
  ADD PRIMARY KEY (`loan_id`),
  ADD KEY `loan_record_ibfk_1` (`u_Id`),
  ADD KEY `loan_record_ibfk_2` (`b_Id`),
  ADD KEY `loan_record_ibfk_3` (`librarian_id`);

--
-- Indexes for table `personal_rating`
--
ALTER TABLE `personal_rating`
  ADD PRIMARY KEY (`u_Id`,`b_Id`),
  ADD KEY `personal_rating_ibfk_2` (`b_Id`);

--
-- Indexes for table `reader`
--
ALTER TABLE `reader`
  ADD PRIMARY KEY (`u_Id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`u_Id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `b_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `loan_record`
--
ALTER TABLE `loan_record`
  MODIFY `loan_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `u_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `librarian`
--
ALTER TABLE `librarian`
  ADD CONSTRAINT `librarian_ibfk_1` FOREIGN KEY (`u_Id`) REFERENCES `users` (`u_Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `loan_record`
--
ALTER TABLE `loan_record`
  ADD CONSTRAINT `loan_record_ibfk_1` FOREIGN KEY (`u_Id`) REFERENCES `reader` (`u_Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `loan_record_ibfk_2` FOREIGN KEY (`b_Id`) REFERENCES `books` (`b_Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `loan_record_ibfk_3` FOREIGN KEY (`librarian_id`) REFERENCES `librarian` (`u_Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `personal_rating`
--
ALTER TABLE `personal_rating`
  ADD CONSTRAINT `personal_rating_ibfk_1` FOREIGN KEY (`u_Id`) REFERENCES `reader` (`u_Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `personal_rating_ibfk_2` FOREIGN KEY (`b_Id`) REFERENCES `books` (`b_Id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `reader`
--
ALTER TABLE `reader`
  ADD CONSTRAINT `reader_ibfk_1` FOREIGN KEY (`u_Id`) REFERENCES `users` (`u_Id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
