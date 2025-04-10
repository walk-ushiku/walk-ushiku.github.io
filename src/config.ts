import type { NavItems } from "./types";

export const NAV_ITEMS: NavItems = {
	home: {
		path: "/",
		title: "ホーム",
	},
	blog: {
		path: "/blog",
		title: "観光地",
	},
	tags: {
		path: "/tags",
		title: "ジャンル別",
	},
	media: {
		path: "/links",
		title: "リンク集",
	},
	about: {
		path: "/others",
		title: "その他",
	},
};

export const SITE = {
	// Your site's detail?
	title: "牛久散歩部",
	name: "牛久散歩部オンライン",
	description: "食べて、見て、歩く。",
	url: "https://astro-ink.vercel.app",
	githubUrl: "https://github.com/one-aalam/astro-ink",
	listDrafts: true,
	image:
		"https://raw.githubusercontent.com/one-aalam/astro-ink/main/public/astro-banner.png",
	// YT video channel Id (used in media.astro)
	ytChannelId: "",
	// Optional, user/author settings (example)
	// Author: name
	author: "", // Example: Fred K. Schott
	// Author: Twitter handler
	authorTwitter: "", // Example: FredKSchott
	// Author: Image external source
	authorImage: "", // Example: https://pbs.twimg.com/profile_images/1272979356529221632/sxvncugt_400x400.jpg, https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png
	// Author: Bio
	authorBio:
		"Crisp, minimal, personal blog theme for Astro. Crisp, minimal, personal blog theme for Astro. Crisp, minimal, personal blog theme for Astro",
};

// Ink - Theme configuration
export const PAGE_SIZE = 8;
export const USE_POST_IMG_OVERLAY = false;
export const USE_MEDIA_THUMBNAIL = true;

export const USE_AUTHOR_CARD = true;
export const USE_SUBSCRIPTION = false; /* works only when USE_AUTHOR_CARD is true */

export const USE_VIEW_STATS = true;
