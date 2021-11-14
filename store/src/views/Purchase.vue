<template>
	<div class="p-4">
		<LoadingSpinner :loading="$resources.getData.loading" />
		<div>Product ID: {{ productName }}</div>
		<ul v-for="d in $resources.getData.data" :key="d">
			Link:
			<a>d</a>
		</ul>
	</div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
	name: 'Purchase',
	components: { LoadingSpinner },
	resources: {
		getData() {
			return {
				method: 'digistore.api.product.get_data',
				params: {
					product: this.productName,
				},
				// auto: true,
			};
		},
	},
	props: ['productName'],
};
</script>
