USE animal_shelter;
INSERT INTO animal_information (
    name,
    species,
    breed,
    age,
    sex,
    characteristics,
    health_status,
    arrival_date,
    adoption_status,
    special_needs,
    adoption_date,
    birthday,
    notes,
    size,
    location_rescued,
    description,
    is_desexed
)
VALUES
    ('Max', 'Dog', 'Labrador', 3, 'Male', 'Friendly and playful', 'Healthy', '2024-01-15', 'Not Adopted', NULL, NULL, '2021-01-10', 'Loves kids', 'Big', 'Park Avenue', 'A lovable Labrador retriever', 'Yes'),
    ('Bella', 'Cat', 'Persian', 2, 'Female', 'Calm and quiet', 'Minor Injury', '2024-02-10', 'Adopted', NULL, '2024-06-10', '2022-02-15', 'Had minor surgery', 'Small', 'Downtown Shelter', 'A calm Persian cat', 'No'),
    ('Buddy', 'Dog', 'Beagle', 5, 'Male', 'Energetic and curious', 'Healthy', '2023-12-20', 'Not Adopted', 'Requires regular vet visits', NULL, '2019-12-25', 'Barks at strangers', 'Medium', 'Hillside Rescue', 'An energetic Beagle', 'Yes'),
    ('Daisy', 'Other', 'Rabbit', 1, 'Female', 'Shy but sweet', 'Healthy', '2024-03-01', 'Not Adopted', NULL, NULL, '2023-03-15', 'Prefers a quiet environment', 'Small', 'Countryside Farm', 'A shy little rabbit', 'No'),
    ('Charlie', 'Dog', 'Golden Retriever', 4, 'Male', 'Gentle and obedient', 'Major Injury', '2024-01-10', 'Not Adopted', 'Needs physical therapy', NULL, '2020-01-20', 'Recovering from injury', 'Big', 'Highway Rescue', 'A gentle Golden Retriever', 'Yes');

