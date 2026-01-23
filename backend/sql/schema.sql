-- Library Management System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS project;
USE project;

-- Table: book
CREATE TABLE IF NOT EXISTS book (
    book_id VARCHAR(10) PRIMARY KEY,
    book_name VARCHAR(50) NOT NULL,
    author VARCHAR(20),
    genre VARCHAR(10),
    price VARCHAR(7),
    count INT DEFAULT 0
);

-- Table: member
CREATE TABLE IF NOT EXISTS member (
    cust_id INT PRIMARY KEY,
    cust_name VARCHAR(20) NOT NULL,
    DOB DATE,
    gender CHAR(1),
    contact INT
);

-- Table: issue_and_return
CREATE TABLE IF NOT EXISTS issue_and_return (
    book_id VARCHAR(10),
    cust_id INT,
    date_of_issue DATE,
    date_of_return DATE,
    days_issued INT,
    days_kept INT,
    penalty INT DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (cust_id) REFERENCES member(cust_id)
);

-- Table: member_details
CREATE TABLE IF NOT EXISTS member_details (
    cust_id INT PRIMARY KEY,
    mail_id VARCHAR(30),
    password VARCHAR(20),
    status VARCHAR(10),
    FOREIGN KEY (cust_id) REFERENCES member(cust_id)
);

-- Insert sample data (optional)
INSERT INTO book VALUES('HP01JKR', 'Harry Potter and the Philosopher stone', 'J.K.Rowling', 'Fantasy', '280.00', 4);
INSERT INTO book VALUES('PJ01RR', 'Percy Jackson and the Lightning Thied', 'Rick Riordan', 'Fantasy', '320.00', 3);

INSERT INTO member VALUES('324J79', 'Lakshya Gupta', '2006-12-30', 'M', 9319027774);
INSERT INTO member VALUES('268K04', 'Devanshhi Dhingra', '2006-08-13', 'F', 8287314273);

INSERT INTO member_details VALUES('324J79', 'lakshya@gmail.com', 'lakshya3012', 'active');
INSERT INTO member_details VALUES('268K04', 'devanshhi@gmail.com', 'devanshhi1308', 'active');

INSERT INTO issue_and_return VALUES('PJ01RR', '324J79', '2023-05-21', '2023-06-18', 30, 28, 0);
INSERT INTO issue_and_return VALUES('HP01JKR', '268K04', '2023-07-13', '2023-08-07', 30, 24, 0);
