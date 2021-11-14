import call from './call';

export default class Account {
	constructor() {
		this.user = null;
	}

	async fetchAccount() {
		if (document.cookie.includes('user_id=Guest;')) {
			return;
		}
		let result = await call('digistore.api.account.get');
		this.user = result.user;
	}
}
