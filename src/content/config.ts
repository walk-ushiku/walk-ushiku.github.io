import { z, defineCollection } from "astro:content";

const spotNoteCollection = defineCollection({
	schema: z.object({
		title: z
			.string()
			.max(100, "The title length must be less than or equal to 100 chars"),
		description: z.string(),
		tags: z.array(z.string()),
		icon: z.string().optional(),
		lat: z.number(),
		lng: z.number(),
		id: z.number(),
		gmap: z.string(),
	}),
});

const courseCollection = defineCollection({
        schema: z.object({
                title: z
                        .string()
                        .max(100, "The title length must be less than or equal to 100 chars"),
                description: z.string(),
                image: z.string().optional(),
                icon: z.string(),
		id: z.number(),
        }),
});

const userCollection = defineCollection({
        schema: z.object({
                title: z
                        .string()
                        .max(100, "The title length must be less than or equal to 100 chars"),
		twitter_id: z.string(),
        }),
});

const noteCollection = defineCollection({
        schema: z.object({
                title: z
                        .string()
                        .max(100, "The title length must be less than or equal to 100 chars"),
                description: z.string(),
                image: z.string().optional(),
                id: z.number(),
        }),
});

const photoPagesCollection = defineCollection({
        schema: z.object({
		image: z.string(),
		contributor: z.string(),
		contributor_id: z.string().optional(),
		description: z.string().optional(),
		related_place: z.string().optional(),
		lat: z.number().optional(),
		lng: z.number().optional(),
        }),
});

export const collections = {
	spot_note: spotNoteCollection,
	course: courseCollection,
	photo_pages: photoPagesCollection,
	note: noteCollection,
	user: userCollection,
};
