CREATE TABLE `accounts` (
  `id` bigint(20) unsigned NOT NULL COMMENT 'Account id.',
  `admin_uid` int(10) unsigned NOT NULL COMMENT 'Admin User id of the Account.',
  `namespace` varchar(25) NOT NULL COMMENT 'Account namespace.',
  `organization` varchar(50) NOT NULL COMMENT 'Account organization.',
  `email` varchar(50) NOT NULL COMMENT 'Account email address.',
  `phone` varchar(50) NOT NULL COMMENT 'Account phone number.',
  `status` tinyint(1) unsigned NOT NULL COMMENT 'Account status.',
  `created` datetime NOT NULL COMMENT 'Datetime when Account created.',
  `updated` datetime NOT NULL COMMENT 'Datetime when Account updated.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_index_namespace` (`namespace`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Accounts data.';

CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'User id.',
  `account_id` bigint(20) unsigned NOT NULL COMMENT 'Account id of the User.',
  `name` varchar(50) NOT NULL COMMENT 'User name.',
  `email` varchar(50) NOT NULL COMMENT 'User email address.',
  `password` varchar(255) NOT NULL COMMENT 'User password.',
  `status` tinyint(1) unsigned NOT NULL COMMENT 'User status.',
  `created` datetime NOT NULL COMMENT 'Datetime when User created.',
  `updated` datetime NOT NULL COMMENT 'Datetime when User updated.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_index_account_id_name` (`account_id`,`name`),
  UNIQUE KEY `users_index_account_id_email` (`account_id`,`email`),
  KEY `users_index_account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Users data.';
