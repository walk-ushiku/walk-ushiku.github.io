import { z, defineCollection } from "astro:content";

const blogCollection = defineCollection({
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
        }),
});

export const collections = {
	blog: blogCollection,
	course: courseCollection,
};
