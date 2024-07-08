CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `username` varchar(255) UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `avatar` varchar(255) UNIQUE NOT NULL,
  `access_token` varchar(255) UNIQUE,
  `refresh_token` varchar(255) UNIQUE,
  `created_at` timestamp
);

CREATE TABLE `WebFeedback` (
  `id` integer PRIMARY KEY,
  `body` text COMMENT 'Content of the user feedback',
  `user_id` integer,
  `sentiment` enum(0,1,2) DEFAULT 0,
  `created_at` timestamp
);

CREATE TABLE `userComment` (
  `id` integer PRIMARY KEY,
  `body` text COMMENT 'content of user comment',
  `user_id` integer,
  `regarding` enum(stock,ipo),
  `for_comapany` integer,
  `sentiment` enum(0,1,2) COMMENT '0:negative, 1:neutral, 2:posetive',
  `created_at` timestamp
);

CREATE TABLE `company` (
  `id` integer PRIMARY KEY,
  `company_id` varchar(255) UNIQUE NOT NULL,
  `company_name` varchar(255),
  `mcap` bigint,
  `price_file_url` varchar(255),
  `sector` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `news` (
  `id` integer PRIMARY KEY,
  `headline` varchar2(300) NOT NULL,
  `news_url` varchar2 NOT NULL,
  `sentiment` enum(0,1,2) NOT NULL,
  `sentiment_statement` varchar(255) NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `newsCompanyRelation` (
  `id` integer PRIMARY KEY,
  `news_id` integer,
  `company_id` integer,
  `created_at` timestamp
);

CREATE TABLE `investorDistribution` (
  `id` integer PRIMARY KEY,
  `company_id` integer,
  `fii` integer,
  `dii` integer,
  `anchor_investor` integer NOT NULL,
  `nii` integer NOT NULL,
  `bnii` integer NOT NULL,
  `snii` integer NOT NULL,
  `retailer` integer NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `event` (
  `id` integer PRIMARY KEY,
  `event_name` varchar(255) NOT NULL,
  `event_date` datetime NOT NULL,
  `company_id` integer NOT NULL,
  `related_to` enum(stock,ipo,general) NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `ipoTable` (
  `id` integer PRIMARY KEY,
  `company_id` integer UNIQUE NOT NULL,
  `price_band` integer NOT NULL,
  `lot_size` integer NOT NULL,
  `offer_for_sale` bigint,
  `fresh_issue` bigint,
  `listing_platform` varchar(255) NOT NULL,
  `primoter_holding_preissue` float COMMENT '% of share held by promoter',
  `promoter_share_pre_issue` bigint NOT NULL,
  `promoter_share_post_issue` bigint NOT NULL DEFAULT 0,
  `about_company` text NOT NULL,
  `about_ipo` text NOT NULL,
  `overall_subscriptionX` float,
  `roe` float,
  `roce` float,
  `debt_to_equity` float,
  `ronw` float,
  `p_to_bv` float,
  `pat_margin` float,
  `rhp_url` varchar(255),
  `drhp_url` varchar(255) NOT NULL,
  `anchor_investor_url` varchar(255) NOT NULL,
  `registrar` integer,
  `created_at` timestamp
);

CREATE TABLE `ipoLotSize` (
  `id` integer PRIMARY KEY,
  `price_per_issue` integer NOT NULL,
  `lot_size` integer NOT NULL,
  `retail_min` integer NOT NULL,
  `retail_max` integer NOT NULL
);

CREATE TABLE `registrar` (
  `id` integer PRIMARY KEY,
  `name` varchar(255) UNIQUE NOT NULL,
  `webpage` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255),
  `created_at` timestamp
);

ALTER TABLE `newsCompanyRelation` ADD FOREIGN KEY (`news_id`) REFERENCES `news` (`id`);

ALTER TABLE `newsCompanyRelation` ADD FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);

ALTER TABLE `investorDistribution` ADD FOREIGN KEY (`id`) REFERENCES `ipoTable` (`id`);

ALTER TABLE `ipoLotSize` ADD FOREIGN KEY (`id`) REFERENCES `ipoTable` (`id`);

ALTER TABLE `ipoTable` ADD FOREIGN KEY (`registrar`) REFERENCES `registrar` (`id`);

ALTER TABLE `ipoTable` ADD FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);

ALTER TABLE `event` ADD FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);

ALTER TABLE `userComment` ADD FOREIGN KEY (`for_comapany`) REFERENCES `company` (`id`);

ALTER TABLE `userComment` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `WebFeedback` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
