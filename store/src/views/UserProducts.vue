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
						Your Products
					</h3>
				</div>
				<div class="ml-4 mt-2 flex-shrink-0"></div>
			</div>
		</div>

		<!-- Loading state -->
		<div class="py-5 px-5" v-if="$resources.userProducts.loading">
			<button
				type="button"
				class="
					inline-flex
					items-center
					bg-indigo-500
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

		<div v-if="$resources.userProducts.data" class="flow-root mt-6 px-40">
			<ul role="list" class="-my-5 divide-y divide-gray-200">
				<li
					v-for="p in $resources.userProducts.data"
					:key="p.product.name"
					class="py-4"
				>
					<div class="flex items-center space-x-4">
						<div class="flex-shrink-0">
							<img
								class="h-8 w-8 rounded-full"
								:src="p.product.image"
								alt="Product Image"
							/>
						</div>
						<div class="flex-1 min-w-0">
							<p class="text-sm font-medium text-gray-900 truncate">
								{{ p.product.title }}
							</p>
							<p class="text-sm text-gray-500 truncate">
								{{ p.product.category }}
							</p>
						</div>
						<div>
							<a
								href="#"
								class="
									inline-flex
									items-center
									shadow-sm
									px-2.5
									py-0.5
									border border-gray-300
									text-sm
									leading-5
									font-medium
									rounded-full
									text-gray-700
									bg-white
									hover:bg-gray-50
								"
							>
								View
							</a>
						</div>
					</div>
				</li>
			</ul>
		</div>
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
