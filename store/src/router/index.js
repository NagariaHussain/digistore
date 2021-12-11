import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import authRoutes from './auth';
import productRoutes from './product';
import purchaseRoutes from './purchase';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
	...authRoutes,
	...productRoutes,
	...purchaseRoutes,
];

const router = createRouter({
	base: '/store/',
	history: createWebHistory(),
	routes,
});

export default router;
