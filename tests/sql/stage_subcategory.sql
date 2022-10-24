DROP TABLE d_subcategory;

CREATE TABLE d_subcategory (
    subcategory_id SERIAL NOT NULL PRIMARY KEY,
    subcategory_desc VARCHAR(50) UNIQUE
);

INSERT INTO d_subcategory (subcategory_desc)
VALUES
    ('raw_ingredient'),
    ('processed_food'),
    ('snack'),
    ('beverage'),
    ('condiment'),
    ('premade_deli'),
    ('cookware'),
    ('silverware'),
    ('appliance'),
    ('toiletry'),
    ('medicine'),
    ('cleaning_supply'),
    ('garden'),
    ('tool'),
    ('decoration'),
    ('furniture'),
    ('renovation'),
    ('organization'),
    ('laundry'),
    ('home_security'),
    ('dine_in'),
    ('takeout'),
    ('drink'),
    ('dessert'),
    ('membership_fee'),
    ('gym_equipment'),
    ('workout_accessory'),
    ('top'),
    ('bottom'),
    ('footwear'),
    ('accessory'),
    ('government_fee'),
    ('rent'),
    ('peer_to_peer'),
    ('penalty_fee'),
    ('warehouse_membership'),
    ('holiday'),
    ('birthday'),
    ('random'),
    ('computer_system'),
    ('computer_part'),
    ('computer_accessory'),
    ('peripheral'),
    ('stationery'),
    ('software_subscription'),
    ('gas'),
    ('car_maintenance'),
    ('car_aftermarket'),
    ('car_insurance'),
    ('textbook'),
    ('course_fee'),
    ('tuition_fee'),
    ('video_game'),
    ('game_service'),
    ('movie'),
    ('streaming_service'),
    ('destination'),
    ('novel'),
    ('outdoor'),
    ('arts_and_crafts'),
    ('music')
;