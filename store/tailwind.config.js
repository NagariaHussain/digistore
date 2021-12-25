const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
	content: ['./public/**/*.html', './src/**/*.{js,jsx,ts,tsx,vue}'],
	theme: {
		extend: {
			fontFamily: {
				sans: ['Inter var', ...defaultTheme.fontFamily.sans],
			},
		},
	},
	plugins: [require('@tailwindcss/typography')],
};
