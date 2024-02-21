CREATE TABLE `unit_measure` (
  `unit_measure_id` int,
  `name` varchar(40),
  PRIMARY KEY (`unit_measure_id`)
);

CREATE TABLE `user_role` (
  `role_id` int,
  `role` varchar(50),
  PRIMARY KEY (`role_id`)
);

CREATE TABLE `user` (
  `user_id` int,
  `email` varchar(255),
  `fname` varchar(255),
  `lname` varchar(255),
  `password` varchar(255),
  `role_id_usr` int,
  PRIMARY KEY (`user_id`),
  FOREIGN KEY (`role_id_usr`) REFERENCES `user_role`(`role_id`) ON DELETE CASCADE
);

CREATE TABLE `tag` (
  `tag_id` int,
  `tag_name` varchar(255),
  `tag_description` varchar(1000),
  PRIMARY KEY (`tag_id`)
);

CREATE TABLE `user_tag_preference` (
  `user_tag_preference_id` int,
  `tag_id_utp` int,
  `user_id_utp` int,
  PRIMARY KEY (`user_tag_preference_id`),
  FOREIGN KEY (`user_id_utp`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`tag_id_utp`) REFERENCES `tag`(`tag_id`) ON DELETE CASCADE
);

CREATE TABLE `recipe` (
  `recipe_id` int,
  `title` varchar(255),
  `description` varchar(1000),
  `prep_time` time,
  `cook_time` time,
  `serving_size` int,
  `user_id_rec` int,
  `image_filename` varchar(255),
  PRIMARY KEY (`recipe_id`),
  FOREIGN KEY (`user_id_rec`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
);

CREATE TABLE `menu` (
  `menu_id` int,
  `user_id_men` int,
  `date_created` datetime,
  `date_start` datetime,
  `is_approved` bool,
  PRIMARY KEY (`menu_id`),
  FOREIGN KEY (`user_id_men`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
);

CREATE TABLE `menu_recipe` (
  `menu_recipe_id` int,
  `recipe_id_mnr` int,
  `menu_id_mnr` int,
  PRIMARY KEY (`menu_recipe_id`),
  FOREIGN KEY (`recipe_id_mnr`) REFERENCES `recipe`(`recipe_id`) ON DELETE CASCADE,
  FOREIGN KEY (`menu_id_mnr`) REFERENCES `menu`(`menu_id`) ON DELETE CASCADE
);

CREATE TABLE `ingredient` (
  `ingredient_id` int,
  `ingredient_name` varchar(255),
  PRIMARY KEY (`ingredient_id`)
);

CREATE TABLE `recipe_ingredient` (
  `recipe_ingredient_id` int,
  `ingredient_id_rpi` int,
  `quantity` int,
  `recipe_id_rpi` int,
  `unit_measure_id_rpi` varchar(20),
  PRIMARY KEY (`recipe_ingredient_id`),
  FOREIGN KEY (`ingredient_id_rpi`) REFERENCES `ingredient`(`ingredient_id`) ON DELETE CASCADE,
  FOREIGN KEY (`unit_measure_id_rpi`) REFERENCES `unit_measure`(`unit_measure_id`) ON DELETE CASCADE,
  FOREIGN KEY (`recipe_id_rpi`) REFERENCES `recipe`(`recipe_id`) ON DELETE CASCADE
);

CREATE TABLE `menu_recipe_qeue` (
  `menu_recipe_qeue_id` int,
  `user_id_mrq` int,
  `recipe_id_mrq` int,
  PRIMARY KEY (`menu_recipe_qeue_id`),
  FOREIGN KEY (`user_id_mrq`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`recipe_id_mrq`) REFERENCES `recipe`(`recipe_id`) ON DELETE CASCADE
);

CREATE TABLE `user_favorite` (
  `user_favorite_id` int,
  `user_id_usf` int,
  `recipe_id_usf` int,
  PRIMARY KEY (`user_favorite_id`),
  FOREIGN KEY (`user_id_usf`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`recipe_id_usf`) REFERENCES `recipe`(`recipe_id`) ON DELETE CASCADE
);
