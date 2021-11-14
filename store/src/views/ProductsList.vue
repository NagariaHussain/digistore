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
				<div class="ml-4 mt-2 flex-shrink-0"></div>
			</div>
		</div>

		<div class="py-5 px-5" v-if="$resources.allProducts.loading">
			<button
				type="button"
				class="
					inline-flex
					items-center bg-indigo-500
					px-4
					py-2
					border border-transparent
					text-base
					leading-6
					font-medium
					rounded-md
					text-white
					bg-rose-600
					hover:bg-rose-500
					focus:border-rose-700
					active:bg-rose-700
					transition
					ease-in-out
					duration-150
					cursor-not-allowed
				"
			>
				<svg
					class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
				>
					<circle
						class="opacity-25"
						cx="12"
						cy="12"
						r="10"
						stroke="currentColor"
						stroke-width="4"
					></circle>
					<path
						class="opacity-75"
						fill="currentColor"
						d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
					></path>
				</svg>
				Loading
			</button>
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
