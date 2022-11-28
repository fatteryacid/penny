# Changelog

### Version 1.0.1
- Schema changes
    - d_subcategory now stores foreign key constraint 'fk_cat' in reference to d_category. This deprecates the use  of the join table j_categorical
    - clothing
        - accessory changed to clothing_accessory
    - fee
        - penalty_fee changed to business fee
        - warehouse_membership changed to store_membership