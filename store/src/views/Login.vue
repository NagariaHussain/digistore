<template>
	<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
		<h2 class="my-6 text-center text-3xl font-extrabold text-gray-900">
			Sign in to your account
		</h2>

		<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
			<form class="space-y-6" @submit.prevent="login">
				<div>
					<label for="email" class="block text-sm font-medium text-gray-700">
						Email address
					</label>
					<div class="mt-1">
						<input
							v-model="email"
							id="email"
							name="email"
							:type="email !== 'Administrator' ? 'email' : 'text'"
							autocomplete="email"
							required="true"
							class="
								appearance-none
								block
								w-full
								px-3
								py-2
								border border-gray-300
								rounded-md
								shadow-sm
								placeholder-gray-400
								focus:outline-none focus:ring-indigo-500 focus:border-indigo-500
								sm:text-sm
							"
						/>
					</div>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-gray-700">
						Password
					</label>
					<div class="mt-1">
						<input
							v-model="password"
							id="password"
							name="password"
							type="password"
							autocomplete="current-password"
							required=""
							class="
								appearance-none
								block
								w-full
								px-3
								py-2
								border border-gray-300
								rounded-md
								shadow-sm
								placeholder-gray-400
								focus:outline-none focus:ring-indigo-500 focus:border-indigo-500
								sm:text-sm
							"
						/>
					</div>
				</div>

				<ErrorMessage :error="errorMessage" class="mt-4" />

				<div class="flex items-center justify-between">
					<div class="text-sm">
						<a
							href="#"
							class="font-medium text-indigo-600 hover:text-indigo-500"
						>
							Forgot your password?
						</a>
					</div>
				</div>

				<div>
					<button
						type="submit"
						class="
							w-full
							flex
							justify-center
							py-2
							px-4
							border border-transparent
							rounded-md
							shadow-sm
							text-sm
							font-medium
							text-white
							bg-indigo-600
							hover:bg-indigo-700
							focus:outline-none
							focus:ring-2
							focus:ring-offset-2
							focus:ring-indigo-500
						"
					>
						Sign in
					</button>
				</div>
			</form>
		</div>
	</div>
</template>
<script>
export default {
	data() {
		return {
			email: null,
			password: null,
			errorMessage: null,
		};
	},
	inject: ['$auth'],
	async mounted() {
		if (this.$route?.query?.route) {
			this.redirect_route = this.$route.query.route;
			this.$router.replace({ query: null });
		}
	},
	methods: {
		async login() {
			if (this.email && this.password) {
				try {
					let res = await this.$auth.login(this.email, this.password);
					if (res) {
						this.$router.push({ name: 'Home' });
					}
				} catch (e) {
					this.errorMessage = e.messages?.join('\n');
				}
			}
		},
	},
};
</script>
