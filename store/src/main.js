import './index.css';
import { createApp, reactive } from 'vue';
import App from './App.vue';

import router from './router';
import resourceManager from '../../../doppio/vision/src/resourceManager';
import call from './controllers/call';
import socket from './controllers/socket';
import Auth from './controllers/auth';
import Account from './controllers/account';

const app = createApp(App);
const auth = reactive(new Auth());
const account = reactive(new Account());

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties,
// components can inject this
app.provide('$auth', auth);
app.provide('$call', call);
app.provide('$socket', socket);
app.provide('$account', account);

// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			if (!account.user) {
				await account.fetchAccount();
			}
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			if (!account.user) {
				await account.fetchAccount();
			}
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

app.mount('#app');

window.$account = account;
