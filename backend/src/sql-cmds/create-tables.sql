use animal_shelter;
CREATE TABLE animal_information (
    animal_id int auto_increment PRIMARY KEY,
    name VARCHAR(50),
    species ENUM('Dog', 'Cat', 'Other'),
    breed VARCHAR(50),
    age INT,
    sex ENUM('Male', 'Female'),
    characteristics VARCHAR(128),
    health_status ENUM('Healthy', 'Minor Injury', 'Major Injury'),
    arrival_date DATE,
    adoption_status ENUM('Adopted', 'Not Adopted'),
    special_needs VARCHAR(512),
    adoption_date DATE,
    birthday DATE,
    notes VARCHAR(512),
    size ENUM('Big', 'Medium', 'Small'),
    location_rescued VARCHAR(512),
    description VARCHAR(512),
    is_desexed ENUM('Yes', 'No')
);

create table animal_med_history(
 vacc_id int auto_increment ,
    vacc_type varchar(128),
    vacc_date date,
    vacc_dose int,
 animal_id int,
    PRIMARY KEY (vacc_id),
    FOREIGN KEY (animal_id) REFERENCES animal_information(animal_id) ON DELETE CASCADE

 );
