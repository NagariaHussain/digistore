export default [
	{
		path: '/products/:productName',
		name: 'Product',
		component: () => import('../views/Product.vue'),
		props: true,
		meta: {
			isPublicPage: true,
		},
	},
	{
		path: '/success',
		name: 'Success',
		component: () => import('../views/Success.vue'),
	},
];
