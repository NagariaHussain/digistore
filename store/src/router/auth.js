import UserProducts from '../views/UserProducts.vue';

export default [
	{
		path: '/login',
		name: 'Login',
		component: () =>
			import(/* webpackChunkName: "login" */ '../views/Login.vue'),
		meta: {
			isLoginPage: true,
		},
		props: true,
	},
	{
		path: '/purchases',
		name: 'Purchases',
		component: UserProducts,
	},
];
