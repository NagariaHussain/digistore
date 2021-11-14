<template>
	<div>
		<LoadingSpinner :loading="$resources.productData.loading" />
		<div class="mt-8 px-4 prose" v-if="productData">
			<h1>
				{{ productData.product_doc.title }}
			</h1>
			<p>{{ productData.product_doc.short_description }}</p>
			<h2>Plans</h2>
			<ul>
				<li v-for="plan in productData.product_plans" :key="plan.title">
					{{ plan.title }}
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
	components: { LoadingSpinner },
	name: 'Product',
	props: ['productName'],
	resources: {
		productData() {
			return {
				method: 'digistore.api.product.get',
				params: {
					name: this.productName,
				},
				auto: true,
				onSuccess(d) {
					console.log(d);
				},
			};
		},
	},
	computed: {
		productData() {
			if (
				!this.$resources.productData.loading &&
				this.$resources.productData.data
			) {
				return this.$resources.productData.data;
			}
		},
	},
};
</script>
