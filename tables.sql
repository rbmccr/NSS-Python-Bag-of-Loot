DROP TABLE IF EXISTS Child;
DROP TABLE IF EXISTS Toy;

CREATE TABLE `Child` (
    `childID`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `Name`    TEXT NOT NULL,
    `Delivered`    BIT NOT NULL
);

INSERT INTO Child VALUES (null, 'Brendan', 0);
INSERT INTO Child VALUES (null, 'Zac', 0);
INSERT INTO Child VALUES (null, 'Ousama', 0);
INSERT INTO Child VALUES (null, 'Richard', 0);
INSERT INTO Child VALUES (null, 'Brad', 0);

CREATE TABLE `Toy` (
    `toyID`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `Name`    TEXT NOT NULL,
    `childID`    INTEGER NOT NULL,
    FOREIGN KEY(`childID`)
    REFERENCES `Child`(`childID`)
);