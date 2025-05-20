import type { NavItems } from "./types";

export const SITE = {
	// Your site's detail?
	title: "うしくさんぽノート",
	name: "うしくさんぽノート",
	description: "有志による非公式の牛久市観光サイトです。",
	url: "https://walk-ushiku.github.io/",
	githubUrl: "https://github.com/walk-ushiku/walk-ushiku.github.io",
	listDrafts: true,
	image:
		"https://walk-ushiku.github.io/favicon/favicon-256x256.png",
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
		"牛久散歩部",
};

// Ink - Theme configuration
export const PAGE_SIZE = 20;
export const USE_POST_IMG_OVERLAY = false;
export const USE_MEDIA_THUMBNAIL = true;

export const USE_AUTHOR_CARD = true;
export const USE_SUBSCRIPTION = false; /* works only when USE_AUTHOR_CARD is true */

export const USE_VIEW_STATS = true;
