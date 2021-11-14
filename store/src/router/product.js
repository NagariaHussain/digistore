import UserProducts from '../views/UserProducts.vue';

export default [
	{
		path: '/purchases',
		name: 'Purchases',
		component: UserProducts,
	},
	{
		path: '/products/:productName',
		name: 'Product',
		component: () => import('../views/Product.vue'),
		props: true,
	},
	{
		path: '/success',
		name: 'Success',
		component: () => import('../views/Success.vue'),
	},
	{
		path: '/purchase/:productName',
		name: 'Purchase',
		component: () => import('../views/Purchase.vue'),
		props: true,
	},
];
