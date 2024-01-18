-- Email validation to sent
DELIMITER $$
CREATE TRIGGER valid
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        UPDATE users SET valid_email = 0 WHERE email = NEW.email;
    END IF;
END $$
DELIMITER ;
