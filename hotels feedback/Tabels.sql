DROP TABLE IF EXISTS Hotels;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Reviewer;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE Hotels (
    HotelID INTEGER PRIMARY KEY AUTOINCREMENT,
    hotName varchar(255) NOT NULL,
    hotDes TEXT,
    picture 
);


CREATE TABLE Reviewer(
    ReviewerID INTEGER PRIMARY KEY AUTOINCREMENT, 
    FirstName varchar(100),
    LastName varchar(100),
    ReviewID int,
    HotelID int,
    FOREIGN KEY (HotelID) REFERENCES Hotels(HotelID),
    FOREIGN KEY (ReviewID) REFERENCES Reviews(ReviewID)
    );

CREATE TABLE Reviews (
    ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReviewerID int,
    HotelID int,
    Review varchar(255) NOT NULL,
    FOREIGN KEY (ReviewerID) REFERENCES Reviewer(ReviewerID),
    FOREIGN KEY (HotelID) REFERENCES Hotels(HotelID)
);

CREATE TABLE messages (
    mess_id INTEGER PRIMARY KEY AUTOINCREMENT,
    messName varchar(255) NOT NULL,
    messEmail varchar(255) NOT NULL,
    messPhone int,
    message_des varchar(255) NOT NULL
);

CREATE TABLE users (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    Email varchar(255) NOT NULL,
    password TEXT NOT NULL

);


