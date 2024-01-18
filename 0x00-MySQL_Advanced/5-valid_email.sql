-- Email validation to sent
DELIMITER $$
CREATE TRIGGER valid
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
	SET NEW.valid_email = 0;
END $$
DELIMITER ;
