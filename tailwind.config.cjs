const { fontFamily } = require('tailwindcss/defaultTheme')
const config = require('./tailwind.theme.config.cjs')
/**
 * Find the applicable theme color palette, or use the default one
 */
const themeConfig = process.env.THEME_KEY && config[process.env.THEME_KEY] ? config[process.env.THEME_KEY] : config.default
const { colors } = themeConfig
module.exports = {
    darkMode: 'class',
    content: [
        './public/**/*.html',
        './src/**/*.{astro,js,ts}'
    ],
    safelist: ['dark'],
    theme: {
		fontFamily: {
			sans: ['"Mamelon"', 'Fira Code', ...fontFamily.sans],
		},
		extend: {
            colors: {
                theme: {
                    ...colors
                }
            },
            typography: (theme) => ({
                dark: {
                    css: {
                        color: theme("colors.gray.200"),
                        blockquote: {
                            color: colors.dark.primary,
                            borderColor: colors.primary
                        },
                        'blockquote > p::before, p::after': {
                            color: colors.primary,
                        },
                    },
                },
                DEFAULT: {
                    css: {
                        a: {
                            color: colors.dark.primary,
                              '&:hover': {
                                color: colors.primary,
                              },
                        },
                        blockquote: {
                            color: colors.primary,
                            fontSize: theme("fontSize.2xl"),
                            borderColor: colors.dark.primary,
                        },
                        'blockquote > p::before, p::after': {
                            color: colors.dark.primary,
                        },
                        h1: {
                            color: colors.dark.secondary,
                            marginTop: '0.75rem',
                            marginBottom: '0.5rem',
                        },
                        h2: {
                            color: colors.dark.secondary,
                            marginTop: '1.5rem',
                            marginBottom: '0.5rem',
                        },
                        h3: {
                            color: colors.dark.secondary,
                            marginTop: '0.5rem',
                            marginBottom: '0.5rem',
                        },
                        p: {
                            marginTop: '0.5rem',
                            marginBottom: '0.5rem',
                        },
                    }
                },
            }),
		},
	},
    variants: {
        extend: { typography: ["dark"] }
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
    ]
};
