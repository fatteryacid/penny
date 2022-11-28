DROP TABLE d_subcategory CASCADE;

CREATE TABLE d_subcategory (
    subcategory_id SERIAL NOT NULL PRIMARY KEY,
    category_id INT NOT NULL,
    subcategory_desc VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT fk_cat FOREIGN KEY (category_id) REFERENCES d_category(category_id) ON DELETE SET NULL
);

DROP SEQUENCE subcategory_sequence;

CREATE SEQUENCE subcategory_sequence
    START 100
    INCREMENT 1
;


INSERT INTO d_subcategory (subcategory_id, category_id, subcategory_desc)
VALUES
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'automotive'),
        'gas'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'automotive'),
        'car_maintenance'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'automotive'),
        'car_aftermarket'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'automotive'),
        'car_insurance'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'education'),
        'textbook'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'education'),
        'course_fee'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'education'),
        'tuition_fee'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'video_game'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'game_service'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'movie'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'streaming_service'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'destination'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'novel'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'outdoor'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'arts_and_crafts'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'recreation'),
        'music'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'cookware'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'diningware'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'appliance'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'toiletry'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'medicine'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'cleaning_supply'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'garden'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'tool'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'decoration'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'furniture'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'renovation'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'organization'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'laundry'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'household'),
        'home_security'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'dining'),
        'bakery'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'dining'),
        'dine_in'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'dining'),
        'takeout'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'dining'),
        'drink'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'dining'),
        'dessert'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fitness'),
        'membership_fee'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fitness'),
        'gym_equipment'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fitness'),
        'workout_accessory'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'clothing'),
        'top'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'clothing'),
        'bottom'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'clothing'),
        'footwear'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'clothing'),
        'clothing_accessory'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fee'),
        'government_fee'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fee'),
        'rent'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fee'),
        'peer_to_peer'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fee'),
        'business_fee'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'fee'),
        'store_membership'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'gift'),
        'holiday'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'gift'),
        'birthday'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'gift'),
        'random'
    ),



    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'computer_system'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'computer_part'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'computer_accessory'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'peripheral'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'stationery'
    ),
    (
		nextval('subcategory_sequence'),
        (SELECT category_id FROM d_category WHERE category_desc = 'office'),
        'software_subscription'
    )
;