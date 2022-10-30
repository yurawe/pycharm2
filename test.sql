-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `playlist_service_db` DEFAULT CHARACTER SET utf8 ;
USE `playlist_service_db` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) ,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`genre` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`album`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`album` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`artist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`artist` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `date_of_birth` DATE NULL,
  `country` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`song`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`song` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `length` DOUBLE NOT NULL,
  `language` VARCHAR(45) NULL,
  `release_date` DATE NULL,
  `album_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`id`, `album_id`, `genre_id`),
  INDEX `fk_song_album_idx` (`album_id` ASC) VISIBLE,
  INDEX `fk_song_genre1_idx` (`genre_id` ASC) VISIBLE,
  CONSTRAINT `fk_song_album`
    FOREIGN KEY (`album_id`)
    REFERENCES `playlist_service_db`.`album` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_song_genre1`
    FOREIGN KEY (`genre_id`)
    REFERENCES `playlist_service_db`.`genre` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`artist_has_song`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`artist_song` (
  `artist_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`artist_id`, `song_id`),
  INDEX `fk_artist_has_song_song1_idx` (`song_id` ASC) VISIBLE,
  INDEX `fk_artist_has_song_artist1_idx` (`artist_id` ASC) VISIBLE,
  CONSTRAINT `fk_artist_has_song_artist1`
    FOREIGN KEY (`artist_id`)
    REFERENCES `playlist_service_db`.`artist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_artist_has_song_song1`
    FOREIGN KEY (`song_id`)
    REFERENCES `playlist_service_db`.`song` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`playlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`playlist` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `isPrivate` TINYINT NOT NULL,
  `created_at` DATE NOT NULL,
  `updated_at` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`user_has_playlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`user_playlist` (
  `user_id` INT NOT NULL,
  `playlist_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `playlist_id`),
  INDEX `fk_user_has_playlist_playlist1_idx` (`playlist_id` ASC) VISIBLE,
  INDEX `fk_user_has_playlist_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_has_playlist_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `playlist_service_db`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_playlist_playlist1`
    FOREIGN KEY (`playlist_id`)
    REFERENCES `playlist_service_db`.`playlist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`playlist_has_song`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `playlist_service_db`.`playlist_song` (
  `playlist_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`playlist_id`, `song_id`),
  INDEX `fk_playlist_has_song_song1_idx` (`song_id` ASC) VISIBLE,
  INDEX `fk_playlist_has_song_playlist1_idx` (`playlist_id` ASC) VISIBLE,
  CONSTRAINT `fk_playlist_has_song_playlist1`
    FOREIGN KEY (`playlist_id`)
    REFERENCES `playlist_service_db`.`playlist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_playlist_has_song_song1`
    FOREIGN KEY (`song_id`)
    REFERENCES `playlist_service_db`.`song` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- mysql -u root -p playlist_service_db < :\Users\Admin\PycharmProjects\pycharm2\test.sql
-- mysql -u root -p playlist_service_db < test.sql