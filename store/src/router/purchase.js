import UserProducts from '../views/UserProducts.vue';

export default [
	{
		path: '/purchases',
		name: 'Purchases',
		component: UserProducts,
	},
	{
		path: '/purchases/:purchaseName',
		name: 'SinglePurchase',
		component: () => import('../views/Purchase.vue'),
		props: true,
	},
];
