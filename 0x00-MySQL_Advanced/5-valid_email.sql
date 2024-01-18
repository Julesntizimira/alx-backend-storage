-- Email validation to sent
-- SQL script to create a trigger for email validation
DELIMITER $$
CREATE TRIGGER valid_email_trigger
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END $$
DELIMITER ;
