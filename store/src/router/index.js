import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import authRoutes from './auth';
import productRoutes from './product';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
	...authRoutes,
	...productRoutes,
];

const router = createRouter({
	base: '/store/',
	history: createWebHistory(),
	routes,
});

export default router;
