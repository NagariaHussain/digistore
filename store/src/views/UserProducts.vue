<template>
	<div>
		<h2>Your Products</h2>
		<ol v-if="$resources.userProducts.data">
			<li v-for="p in $resources.userProducts.data" :key="p.product.name">
				{{ p.product.title }}
			</li>
		</ol>
	</div>
</template>

<script>
export default {
	name: 'UserProducts',
	resources: {
		userProducts() {
			console.log(this.$account.user.name);
			return {
				method: 'digistore.api.product.purchased',
				params: {
					user: this.$account.user.name,
				},
				auto: true,
				onSuccess(d) {
					console.log(d);
				},
			};
		},
	},
	inject: ['$auth', '$account'],
};
</script>
