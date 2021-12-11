import './index.css';
import { createApp, reactive } from 'vue';
import App from './App.vue';

import router from './router';
import resourceManager from './resourceManager';
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

// Import Global components
let components = import.meta.globEager('./globals/*.vue'); // To get each component inside globals folder

for (let path in components) {
	let component = components[path];
	let name = path.replace('./globals/', '').replace('.vue', '');
	console.log(name);
	app.component(name, component.default || component);
}

// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	console.log(
		'isLogin',
		to,
		to.matched.some((record) => record.meta.isLoginPage)
	);
	console.log(
		'isPublic',
		to,
		to.matched.some((record) => record.meta.isPublicPage)
	);

	if (
		to.matched.some((record) => !record.meta.isLoginPage) &&
		to.matched.some((record) => !record.meta.isPublicPage)
	) {
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
		// Public page
		if (to.matched.some((record) => record.meta.isPublicPage)) {
			console.log('Visiting public page...');
			next();
		}

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
