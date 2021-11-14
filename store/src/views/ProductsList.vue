<!-- This example requires Tailwind CSS v2.0+ -->
<template>
	<div>
		<div class="bg-white px-4 py-5 border-b border-gray-200 sm:px-6">
			<div
				class="
					-ml-4
					-mt-2
					flex
					items-center
					justify-between
					flex-wrap
					sm:flex-nowrap
				"
			>
				<div class="ml-4 mt-2">
					<h3 class="text-lg leading-6 font-medium text-gray-900">
						All Products
					</h3>
				</div>
				<div class="ml-4 mt-2 flex-shrink-0">
					<button
						type="button"
						class="
							relative
							inline-flex
							items-center
							px-4
							py-2
							border border-transparent
							shadow-sm
							text-sm
							font-medium
							rounded-md
							text-white
							bg-indigo-600
							hover:bg-indigo-700
							focus:outline-none
							focus:ring-2
							focus:ring-offset-2
							focus:ring-indigo-500
						"
					>
						Create new product
					</button>
				</div>
			</div>
		</div>

		<div class="px-5" v-if="$resources.allProducts.loading">
			Loading Products
		</div>
		<div
			v-if="$resources.allProducts.data"
			class="
				px-5
				mt-12
				max-w-lg
				mx-auto
				grid
				gap-5
				lg:grid-cols-3 lg:max-w-none
			"
		>
			<div
				class="flex flex-col rounded-lg shadow-lg overflow-hidden"
				v-for="product in $resources.allProducts.data"
				:key="product.name"
			>
				<div class="flex-shrink-0">
					<img class="h-48 w-full object-cover" :src="product.image" alt="" />
				</div>
				<div class="flex-1 bg-white p-6 flex flex-col justify-between">
					<div class="flex-1">
						<p class="text-sm font-medium text-indigo-600">
							<a href="#" class="hover:underline">
								{{ product.category }}
							</a>
						</p>
						<a class="block mt-2">
							<p class="text-xl font-semibold text-gray-900">
								{{ product.title }}
							</p>
							<p class="mt-3 text-base text-gray-500">
								{{ product.short_description }}
							</p>
						</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {};
	},
	resources: {
		allProducts() {
			return {
				method: 'digistore.api.product.all_products',
				auto: true,
				onSuccess(d) {
					console.log('Products fetched.', d);
				},
			};
		},
	},
};
</script>
